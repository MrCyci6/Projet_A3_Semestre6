<?php

class Pdc {

    public static function search(string $query, array $filters, int $page, int $rows) {
        try {
            $sql = "SELECT DISTINCT 
                        p.*, 
                        s.nom AS station_nom, s.adresse, s.latitude, s.longitude, s.horaires, s.ouvert_24_7, 
                        e.nom AS enseigne_nom, 
                        a.nom AS amenageur_nom, a.siren, a.contact AS amenageur_contact, 
                        o.nom AS operateur_nom, o.telephone, o.contact AS operateur_contact,
                        i.denomination AS implantation_nom,
                        ca.denomination AS condition_access_nom,
                        racc.denomination AS raccordement_nom,
                        ap.denomination AS accessibilite_pmr_nom,
                        rg.denomination AS restriction_gabarit_nom,
                        c.nom AS commune_nom, c.code_postal, 
                        d.denomination AS departement_nom, 
                        r.denomination AS region_nom, 
                        pa.denomination AS pays_nom
                    FROM pdc p 
                    INNER JOIN station s ON s.id_station_itinerance = p.id_station_itinerance 
                    INNER JOIN enseigne e ON e.id_enseigne = s.id_enseigne 
                    INNER JOIN amenageur a ON a.id_amenageur = s.id_amenageur 
                    INNER JOIN operateur o ON o.id_operateur = s.id_operateur 
                    LEFT JOIN implantation i ON s.id_implantation = i.id_implantation
                    LEFT JOIN condition_access ca ON p.id_condition = ca.id_condition
                    LEFT JOIN raccordement racc ON p.id_raccordement = racc.id_raccordement
                    LEFT JOIN accessibilite_pmr ap ON p.id_accessibilite = ap.id_accessibilite
                    LEFT JOIN restriction_gabarit rg ON p.id_restriction = rg.id_restriction 
                    INNER JOIN commune c ON s.code_insee = c.code_insee
                    INNER JOIN departement d ON c.id_departement = d.id_departement
                    INNER JOIN region r ON d.id_region = r.id_region
                    INNER JOIN pays pa ON r.id_pays = pa.id_pays ";
                    
            if (!empty($filters['prises'])) {
                $sql .= "LEFT JOIN Possede pos ON p.id_pdc_itinerance = pos.id_pdc_itinerance ";
            }
            if (!empty($filters['paiement'])) {
                $sql .= "LEFT JOIN Avoir avo ON p.id_pdc_itinerance = avo.id_pdc_itinerance ";
            }

            $conditions = [];
            $params = [];

            if (!empty($query)) {
                $conditions[] = "(s.nom LIKE :search OR s.adresse LIKE :search OR c.nom LIKE :search OR c.code_postal LIKE :search)";
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
                $conditions[] = "p.id_condition = :acces";
                $params[':acces'] = (int)$filters['condition_access'];
            }
            if ($filters['restriction_gabarit'] !== null) {
                $conditions[] = "p.id_restriction = :gabarit";
                $params[':gabarit'] = (int)$filters['restriction_gabarit'];
            }
            if ($filters['accessibilite_pmr'] !== null) {
                $conditions[] = "p.id_accessibilite = :pmr";
                $params[':pmr'] = (int)$filters['accessibilite_pmr'];
            }

            if (!empty($filters['prises'])) {
                $inQuery = implode(',', array_map(function($i) { return ":prise_$i"; }, array_keys($filters['prises'])));
                $conditions[] = "pos.id_type_prise IN ($inQuery)";
                foreach ($filters['prises'] as $index => $val) {
                    $params[":prise_$index"] = (int)$val;
                }
            }
            if (!empty($filters['paiement'])) {
                $inQuery = implode(',', array_map(function($i) { return ":paie_$i"; }, array_keys($filters['paiement'])));
                $conditions[] = "avo.id_type_paiement IN ($inQuery)";
                foreach ($filters['paiement'] as $index => $val) {
                    $params[":paie_$index"] = (int)$val;
                }
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
                    p.*, 
                    s.nom AS station_nom, s.adresse, s.latitude, s.longitude, s.horaires, s.ouvert_24_7, 
                    e.nom AS enseigne_nom, 
                    a.nom AS amenageur_nom, a.siren, a.contact AS amenageur_contact, 
                    o.nom AS operateur_nom, o.telephone, o.contact AS operateur_contact,
                    i.denomination AS implantation_nom,
                    ca.denomination AS condition_access_nom,
                    racc.denomination AS raccordement_nom,
                    ap.denomination AS accessibilite_pmr_nom,
                    rg.denomination AS restriction_gabarit_nom,
                    c.nom AS commune_nom, c.code_postal, 
                    d.denomination AS departement_nom, 
                    r.denomination AS region_nom, 
                    pa.denomination AS pays_nom
                FROM pdc p 
                INNER JOIN station s ON s.id_station_itinerance = p.id_station_itinerance 
                INNER JOIN enseigne e ON e.id_enseigne = s.id_enseigne 
                INNER JOIN amenageur a ON a.id_amenageur = s.id_amenageur 
                INNER JOIN operateur o ON o.id_operateur = s.id_operateur 
                LEFT JOIN implantation i ON s.id_implantation = i.id_implantation
                LEFT JOIN condition_access ca ON p.id_condition = ca.id_condition
                LEFT JOIN raccordement racc ON p.id_raccordement = racc.id_raccordement
                LEFT JOIN accessibilite_pmr ap ON p.id_accessibilite = ap.id_accessibilite
                LEFT JOIN restriction_gabarit rg ON p.id_restriction = rg.id_restriction
                INNER JOIN commune c ON s.code_insee = c.code_insee
                INNER JOIN departement d ON c.id_departement = d.id_departement
                INNER JOIN region r ON d.id_region = r.id_region
                INNER JOIN pays pa ON r.id_pays = pa.id_pays
                WHERE p.id_pdc_itinerance=?;",
                [$id]
            );

            return $statement ? $statement->fetch(PDO::FETCH_ASSOC) : false;
        } catch (PDOException $exception) {
            error_log('Request error: '.$exception->getMessage());
            return false;
        }
    }

