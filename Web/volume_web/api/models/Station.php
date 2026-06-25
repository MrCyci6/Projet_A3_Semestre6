<?php

class Station {

    public static function search(string $query, array $filters, int $page, int $rows) {
        try {
            $sql = "SELECT 
                        s.id_station_itinerance, s.nom AS station_nom, s.adresse, s.latitude, s.longitude, s.horaires, s.ouvert_24_7, 
                        e.nom AS enseigne_nom, 
                        a.nom AS amenageur_nom, a.siren, a.contact AS amenageur_contact, 
                        o.nom AS operateur_nom, o.telephone, o.contact AS operateur_contact,
                        i.denomination AS implantation_nom,
                        c.nom AS commune_nom, c.code_postal, 
                        d.denomination AS departement_nom, 
                        r.denomination AS region_nom, 
                        pa.denomination AS pays_nom
                    FROM station s
                    INNER JOIN enseigne e ON e.id_enseigne = s.id_enseigne 
                    INNER JOIN amenageur a ON a.id_amenageur = s.id_amenageur 
                    INNER JOIN operateur o ON o.id_operateur = s.id_operateur
                    LEFT JOIN implantation i ON s.id_implantation = i.id_implantation
                    INNER JOIN commune c ON s.code_insee = c.code_insee
                    INNER JOIN departement d ON c.id_departement = d.id_departement
                    INNER JOIN region r ON d.id_region = r.id_region
                    INNER JOIN pays pa ON r.id_pays = pa.id_pays";

            $conditions = [];
            $params = [];

            if (!empty($query)) {
                $conditions[] = "(s.nom LIKE :search OR s.adresse LIKE :search OR c.nom LIKE :search OR c.code_postal LIKE :search)";
                $params[':search'] = '%' . $query . '%';
            }

            if (isset($filters['ouvert_24_7']) && $filters['ouvert_24_7'] !== null) {
                $conditions[] = "s.ouvert_24_7 = :h24";
                $params[':h24'] = $filters['ouvert_24_7'];
            }
            if (isset($filters['id_enseigne']) && $filters['id_enseigne'] !== null) {
                $conditions[] = "s.id_enseigne = :enseigne";
                $params[':enseigne'] = $filters['id_enseigne'];
            }
            if (isset($filters['id_operateur']) && $filters['id_operateur'] !== null) {
                $conditions[] = "s.id_operateur = :operateur";
                $params[':operateur'] = $filters['id_operateur'];
            }
            if (isset($filters['id_departement']) && $filters['id_departement'] !== null) {
                $conditions[] = "d.id_departement = :departement";
                $params[':departement'] = $filters['id_departement'];
            }

            if (!empty($conditions)) {
                $sql .= " WHERE " . implode(" AND ", $conditions);
            }

            $sql .= " LIMIT :limit OFFSET :offset";
            $params[':limit'] = (int)$rows;
            $params[':offset'] = (int)(($page - 1) * $rows);

            $statement = Database::preparedQuery($sql, $params);

            return $statement ? $statement->fetchAll(PDO::FETCH_ASSOC) : false;
        } catch (PDOException $exception) {
            error_log('Request error: '.$exception->getMessage());
            return false;
        }
    }

    public static function get(string $id) {
        try {
            $statement = Database::preparedQuery(
                "SELECT 
                    s.id_station_itinerance, s.nom AS station_nom, s.adresse, s.latitude, s.longitude, s.horaires, s.ouvert_24_7, 
                    e.nom AS enseigne_nom, 
                    a.nom AS amenageur_nom, a.siren, a.contact AS amenageur_contact, 
                    o.nom AS operateur_nom, o.telephone, o.contact AS operateur_contact,
                    i.denomination AS implantation_nom,
                    c.nom AS commune_nom, c.code_postal, 
                    d.denomination AS departement_nom, 
                    r.denomination AS region_nom, 
                    pa.denomination AS pays_nom
                FROM station s
                INNER JOIN enseigne e ON e.id_enseigne = s.id_enseigne 
                INNER JOIN amenageur a ON a.id_amenageur = s.id_amenageur 
                INNER JOIN operateur o ON o.id_operateur = s.id_operateur
                LEFT JOIN implantation i ON s.id_implantation = i.id_implantation
                INNER JOIN commune c ON s.code_insee = c.code_insee
                INNER JOIN departement d ON c.id_departement = d.id_departement
                INNER JOIN region r ON d.id_region = r.id_region
                INNER JOIN pays pa ON r.id_pays = pa.id_pays
                WHERE s.id_station_itinerance=?;",
                [$id]
            );

            return $statement ? $statement->fetch(PDO::FETCH_ASSOC) : false;
        } catch (PDOException $exception) {
            error_log('Request error: '.$exception->getMessage());
            return false;
        }
    }

    public static function getByCluster(string $lat_min, string $lat_max, string $lng_min, string $lng_max) {
        try {
            $statement = Database::preparedQuery(
                "SELECT 
                    ROUND(latitude, 1) AS lat, 
                    ROUND(longitude, 1) AS lng, 
                    COUNT(*) AS count 
                FROM station 
                WHERE latitude BETWEEN ? AND ? AND longitude BETWEEN ? AND ?
                GROUP BY ROUND(latitude, 1), ROUND(longitude, 1);",
                [$lat_min, $lat_max, $lng_min, $lng_max]
            );

            return $statement ? $statement->fetchAll(PDO::FETCH_ASSOC) : false;
        } catch (PDOException $exception) {
            error_log('Request error: '.$exception->getMessage());
            return false;
        }
    }

    public static function getByBoundingBox(string $lat_min, string $lat_max, string $lng_min, string $lng_max, int $limit = 500) {
        try {
            $statement = Database::preparedQuery(
                "SELECT 
                    id_station_itinerance, nom, latitude, longitude, ouvert_24_7 
                FROM station 
                WHERE latitude BETWEEN ? AND ? 
                AND longitude BETWEEN ? AND ?
                LIMIT ?;",
                [$lat_min, $lat_max, $lng_min, $lng_max, $limit]
            );

            return $statement ? $statement->fetchAll(PDO::FETCH_ASSOC) : false;
        } catch (PDOException $exception) {
            error_log('Request error: '.$exception->getMessage());
            return false;
        }
    }
}
?>