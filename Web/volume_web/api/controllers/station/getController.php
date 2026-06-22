<?php

    if(isset($_GET['id'])) {
        $id = (string) $_GET['id'];

        $data = Station::get($id);
        if(!is_array($data) && !$data) {
            sendNotFound();
        }

        sendData("{\"success\": true, \"data\": ".json_encode($data)."}", 200);

        exit();
    } else if(isset($_GET['zoom'], $_GET['lat_min'], $_GET['lat_max'], $_GET['lng_min'], $_GET['lng_max'])) {

        $zoom = (int) $_GET['zoom'];
        $lat_min = (float) $_GET['lat_min'];
        $lat_max = (float) $_GET['lat_max'];
        $lng_min = (float) $_GET['lng_min'];
        $lng_max = (float) $_GET['lng_max'];

        $ZOOM_THRESHOLD = 10;

        if ($zoom < $ZOOM_THRESHOLD) {
            $data = Station::getByCluster($lat_min, $lat_max, $lng_min, $lng_max);
        } else {
            $data = Station::getByBoundingBox($lat_min, $lat_max, $lng_min, $lng_max);
        }

        if(!is_array($data) && !$data) {
            sendError();
        }

        sendData(json_encode(["success" => true, "data" => $data]), 200);
        exit();
    }


    $rows = (int) ($_GET['rows'] ?? DEFAULT_ROWS);
    $page = (int) ($_GET['page'] ?? 1);
    $query = $_GET['query'] ?? "";

    $filters = [
        'ouvert_24_7'         => isset($_GET['h24']) ? (int) $_GET['h24'] : null,
        'id_enseigne'         => isset($_GET['enseigne']) ? (int) $_GET['enseigne'] : null,
        'id_operateur'        => isset($_GET['operateur']) ? (int) $_GET['operateur'] : null,
    ];

    $data = Station::search($query, $filters, $page, $rows);
    if(!is_array($data) && !$data) {
        sendError();
    }

    sendData("{\"success\": true, \"data\": ".json_encode($data)."}", 200);
?>