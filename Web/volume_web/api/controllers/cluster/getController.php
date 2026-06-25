<?php
    $output_dir = "/var/www/html/outputs";
    $script_path = "/var/www/scripts/clustering.py";

    shell_exec("cd /var/www/html && python3 $script_path 2>&1");

    sendData(json_encode([
        "success" => true,
        "image" => "http://localhost:8080/images/carte_clustering.png"
    ]), 200);
?>