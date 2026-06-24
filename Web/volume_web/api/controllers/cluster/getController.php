<?php
    $output_dir = "/var/www/html/scripts/outputs";
    $script_path = "/var/www/html/scripts/clustering.py";

    shell_exec("python3 $script_path 2>&1");

    $img1 = "/outputs/metriques_clustering.png";
    $img2 = "/outputs/carte_clustering.png";

    if (file_exists($output_dir . "/metriques_clustering.png")) {
        sendData(json_encode([
            "success" => true,
            "images" => [
                "metriques" => $img1,
                "carte" => $img2
            ]
        ]), 200);
    } else {
        sendError("Erreur lors de la génération des graphiques", 500);
    }
?>