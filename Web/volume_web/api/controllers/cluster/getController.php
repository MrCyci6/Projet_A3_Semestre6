<?php
    $output_dir = "/var/www/clenoi28/outputs";
    $script_path = "/var/www/clenoi28/scripts/clustering.py";

    #shell_exec("cd /var/www/clenoi28 && python3 $script_path 2>&1");

    sendData(json_encode([
        "success" => true,
        "image" => "/images/carte_clustering.png"
    ]), 200);
?>