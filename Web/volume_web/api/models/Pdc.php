<?php

class Pdc {

    public static function search(string $query, array $filters, int $page, int $rows) {
        try {
            $sql = "SELECT DISTINCT 
                        p.*, 
                        s.nom AS station_nom, s.implantation, s.adresse, s.latitude, s.longitude, s.horaires, s.ouvert_24_7, 
                        e.nom AS enseigne_nom, 
                        a.nom AS amenageur_nom, a.siren, a.contact AS amenageur_contact, 
                        o.nom AS operateur_nom, o.telephone, o.contact AS operateur_contact 
                    FROM pdc p 
                    INNER JOIN station s ON s.id_station_itinerance = p.id_station_itinerance 
                    INNER JOIN enseigne e ON e.id_enseigne = s.id_enseigne 
                    INNER JOIN amenageur a ON a.id_amenageur = s.id_amenageur 
                    INNER JOIN operateur o ON o.id_operateur = s.id_operateur ";
                    
            if (!empty($filters['prises'])) {
                $sql .= "LEFT JOIN type_prise_pdc tpp ON p.id_pdc_itinerance = tpp.id_pdc_itinerance ";
            }
            if (!empty($filters['paiement'])) {
                $sql .= "LEFT JOIN type_paiement_pdc tpa ON p.id_pdc_itinerance = tpa.id_pdc_itinerance ";
            }

            $conditions = [];
            $params = [];

            if (!empty($query)) {
                $conditions[] = "(s.nom LIKE :search OR s.adresse LIKE :search)";
                $params[':search'] = '%' . $query . '%';
            }

            if ($filters['ouvert_24_7'] !== null) {
                $conditions[] = "s.ouvert_24_7 = :h24";
                $params[':h24'] = $filters['ouvert_24_7'];
            }
            if ($filters['id_enseigne'] !== null) {
                $conditions[] = "s.id_enseigne = :enseigne";
                $params[':enseigne'] = $filters['id_enseigne'];
            }
            if ($filters['id_operateur'] !== null) {
                $conditions[] = "s.id_operateur = :operateur";
                $params[':operateur'] = $filters['id_operateur'];
            }
            if ($filters['charge_rapide'] !== null) {
                $conditions[] = "p.charge_rapide = :rapide";
                $params[':rapide'] = $filters['charge_rapide'];
            }
            if ($filters['reservation'] !== null) {
                $conditions[] = "p.reservation = :reservation";
                $params[':reservation'] = $filters['reservation'];
            }
            if ($filters['condition_access'] !== null) {
                $conditions[] = "p.condition_access = :acces";
                $params[':acces'] = $filters['condition_access'];
            }
            if ($filters['restriction_gabarit'] !== null) {
                $conditions[] = "p.restriction_gabarit = :gabarit";
                $params[':gabarit'] = $filters['restriction_gabarit'];
            }
            if ($filters['accessibilite_pmr'] !== null) {
                $conditions[] = "p.accessibilite_pmr LIKE :pmr";
                $params[':pmr'] = '%' . $filters['accessibilite_pmr'] . '%';
            }

            if (!empty($filters['prises'])) {
                $inQuery = implode(',', array_map(function($i) { return ":prise_$i"; }, array_keys($filters['prises'])));
                $conditions[] = "tpp.id_type_prise IN ($inQuery)";
                foreach ($filters['prises'] as $index => $val) {
                    $params[":prise_$index"] = (int)$val;
                }
            }
            if (!empty($filters['paiement'])) {
                $inQuery = implode(',', array_map(function($i) { return ":paie_$i"; }, array_keys($filters['paiement'])));
                $conditions[] = "tpa.id_type_paiement IN ($inQuery)";
                foreach ($filters['paiement'] as $index => $val) {
                    $params[":paie_$index"] = (int)$val;
                }
            }

            if (!empty($conditions)) {
                $sql .= " WHERE " . implode(" AND ", $conditions);
            }

            $sql .= " LIMIT :limit OFFSET :offset";
            
            $params[':limit'] = (int)$rows;
            $params[':offset'] = ($page - 1) * $rows;
            
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
                    p.*, 
                    s.nom AS station_nom, s.implantation, s.adresse, s.latitude, s.longitude, s.horaires, s.ouvert_24_7, 
                    e.nom AS enseigne_nom, 
                    a.nom AS amenageur_nom, a.siren, a.contact AS amenageur_contact, 
                    o.nom AS operateur_nom, o.telephone, o.contact AS operateur_contact 
                FROM pdc p 
                INNER JOIN station s ON s.id_station_itinerance=p.id_station_itinerance 
                INNER JOIN enseigne e ON e.id_enseigne=s.id_enseigne 
                INNER JOIN amenageur a ON a.id_amenageur=s.id_amenageur 
                INNER JOIN operateur o ON o.id_operateur=s.id_operateur
                WHERE p.id_pdc_itinerance=?;",
                [$id]
            );

            if ($statement) {
                return $statement->fetch(PDO::FETCH_ASSOC);
            }
            return false;
        } catch (PDOException $exception) {
            error_log('Request error: '.$exception->getMessage());
            return false;
        }
    }

    public static function getAll(int $page, int $rows) {
        try {
            $statement = Database::preparedQuery(
                "SELECT 
                    p.*, 
                    s.nom AS station_nom, s.implantation, s.adresse, s.latitude, s.longitude, s.horaires, s.ouvert_24_7, 
                    e.nom AS enseigne_nom, 
                    a.nom AS amenageur_nom, a.siren, a.contact AS amenageur_contact, 
                    o.nom AS operateur_nom, o.telephone, o.contact AS operateur_contact 
                FROM pdc p 
                INNER JOIN station s ON s.id_station_itinerance=p.id_station_itinerance 
                INNER JOIN enseigne e ON e.id_enseigne=s.id_enseigne 
                INNER JOIN amenageur a ON a.id_amenageur=s.id_amenageur 
                INNER JOIN operateur o ON o.id_operateur=s.id_operateur
                LIMIT :limit OFFSET :offset;",
                [
                    ':limit' => (int)$rows,
                    ':offset' => (int)(($page - 1) * $rows)
                ]
            );

            if ($statement) {
                return $statement->fetchAll(PDO::FETCH_ASSOC);
            }
            return false;
        } catch (PDOException $exception) {
            error_log('Request error: '.$exception->getMessage());
            return false;
        }
    }
}
?>