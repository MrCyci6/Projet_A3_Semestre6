<?php
    if (!isset($_GET['id'])) {
        sendData("{\"success\": false, \"message\": \"ID is missing\"}", 400);
        exit();
    }

    if (!isset($_POST['puissance_nomiale'])) {
        sendData("{\"success\": false, \"message\": \"Missing data\"}", 400);
        exit();
    }

    $data = [
        'id_pdc_itinerance' => (string) $_GET['id'],
        'puissance'         => (float)  $_POST['puissance_nomiale'],
        'gratuit'           => (int)    $_POST['gratuit'],
        'reservation'       => (int)    $_POST['reservation'],
        'charge_rapide'     => (int)    $_POST['charge_rapide'],
        'prises'            => isset($_POST['prises']) ? json_decode($_POST['prises'], true) : [],
        'paiements'         => isset($_POST['paiements']) ? json_decode($_POST['paiements'], true) : []
    ];

    if (!Pdc::update($data)) {
        sendError();
    }
    
    sendData("{\"success\": true, \"message\": \"PDC updated\"}", 200);
?>