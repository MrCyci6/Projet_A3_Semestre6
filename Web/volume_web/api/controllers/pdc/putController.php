<?php

    if (!isset($_GET['id'])) {
        sendData("{\"success\": false, \"message\": \"ID is missing\"}", 400);
        exit();
    }

    if (!isset($_PUT['puissance_nomiale'])) {
        sendData("{\"success\": false, \"message\": \"Missing data\"}", 400);
        exit();
    }

    $data = [
        'id_pdc_itinerance' => (string) $_GET['id'],
        'puissance'         => (float)  $_PUT['puissance_nomiale'],
        'gratuit'           => (int)    $_PUT['gratuit'],
        'reservation'       => (int)    $_PUT['reservation'],
        'charge_rapide'     => (int)    $_PUT['charge_rapide'],
        'prises'            => isset($_PUT['prises']) ? json_decode($_PUT['prises'], true) : [],
        'paiements'         => isset($_PUT['paiements']) ? json_decode($_PUT['paiements'], true) : []
    ];

    if (!Pdc::update($data)) {
        sendError();
    }
    
    sendData("{\"success\": true, \"message\": \"PDC updated\"}", 200);
?>