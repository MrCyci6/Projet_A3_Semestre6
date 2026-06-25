let map;
let mapCluster;
let selectedStationId = null;
let markersData = {
    main: [],
    cluster: []
};
let tableState = {
    page: 1,
    rows: 10,
    query: "",
    h24: "",
    enseigne: "",
    operateur: "",
    departement: ""
};
let filterTimeout = null;


function initMap() {
    if (document.getElementById('map') && !map) {
        map = L.map('map').setView([46.603354, 1.888334], 6);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap'
        }).addTo(map);

        map.on('moveend', () => loadMapData(map, markersData.main));
        loadMapData(map, markersData.main);
    }

    if (document.getElementById('map-cluster') && !mapCluster) {
        mapCluster = L.map('map-cluster').setView([46.603354, 1.888334], 6);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap'
        }).addTo(mapCluster);

        mapCluster.on('moveend', () => loadMapData(mapCluster, markersData.cluster));
    }
}

function loadMapData(targetMap, markersArray) {
    if (!targetMap) return;

    const bounds = targetMap.getBounds();
    const zoom = targetMap.getZoom();
    const lat_min = bounds.getSouth();
    const lat_max = bounds.getNorth();
    const lng_min = bounds.getWest();
    const lng_max = bounds.getEast();

    const url = `/api/index.php/station?zoom=${zoom}&lat_min=${lat_min}&lat_max=${lat_max}&lng_min=${lng_min}&lng_max=${lng_max}`;
    ajaxRequest('GET', url, (result) => {
        if (result.success && result.data) {
            markersArray.forEach(marker => targetMap.removeLayer(marker));
            markersArray.length = 0;

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
    });
}

function loadTableData() {
    const params = new URLSearchParams();
    params.append("page", tableState.page);
    params.append("rows", tableState.rows);
    if (tableState.query) params.append("query", tableState.query);
    if (tableState.h24 !== "") params.append("h24", tableState.h24);
    if (tableState.enseigne) params.append("enseigne", tableState.enseigne);
    if (tableState.operateur) params.append("operateur", tableState.operateur);
    if (tableState.departement) params.append("departement", tableState.departement);

    const url = `/api/index.php/pdc?${params.toString()}`;
    ajaxRequest('GET', url, (result) => {
        if (result.success && result.data) {
            const tbody = document.getElementById('station-table-body');
            if (!tbody) return;
            tbody.innerHTML = ''; // Nettoyer
            
            result.data.forEach(pdc => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><input type="radio" name="stationSelection" value="${pdc.id_pdc_itinerance}" class="form-check-input" ${selectedStationId === pdc.id_pdc_itinerance ? 'checked' : ''}></td>
                    <td>${pdc.id_pdc_itinerance || 'N/A'}</td>
                    <td>${pdc.station_nom || 'N/A'}</td>
                    <td>${pdc.adresse || 'N/A'}</td>
                    <td>${pdc.puissance_nomiale || pdc.puissance_nominale || 'N/A'}</td>
                    <td>${pdc.gratuit == 1 ? 'Oui' : 'Non'}</td>
                    <td>${pdc.reservation == 1 ? 'Oui' : 'Non'}</td>
                    <td>${pdc.enseigne_nom || 'N/A'}</td>
                    <td>${pdc.operateur_nom || 'N/A'}</td>
                `;
                tbody.appendChild(tr);
            });

            // Mettre à jour les boutons de pagination
            const prevBtn = document.getElementById("btn-page-prev");
            const nextBtn = document.getElementById("btn-page-next");
            const pageNumSpan = document.getElementById("current-page-num");

            if (pageNumSpan) pageNumSpan.innerText = tableState.page;
            if (prevBtn) prevBtn.disabled = (tableState.page === 1);
            if (nextBtn) nextBtn.disabled = (result.data.length < tableState.rows);
        }
    });
}

function triggerTableReload() {
    clearTimeout(filterTimeout);
    filterTimeout = setTimeout(() => {
        tableState.page = 1;
        loadTableData();
    }, 300);
}

function loadDepartements() {
    ajaxRequest('GET', "/api/index.php/departement", (result) => {
        if (result.success && result.data) {
            const select = document.getElementById("filter-departement");
            if (!select) return;
            
            result.data.forEach(dep => {
                const opt = document.createElement("option");
                opt.value = dep.id_departement;
                opt.textContent = `${dep.id_departement} - ${dep.denomination}`;
                select.appendChild(opt);
            });
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    initMap();

    loadTableData();
    loadDepartements();

    const filterQuery = document.getElementById("filter-query");
    if (filterQuery) {
        filterQuery.addEventListener("input", () => {
            tableState.query = filterQuery.value;
            triggerTableReload();
        });
    }

    const filterDepartement = document.getElementById("filter-departement");
    if (filterDepartement) {
        filterDepartement.addEventListener("change", () => {
            tableState.departement = filterDepartement.value;
            triggerTableReload();
        });
    }

    const filterH24 = document.getElementById("filter-h24");
    if (filterH24) {
        filterH24.addEventListener("change", () => {
            tableState.h24 = filterH24.value;
            triggerTableReload();
        });
    }

    const filterEnseigne = document.getElementById("filter-enseigne");
    if (filterEnseigne) {
        filterEnseigne.addEventListener("input", () => {
            tableState.enseigne = filterEnseigne.value;
            triggerTableReload();
        });
    }

    const filterOperateur = document.getElementById("filter-operateur");
    if (filterOperateur) {
        filterOperateur.addEventListener("input", () => {
            tableState.operateur = filterOperateur.value;
            triggerTableReload();
        });
    }

    const filterRows = document.getElementById("filter-rows");
    if (filterRows) {
        filterRows.addEventListener("change", () => {
            tableState.rows = parseInt(filterRows.value);
            triggerTableReload();
        });
    }

    const btnPrev = document.getElementById("btn-page-prev");
    if (btnPrev) {
        btnPrev.addEventListener("click", () => {
            if (tableState.page > 1) {
                tableState.page--;
                loadTableData();
            }
        });
    }

    const btnNext = document.getElementById("btn-page-next");
    if (btnNext) {
        btnNext.addEventListener("click", () => {
            tableState.page++;
            loadTableData();
        });
    }
});

document.addEventListener('shown.bs.modal', function (event) {
    if (event.target.id === 'modalCluster') {
        if (mapCluster) {
            mapCluster.invalidateSize();
            loadMapData(mapCluster, markersData.cluster);
        }
    }
});

document.addEventListener("change", (event) => {
    if (event.target && event.target.name === "stationSelection") {
        selectedStationId = event.target.value;
        document.querySelectorAll(".btn-fill-station").forEach(btn => {
            btn.disabled = false;
        });
    }
});

document.addEventListener("click", (event) => {
    if (event.target && event.target.classList.contains("btn-fill-station")) {
        if (!selectedStationId) return;
        
        event.target.innerHTML = "Chargement...";
        const url = `/api/index.php/pdc?id=${selectedStationId}`;
        ajaxRequest('GET', url, (result) => {
            if (result.success && result.data) {
                const station = result.data;
                
                const formType = document.getElementById("form-predict-type");
                if (formType && formType.contains(event.target)) {
                    formType.querySelector("[name='puissance']").value = parseFloat(station.puissance_nomiale) || parseFloat(station.puissance_nominale) || 22.0; 
                    formType.querySelector("[name='nbre_pdc']").value = parseInt(station.nbr_pdc) || 1;
                    
                    formType.querySelector("[name='acces']").value = station.condition_access_nom || (station.ouvert_24_7 == 1 ? "Accès libre" : "Accès réservé");
                    formType.querySelector("[name='pmr']").value = station.accessibilite_pmr_nom || "Inconnu";
                    formType.querySelector("[name='raccord']").value = station.raccordement_nom || "Direct";
                    
                    formType.querySelector("[name='operateur']").value = station.operateur_nom || "Autre";
                    formType.querySelector("[name='commune']").value = station.code_postal ? station.code_postal.substring(0, 5) : "00000";
                    
                    formType.querySelector("#type-h24").checked = (station.ouvert_24_7 == 1);
                    formType.querySelector("#type-cb").checked = false; // Note: You would need to join the payment types if you want to set this accurately.
                    formType.querySelector("#type-acte").checked = true;
                    formType.querySelector("#type-gratuit").checked = (station.gratuit == 1);
                    formType.querySelector("#type-rapide").checked = (station.charge_rapide == 1);
                }
                
                const formPuis = document.getElementById("form-predict-puissance");
                if (formPuis && formPuis.contains(event.target)) {
                    formPuis.querySelector("[name='nbre_pdc']").value = parseInt(station.nbr_pdc) || 1;
                    formPuis.querySelector("[name='lat']").value = parseFloat(station.latitude) || 49.24;
                    formPuis.querySelector("[name='long']").value = parseFloat(station.longitude) || 6.13;
                    
                    formPuis.querySelector("[name='acces']").value = station.condition_access_nom || (station.ouvert_24_7 == 1 ? "Accès libre" : "Accès réservé");
                    formPuis.querySelector("[name='implantation']").value = station.implantation_nom || "Parking public";
                    
                    formPuis.querySelector("#puis-h24").checked = (station.ouvert_24_7 == 1);
                    formPuis.querySelector("#puis-gratuit").checked = (station.gratuit == 1);
                    formPuis.querySelector("#puis-rapide").checked = (station.charge_rapide == 1);
                }
                
                event.target.innerHTML = "Prérempli avec succès !";
                setTimeout(() => {
                    event.target.innerHTML = "Préremplir avec la station sélectionnée";
                }, 2000);
            }
        });
    }
});

document.addEventListener("submit", (event) => {
    if (event.target && event.target.id === "form-predict-type") {
        event.preventDefault();
        const form = event.target;
        const submitBtn = form.querySelector("button[type='submit']");
        const originalText = submitBtn.innerHTML;
        
        submitBtn.disabled = true;
        submitBtn.innerHTML = "Calcul en cours...";
        
        const params = new URLSearchParams();
        params.append("puissance", form.querySelector("[name='puissance']").value);
        params.append("nbre_pdc", form.querySelector("[name='nbre_pdc']").value);
        params.append("nb_types", form.querySelector("[name='nb_types']").value);
        
        params.append("acces", form.querySelector("[name='acces']").value);
        params.append("raccord", form.querySelector("[name='raccord']").value);
        params.append("pmr", form.querySelector("[name='pmr']").value);
        params.append("operateur", form.querySelector("[name='operateur']").value);
        params.append("commune", form.querySelector("[name='commune']").value);
        
        params.append("rapide", form.querySelector("[name='rapide']").checked ? 1 : 0);
        params.append("h24", form.querySelector("[name='h24']").checked ? 1 : 0);
        params.append("cb", form.querySelector("[name='cb']").checked ? 1 : 0);
        params.append("acte", form.querySelector("[name='acte']").checked ? 1 : 0);
        params.append("autre_paiement", form.querySelector("[name='autre_paiement']").checked ? 1 : 0);
        params.append("gratuit", form.querySelector("[name='gratuit']").checked ? 1 : 0);
        params.append("res", form.querySelector("[name='res']").checked ? 1 : 0);
        params.append("cable_t2", form.querySelector("[name='cable_t2']").checked ? 1 : 0);
        params.append("2roues", form.querySelector("[name='2roues']").checked ? 1 : 0);
        
        params.append("ef", form.querySelector("[name='ef']").checked ? 1 : 0);
        params.append("t2", form.querySelector("[name='t2']").checked ? 1 : 0);
        params.append("ccs", form.querySelector("[name='ccs']").checked ? 1 : 0);
        params.append("chademo", form.querySelector("[name='chademo']").checked ? 1 : 0);
        params.append("autre_prise", form.querySelector("[name='autre_prise']").checked ? 1 : 0);
        
        ajaxRequest('GET', `/api/index.php/prediction/implantation?${params.toString()}`, (result) => {
            const resultDiv = document.getElementById("result-predict-type");
            const resultText = document.getElementById("result-type-content");
            const resultProb = document.getElementById("result-type-prob");
            
            if (result.success && result.data) {
                resultDiv.classList.remove("d-none");
                
                resultText.innerHTML = `<strong>Type prédit :</strong> <span class="badge bg-success p-2 fs-6 mt-1">${result.data.prediction}</span>`;
                
                resultProb.innerHTML = "";
                if (result.data.probabilites) {
                    Object.entries(result.data.probabilites).forEach(([classe, prob]) => {
                        const percent = (prob * 100).toFixed(1);
                        const progressCol = document.createElement("div");
                        progressCol.className = "col-md-6 mb-2";
                        progressCol.innerHTML = `
                            <div class="small fw-bold text-secondary mb-1">${classe} (${percent}%)</div>
                            <div class="progress" style="height: 10px;">
                                <div class="progress-bar bg-success" role="progressbar" style="width: ${percent}%" aria-valuenow="${percent}" aria-valuemin="0" aria-valuemax="100"></div>
                            </div>
                        `;
                        resultProb.appendChild(progressCol);
                    });
                }
            } else {
                alert("La prédiction a échoué.");
            }
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        });
    }
});

document.addEventListener("submit", (event) => {
    if (event.target && event.target.id === "form-predict-puissance") {
        event.preventDefault();
        const form = event.target;
        const submitBtn = form.querySelector("button[type='submit']");
        const originalText = submitBtn.innerHTML;
        
        submitBtn.disabled = true;
        submitBtn.innerHTML = "Calcul en cours...";
        
        const params = new URLSearchParams();
        params.append("nbre_pdc", form.querySelector("[name='nbre_pdc']").value);
        params.append("nb_types_prise", form.querySelector("[name='nb_types_prise']").value);
        params.append("lat", form.querySelector("[name='lat']").value);
        params.append("long", form.querySelector("[name='long']").value);
        
        params.append("implantation", form.querySelector("[name='implantation']").value);
        params.append("acces", form.querySelector("[name='acces']").value);
        
        params.append("charge_rapide", form.querySelector("[name='charge_rapide']").checked ? 1 : 0);
        params.append("h24", form.querySelector("[name='ouvert_24_7']").checked ? 1 : 0);
        params.append("gratuit", form.querySelector("[name='gratuit']").checked ? 1 : 0);
        params.append("cb", form.querySelector("[name='cb']").checked ? 1 : 0);
        
        params.append("combo", form.querySelector("[name='combo']").checked ? 1 : 0);
        params.append("type2", form.querySelector("[name='type2']").checked ? 1 : 0);
        params.append("type_ef", form.querySelector("[name='type_ef']").checked ? 1 : 0);
        params.append("chademo", form.querySelector("[name='chademo']").checked ? 1 : 0);
        params.append("autre", form.querySelector("[name='autre']").checked ? 1 : 0);
        
        ajaxRequest('GET', `/api/index.php/prediction/puissance_nominale?${params.toString()}`, (result) => {
            const resultDiv = document.getElementById("result-predict-puissance");
            const resultText = document.getElementById("result-puissance-content");
            
            if (result.success && result.data) {
                resultDiv.classList.remove("d-none");
                
                resultText.innerHTML = `<span class="badge bg-warning text-dark p-3 fs-5">${result.data}</span>`;
            } else {
                alert("La prédiction de puissance a échoué.");
            }
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        });
    }
});

const btnRunClustering = document.getElementById("btn-run-clustering");
if (btnRunClustering) {
    btnRunClustering.addEventListener("click", () => {
        const originalText = btnRunClustering.innerHTML;
        btnRunClustering.disabled = true;
        btnRunClustering.innerHTML = "Analyse K-Means en cours...";
        
        ajaxRequest('GET', "/api/index.php/cluster", (result) => {
            if (result.success && result.images) {
                const resultsDiv = document.getElementById("cluster-analysis-results");
                const imgMetrics = document.getElementById("img-cluster-metrics");
                const imgMap = document.getElementById("img-cluster-map");
                
                if (resultsDiv && imgMetrics && imgMap) {
                    const t = new Date().getTime();
                    imgMetrics.src = `${result.images.metriques}?t=${t}`;
                    imgMap.src = `${result.images.carte}?t=${t}`;
                    
                    resultsDiv.classList.remove("d-none");
                }
                btnRunClustering.innerHTML = "Analyse terminée !";
                setTimeout(() => {
                    btnRunClustering.innerHTML = originalText;
                    btnRunClustering.disabled = false;
                }, 2000);
            } else {
                const msg = result.message || "Erreur serveur";
                alert("Échec de l'analyse : " + msg);
                btnRunClustering.disabled = false;
                btnRunClustering.innerHTML = originalText;
            }
        });
    });
}
