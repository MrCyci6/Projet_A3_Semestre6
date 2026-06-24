document.addEventListener("DOMContentLoaded", () => {
    initMap();
});

let map;
let mapCluster;

// Références pour stocker les marqueurs afin de pouvoir les effacer lors de la mise à jour
let markersData = {
    main: [],
    cluster: []
};

function initMap() {
    // Initialisation de la carte principale
    if (document.getElementById('map') && !map) {
        map = L.map('map').setView([46.603354, 1.888334], 6);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap'
        }).addTo(map);

        // Mettre à jour la carte principale lors du déplacement
        map.on('moveend', () => loadMapData(map, markersData.main));
        // Premier chargement immédiat
        loadMapData(map, markersData.main);
    }

    // Initialisation anticipée de la carte des clusters
    if (document.getElementById('map-cluster') && !mapCluster) {
        mapCluster = L.map('map-cluster').setView([46.603354, 1.888334], 6);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap'
        }).addTo(mapCluster);

        // Mettre à jour les données de la carte cluster lors du déplacement
        mapCluster.on('moveend', () => loadMapData(mapCluster, markersData.cluster));
    }
}

async function loadMapData(targetMap, markersArray) {
    if (!targetMap) return;

    const bounds = targetMap.getBounds();
    const zoom = targetMap.getZoom();
    const lat_min = bounds.getSouth();
    const lat_max = bounds.getNorth();
    const lng_min = bounds.getWest();
    const lng_max = bounds.getEast();

    try {
        // Chemin absolu à partir de la racine du serveur web
        const url = `/api/index.php/station?zoom=${zoom}&lat_min=${lat_min}&lat_max=${lat_max}&lng_min=${lng_min}&lng_max=${lng_max}`;
        const response = await fetch(url);

        if (!response.ok) throw new Error("Erreur serveur API: " + response.status);
        const result = await response.json();

        if (result.success && result.data) {
            // Retirer les anciens marqueurs
            markersArray.forEach(marker => targetMap.removeLayer(marker));
            markersArray.length = 0; // Vider le tableau

            result.data.forEach(item => {
                const lat = item.latitude || item.lat;
                const lng = item.longitude || item.lng;
                
                let popupText = "";
                if (item.count) {
                    popupText = `<b>Zone de regroupement</b><br>${item.count} stations ici`;
                } else {
                    popupText = `<b>${item.nom || item.station_nom}</b><br>Ouvert 24/7 : ${item.ouvert_24_7 ? 'Oui' : 'Non'}`;
                }

                const marker = L.marker([lat, lng])
                    .bindPopup(popupText)
                    .addTo(targetMap);

                markersArray.push(marker);
            });
        }
    } catch (error) {
        console.error("Erreur de récupération :", error);
        alert("Impossible de charger la carte. Assurez-vous d'avoir bien ouvert la page via le serveur Docker (http://localhost:8080/visualisation.html) et que vos fichiers sont dans le bon dossier.");
    }
}

// Fonction pour récupérer les données du tableau
async function loadTableData() {
    try {
        const url = `/api/index.php/station?page=1&rows=10`;
        const response = await fetch(url);
        if (!response.ok) throw new Error("Erreur API tableau");
        
        const result = await response.json();
        if (result.success && result.data) {
            const tbody = document.getElementById('station-table-body');
            if (!tbody) return;
            tbody.innerHTML = ''; // Nettoyer
            
            result.data.forEach(station => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><input type="radio" name="stationSelection" value="${station.id_station_itinerance}" class="form-check-input"></td>
                    <td>${station.adresse || 'N/A'}</td>
                    <td>${station.station_nom || 'N/A'}</td>
                    <td>${station.enseigne_nom || 'N/A'}</td>
                    <td>${station.implantation || 'N/A'}</td>
                    <td>${station.horaires || 'N/A'}</td>
                    <td>${station.ouvert_24_7 == 1 ? 'Oui' : 'Non'}</td>
                    <td>${station.operateur_nom || 'N/A'}</td>
                `;
                tbody.appendChild(tr);
            });
        }
    } catch (error) {
        console.error("Erreur tableau :", error);
    }
}

// Charger le tableau au démarrage
document.addEventListener("DOMContentLoaded", () => {
    loadTableData();
});

document.addEventListener('shown.bs.modal', function (event) {
    if (event.target.id === 'modalCluster') {
        if (mapCluster) {
            mapCluster.invalidateSize();
            loadMapData(mapCluster, markersData.cluster);
        }
    }
});
