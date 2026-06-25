<?php

    if(!isset($_GET['id'])) {
        sendData(json_encode(["success" => false, "message" => "Missing station ID"]), 400);
    }

    $id_station = (string) $_GET['id'];

    $data = Statistique::getStationStats($id_station);
    if($data === false) {
        sendError();
    }

    sendData(json_encode(["success" => true, "data" => $data]), 200);
?>
