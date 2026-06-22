
document.addEventListener("DOMContentLoaded", () => {
    initMap();
});

let map;
function initMap() {
    if (document.getElementById('map') && !map) {
        map = L.map('map').setView([46.603354, 1.888334], 6);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap'
        }).addTo(map);

    }
}
