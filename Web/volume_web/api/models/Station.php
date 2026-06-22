<?php

    class Station {

        public static function search(string $query, array $filters, int $page, int $rows) {
            try {
                $sql = "SELECT 
                            s.id_station_itinerance, s.nom AS station_nom, s.implantation, s.adresse, s.latitude, s.longitude, s.horaires, s.ouvert_24_7, 
                            e.nom AS enseigne_nom, 
                            a.nom AS amenageur_nom, a.siren, a.contact AS amenageur_contact, 
                            o.nom AS operateur_nom, o.telephone, o.contact AS operateur_contact 
                        FROM station s
                        INNER JOIN enseigne e ON e.id_enseigne=s.id_enseigne 
                        INNER JOIN amenageur a ON a.id_amenageur=s.id_amenageur 
                        INNER JOIN operateur o ON o.id_operateur=s.id_operateur";

                $conditions = [];
                $params = [];

                if (!empty($query)) {
                    $conditions[] = "(s.nom LIKE :search OR s.adresse LIKE :search)";
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

                if (!empty($conditions)) {
                    $sql .= " WHERE " . implode(" AND ", $conditions);
                }

                $sql .= " LIMIT :limit OFFSET :offset";
                $params[':limit'] = (int)$rows;
                $params[':offset'] = (int)(($page - 1) * $rows);

                $statement = Database::preparedQuery($sql, $params);

                if ($statement) {
                    return $statement->fetchAll(PDO::FETCH_ASSOC);
                }
                return false;
            } catch (PDOException $exception) {
                error_log('Request error: '.$exception->getMessage());
                return false;
            }
        }

        public static function get(string $id) {
            try {
                $statement = Database::preparedQuery(
                    "SELECT 
                        s.id_station_itinerance, s.nom AS station_nom, s.implantation, s.adresse, s.latitude, s.longitude, s.horaires, s.ouvert_24_7, 
                        e.nom AS enseigne_nom, 
                        a.nom AS amenageur_nom, a.siren, a.contact AS amenageur_contact, 
                        o.nom AS operateur_nom, o.telephone, o.contact AS operateur_contact 
                    FROM station s
                    INNER JOIN enseigne e ON e.id_enseigne=s.id_enseigne 
                    INNER JOIN amenageur a ON a.id_amenageur=s.id_amenageur 
                    INNER JOIN operateur o ON o.id_operateur=s.id_operateur
                    WHERE s.id_station_itinerance=?;",
                    [$id]
                );

                $result = $statement->fetch(PDO::FETCH_ASSOC);
            } catch (PDOException $exception) {
                error_log('Request error: '.$exception->getMessage());
                return false;
            }
            
            return $result;
        }

        public static function getAll(int $page, int $rows) {
            try {
                $statement = Database::preparedQuery(
                    "SELECT 
                        s.id_station_itinerance, s.nom AS station_nom, s.implantation, s.adresse, s.latitude, s.longitude, s.horaires, s.ouvert_24_7, 
                        e.nom AS enseigne_nom, 
                        a.nom AS amenageur_nom, a.siren, a.contact AS amenageur_contact, 
                        o.nom AS operateur_nom, o.telephone, o.contact AS operateur_contact 
                    FROM station s 
                    INNER JOIN enseigne e ON e.id_enseigne=s.id_enseigne 
                    INNER JOIN amenageur a ON a.id_amenageur=s.id_amenageur 
                    INNER JOIN operateur o ON o.id_operateur=s.id_operateur
                    LIMIT ? OFFSET ?;",
                    [
                        $rows, 
                        ($page - 1) * $rows
                    ]
                );

                $result = $statement->fetchAll(PDO::FETCH_ASSOC);
            } catch (PDOException $exception) {
                error_log('Request error: '.$exception->getMessage());
                return false;
            }
            
            return $result;
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

                $result = $statement->fetchAll(PDO::FETCH_ASSOC);
            } catch (PDOException $exception) {
                error_log('Request error: '.$exception->getMessage());
                return false;
            }
            
            return $result;
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

                $result = $statement->fetchAll(PDO::FETCH_ASSOC);
            } catch (PDOException $exception) {
                error_log('Request error: '.$exception->getMessage());
                return false;
            }
            
            return $result;
        }

    }

?>