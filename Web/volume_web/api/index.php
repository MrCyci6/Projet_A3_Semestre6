<?php

    require_once "./models/Database.php";
    require_once "./models/Pdc.php";
    require_once "./models/Station.php";
    require_once "./utils.php";

    if(!Database::getConnection()) {
        sendData("{\"success\": false, \"message\": \"Database error\"}", 503);
        exit();
    }

    $requestMethod = strtolower($_SERVER['REQUEST_METHOD']);
    $pathInfo = $_SERVER['PATH_INFO'] ?? '/';
    $request = ltrim($pathInfo, '/');
    $request = explode('/', $request);
    $ressource = array_shift($request);
    
    $routes = [
        "pdc" => "controllers/pdc/".$requestMethod."Controller.php",
        "station" => "controllers/station/".$requestMethod."Controller.php"
    ];
    
    if(isset($routes[$ressource])) {
        if($requestMethod == "put") {
            parse_str(file_get_contents('php://input'), $_PUT);
        }
        
        require $routes[$ressource];
    } else {
        if($ressource == "") {
            sendData("{\"success\": true, \"message\": \"Welcome to BorneToBeAlive-API\", \"version\": \"1.0.0\"}", 200);
            exit();
        }

        sendData("{\"success\": false, \"message\": \"Ressource not found\"}", 404);
        exit();    
    }
?>