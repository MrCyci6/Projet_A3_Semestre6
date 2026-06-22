<?php

    function sendData($data, $code, $json = true) {
        $codes = [
            200 => 'HTTP/1.1 200 OK',
            201 => 'HTTP/1.1 201 Created',
            400 => 'HTTP/1.1 400 Bad Request',
            401 => 'HTTP/1.1 401 Unauthorized',
            403 => 'HTTP/1.1 403 Forbidden',
            404 => 'HTTP/1.1 404 Not Found',
            500 => 'HTTP/1.1 500 Internal Server Error',
            503 => 'HTTP/1.1 503 Service Unavailable'
        ];

        header(isset($codes[$code]) ? $codes[$code] : $codes["500"]);
        header('Content-Type: '.($json ? "application/json" : "text/plain").'; charset=utf-8');
        header('Cache-control: no-store, no-cache, must-revalidate');
        header('Pragma: no-cache');

        echo $data;
    }

    function sendError() {
        sendData("{\"success\": false, \"message\": \"Internal Server Error\"}", 500);
        exit();
    }

    function sendNotFound() {
        sendData("{\"success\": false, \"message\": \"Not Found\"}", 404);
        exit();
    }

?>