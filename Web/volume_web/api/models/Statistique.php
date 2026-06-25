<?php

class Statistique {

    public static function getStationStats(string $id_station) {
        try {
            $stats = [];

            $sqlTotal = "SELECT COUNT(*) AS total_pdc FROM pdc WHERE id_station_itinerance = ?";
            $stmtTotal = Database::preparedQuery($sqlTotal, [$id_station]);
            $stats['total_pdc'] = $stmtTotal ? (int)$stmtTotal->fetchColumn() : 0;

            $sqlPuis = "SELECT 
                            ROUND(AVG(puissance_nomiale), 2) AS puissance_moyenne_kw,
                            MAX(puissance_nomiale) AS puissance_max_kw
                        FROM pdc
                        WHERE id_station_itinerance = ?";
            $stmtPuis = Database::preparedQuery($sqlPuis, [$id_station]);
            $stats['puissances'] = $stmtPuis ? $stmtPuis->fetch(PDO::FETCH_ASSOC) : null;

            $sqlDetails = "SELECT 
                            SUM(CASE WHEN gratuit = 1 THEN 1 ELSE 0 END) AS pdc_gratuits,
                            SUM(CASE WHEN charge_rapide = 1 THEN 1 ELSE 0 END) AS pdc_rapides,
                            SUM(CASE WHEN reservation = 1 THEN 1 ELSE 0 END) AS pdc_reservables
                           FROM pdc
                           WHERE id_station_itinerance = ?";
            $stmtDetails = Database::preparedQuery($sqlDetails, [$id_station]);
            $details = $stmtDetails ? $stmtDetails->fetch(PDO::FETCH_ASSOC) : null;
            
            $stats['caracteristiques'] = [
                'gratuits' => isset($details['pdc_gratuits']) ? (int)$details['pdc_gratuits'] : 0,
                'rapides' => isset($details['pdc_rapides']) ? (int)$details['pdc_rapides'] : 0,
                'reservables' => isset($details['pdc_reservables']) ? (int)$details['pdc_reservables'] : 0
            ];

            return $stats;

        } catch (PDOException $exception) {
            error_log('Request error in Statistique: '.$exception->getMessage());
            return false;
        }
    }
}
?>
