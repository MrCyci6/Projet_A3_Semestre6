<?php

    if(isset($_GET['id'])) {
        $id = (string) $_GET['id'];

        $data = Pdc::get($id);
        if(!is_array($data) && !$data) {
            sendNotFound();
        }

        sendData("{\"success\": true, \"data\": ".json_encode($data)."}", 200);

        exit();
    }

    $rows = (int) ($_GET['rows'] ?? DEFAULT_ROWS);
    $page = (int) ($_GET['page'] ?? 1);
    $query = $_GET['query'] ?? "";

    $filters = [
        'charge_rapide'       => isset($_GET['charge_rapide']) ? (int) $_GET['charge_rapide'] : null,
        'prises'              => isset($_GET['prises']) ? explode(',', $_GET['prises']) : null,
        'paiement'            => isset($_GET['paiement']) ? explode(',', $_GET['paiement']) : null,
        'ouvert_24_7'         => isset($_GET['h24']) ? (int) $_GET['h24'] : null,
        'reservation'         => isset($_GET['reservation']) ? (int) $_GET['reservation'] : null,
        'accessibilite_pmr'   => isset($_GET['pmr']) ? $_GET['pmr'] : null,
        'condition_access'    => isset($_GET['acces']) ? $_GET['acces'] : null,
        'restriction_gabarit' => isset($_GET['gabarit']) ? $_GET['gabarit'] : null,
        'id_enseigne'         => isset($_GET['enseigne']) ? (int) $_GET['enseigne'] : null,
        'id_operateur'        => isset($_GET['operateur']) ? (int) $_GET['operateur'] : null,
    ];

    $data = Pdc::search($query, $filters, $page, $rows);
    if(!is_array($data) && !$data) {
        sendError();
    }

    sendData("{\"success\": true, \"data\": ".json_encode($data)."}", 200);
?>