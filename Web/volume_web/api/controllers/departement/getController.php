<?php
    $data = Departement::getAll();
    if(!is_array($data) && !$data) {
        sendError();
    }

    sendData(json_encode(["success" => true, "data" => $data]), 200);
?>
