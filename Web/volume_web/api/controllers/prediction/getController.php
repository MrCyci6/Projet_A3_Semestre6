<?php

    $ressource = array_shift($request);
    if(isset($ressource) && $ressource == "puissance_nominale") {
        $params = [
            'nbre_pdc' => (int)($_GET['nbre_pdc'] ?? 5),
            'nb_types_prise' => (int)($_GET['nb_types_prise'] ?? 1),
            'consolidated_latitude' => (float)($_GET['lat'] ?? 49.24),
            'consolidated_longitude' => (float)($_GET['long'] ?? 6.13),
            'charge_rapide' => (int)($_GET['charge_rapide'] ?? 1),
            'prise_type_combo_ccs' => (int)($_GET['combo'] ?? 1),
            'prise_type_2' => (int)($_GET['type2'] ?? 0),
            'prise_type_ef' => (int)($_GET['type_ef'] ?? 0),
            'prise_type_chademo' => (int)($_GET['chademo'] ?? 0),
            'prise_type_autre' => (int)($_GET['autre'] ?? 0),
            'gratuit' => (int)($_GET['gratuit'] ?? 0),
            'paiement_cb' => (int)($_GET['cb'] ?? 0),
            'ouvert_24_7' => (int)($_GET['h24'] ?? 1),
            'implantation_station' => $_GET['implantation'] ?? 'Parking privé à usage public',
            'condition_acces' => $_GET['acces'] ?? 'Accès libre',
        ];

        $cmd_args = [];
        foreach ($params as $key => $value) {
            $val = is_string($value) ? escapeshellarg($value) : $value;
            $cmd_args[] = "--$key $val";
        }

        $cmd = "python3 /var/www/scripts/predict_puis.py " . implode(" ", $cmd_args) . " 2>&1";

        $output = shell_exec($cmd);

        sendData("{\"success\": true, \"data\": \"".trim($output)."\"}", 200);

    } else if(isset($ressource) && $ressource == "implantation") {

        $params = [
            'puissance_nominale' => (float)($_GET['puissance'] ?? 22.0),
            'nbre_pdc' => (int)($_GET['nbre_pdc'] ?? 2),
            'nb_types_prise' => (int)($_GET['nb_types'] ?? 1),
            'charge_rapide' => (int)($_GET['rapide'] ?? 0),
            'ouvert_24_7' => (int)($_GET['h24'] ?? 1),
            'paiement_cb' => (int)($_GET['cb'] ?? 0),
            'paiement_acte' => (int)($_GET['acte'] ?? 0),
            'paiement_autre' => (int)($_GET['autre_paiement'] ?? 0),
            'gratuit' => (int)($_GET['gratuit'] ?? 0),
            'reservation' => (int)($_GET['res'] ?? 0),
            'cable_t2_attache' => (int)($_GET['cable_t2'] ?? 0),
            'station_deux_roues' => (int)($_GET['2roues'] ?? 0),
            'prise_type_ef' => (int)($_GET['ef'] ?? 0),
            'prise_type_2' => (int)($_GET['t2'] ?? 0),
            'prise_type_combo_ccs' => (int)($_GET['ccs'] ?? 0),
            'prise_type_chademo' => (int)($_GET['chademo'] ?? 0),
            'prise_type_autre' => (int)($_GET['autre_prise'] ?? 0),
            'condition_acces' => $_GET['acces'] ?? 'Accès libre',
            'raccordement' => $_GET['raccord'] ?? 'Direct',
            'accessibilite_pmr' => $_GET['pmr'] ?? 'Inconnu',
            'nom_operateur' => $_GET['operateur'] ?? 'Autre',
            'code_insee_commune' => $_GET['commune'] ?? '00000',
        ];

        $cmd_args = [];
        foreach ($params as $key => $value) {
            $val = is_string($value) ? escapeshellarg($value) : $value;
            $cmd_args[] = "--$key $val";
        }

        $cmd = "python3 /var/www/scripts/predict_impl.py " . implode(" ", $cmd_args) . " 2>&1";

        $json_output = shell_exec($cmd);

        sendData("{\"success\": true, \"data\": ".$json_output."}", 200);

    } else {
        sendData("{\"success\": false, \"message\": \"Ressource not found\"}", 404);
    }
?>