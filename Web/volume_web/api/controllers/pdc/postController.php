<?php
    if (!isset($_POST['id_pdc_itinerance'], $_POST['puissance_nomiale'], $_POST['id_station_itinerance'])) {
        sendData("{\"success\": false, \"message\": \"Missing required fields\"}", 400);
    }

    $data = [
        'id_pdc_itinerance'     => (string) $_POST['id_pdc_itinerance'],
        'puissance'             => (float)  $_POST['puissance_nomiale'],
        'gratuit'               => (int)    $_POST['gratuit'],
        'tarification'          => (string) $_POST['tarification'],
        'reservation'           => (int)    $_POST['reservation'],
        'deux_roues'            => (int)    $_POST['station_deux_roues'],
        'num_pdl'               => (string) $_POST['num_pdl'],
        'date_service'          => (string) $_POST['date_mise_en_service'],
        'obs'                   => (string) $_POST['observations'],
        'charge_rapide'         => (int)    $_POST['charge_rapide'],
        'nbr_pdc'               => (int)    $_POST['nbr_pdc'],
        'id_station'            => (string) $_POST['id_station_itinerance'],
        'id_raccordement'       => (int)    $_POST['id_raccordement'],
        'id_restriction'        => (int)    $_POST['id_restriction'],
        'id_accessibilite'      => (int)    $_POST['id_accessibilite'],
        'id_condition'          => (int)    $_POST['id_condition'],
        'prises'                => isset($_POST['prises']) ? json_decode($_POST['prises'], true) : [],
        'paiements'             => isset($_POST['paiements']) ? json_decode($_POST['paiements'], true) : []
    ];

    if (!Pdc::add($data)) {
        sendError();
    }
    
    sendData("{\"success\": true, \"message\": \"PDC created\"}", 201);

?>