<?php

    if (!isset($_GET['id'])) {
        sendData("{\"success\": false, \"message\": \"ID is missing\"}", 400);
    }

    if (!Pdc::delete($_GET['id']))
        sendError();
    
    sendData("{\"success\": false, \"message\": \"PDC deleted\"}", 200);

?>