    public static function add(array $data) {
        try {
            $conn = Database::getConnection();
            $conn->beginTransaction();
            
            Database::preparedQuery(
                "INSERT INTO pdc (id_pdc_itinerance, puissance_nomiale, gratuit, tarification, reservation, 
                station_deux_roues, num_pdl, date_mise_en_service, observations, date_maj, 
                last_modified, created_at, charge_rapide, nbr_pdc, id_station_itinerance, 
                id_raccordement, id_restriction, id_accessibilite, id_condition) 
                VALUES (:id, :puiss, :grat, :tarif, :res, :deuxr, :pdl, :mise, :obs, NOW(), NOW(), NOW(), :rapide, :nbr, :id_st, :racc, :rest, :access, :cond)"
                , 
                [ ':id' => $data['id_pdc_itinerance'], ':puiss' => $data['puissance'], ':grat' => $data['gratuit'], 
                ':tarif' => $data['tarification'], ':res' => $data['reservation'], ':deuxr' => $data['deux_roues'],
                ':pdl' => $data['num_pdl'], ':mise' => $data['date_service'], ':obs' => $data['obs'],
                ':rapide' => $data['charge_rapide'], ':nbr' => $data['nbr_pdc'], ':id_st' => $data['id_station'],
                ':racc' => $data['id_raccordement'], ':rest' => $data['id_restriction'], 
                ':access' => $data['id_accessibilite'], ':cond' => $data['id_condition']
                ]
            );

            foreach ($data['prises'] as $prise) {
                Database::preparedQuery("INSERT INTO Possede (id_pdc_itinerance, id_type_prise, nbr_type_prise) VALUES (?, ?, ?)", 
                [$data['id_pdc_itinerance'], $prise['id_type_prise'], $prise['nbr']]);
            }

            foreach ($data['paiements'] as $paie) {
                Database::preparedQuery("INSERT INTO Avoir (id_pdc_itinerance, id_type_paiement, nbr_type_paiement) VALUES (?, ?, ?)", 
                [$data['id_pdc_itinerance'], $paie['id_type_paiement'], $paie['nbr']]);
            }

            $conn->commit();
            return true;
        } catch (Exception $e) {
            $conn->rollBack();
            error_log("Erreur ajout PDC: " . $e->getMessage());
            return false;
        }
    }

    public static function update(array $data) {
        try {
            $conn = Database::getConnection();
            $conn->beginTransaction();

            Database::preparedQuery(
                "UPDATE pdc SET puissance_nomiale=:puiss, gratuit=:grat, reservation=:res, charge_rapide=:rapide WHERE id_pdc_itinerance=:id", 
                [':puiss'=>$data['puissance'], ':grat'=>$data['gratuit'], ':res'=>$data['reservation'], ':rapide'=>$data['charge_rapide'], ':id'=>$data['id_pdc_itinerance']]
            );

            Database::preparedQuery("DELETE FROM Possede WHERE id_pdc_itinerance=?", [$data['id_pdc_itinerance']]);
            foreach ($data['prises'] as $prise) {
                Database::preparedQuery("INSERT INTO Possede (id_pdc_itinerance, id_type_prise, nbr_type_prise) VALUES (?, ?, ?)", 
                [$data['id_pdc_itinerance'], $prise['id_type_prise'], $prise['nbr']]);
            }

            $conn->commit();
            return true;
        } catch (Exception $e) {
            $conn->rollBack();
            return false;
        }
    }

    public static function delete(string $id) {
        try {
            $conn = Database::getConnection();
            $conn->beginTransaction();

            Database::preparedQuery("DELETE FROM Possede WHERE id_pdc_itinerance=?", [$id]);
            Database::preparedQuery("DELETE FROM Avoir WHERE id_pdc_itinerance=?", [$id]);
            Database::preparedQuery("DELETE FROM pdc WHERE id_pdc_itinerance=?", [$id]);

            $conn->commit();
            return true;
        } catch (Exception $e) {
            $conn->rollBack();
            return false;
        }
    }
}
?>