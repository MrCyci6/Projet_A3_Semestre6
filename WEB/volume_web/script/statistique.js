'use strict';

// Fallback pour httpErrors s'il n'est pas défini globalement
if (typeof httpErrors === 'undefined') {
    window.httpErrors = function(status) {
        console.error("Erreur HTTP : " + status);
        alert("Une erreur de communication est survenue avec le serveur (code " + status + ").");
    };
}

let tableState = {
    page: 1,
    rows: 10,
    query: "",
    h24: "",
    enseigne: "",
    operateur: "",
    departement: ""
};

let selectedStationId = null;
let filterTimeout = null;

function triggerTableReload() {
    clearTimeout(filterTimeout);
    filterTimeout = setTimeout(() => {
        tableState.page = 1;
        loadTableData();
    }, 300);
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

    const url = `/api/index.php/station?${params.toString()}`;
    ajaxRequest('GET', url, (result) => {
        if (result.success && result.data) {
            const tbody = document.getElementById('station-table-body');
            if (!tbody) return;
            tbody.innerHTML = '';
            
            result.data.forEach(station => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><input type="radio" name="stationSelection" value="${station.id_station_itinerance}" class="form-check-input" ${selectedStationId === station.id_station_itinerance ? 'checked' : ''}></td>
                    <td>${station.adresse || 'N/A'}</td>
                    <td>${station.station_nom || 'N/A'}</td>
                    <td>${station.enseigne_nom || 'N/A'}</td>
                    <td>${station.implantation_nom || station.implantation || 'N/A'}</td>
                    <td>${station.horaires || 'N/A'}</td>
                    <td>${station.ouvert_24_7 == 1 ? 'Oui' : 'Non'}</td>
                    <td>${station.operateur_nom || 'N/A'}</td>
                `;
                tbody.appendChild(tr);
            });

            const prevBtn = document.getElementById("btn-page-prev");
            const nextBtn = document.getElementById("btn-page-next");
            const pageNumSpan = document.getElementById("current-page-num");

            if (pageNumSpan) pageNumSpan.innerText = tableState.page;
            if (prevBtn) prevBtn.disabled = (tableState.page === 1);
            if (nextBtn) nextBtn.disabled = (result.data.length < tableState.rows);
        }
    });
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

    document.addEventListener("change", (event) => {
        if (event.target && event.target.name === "stationSelection") {
            selectedStationId = event.target.value;
        }
    });

    const btnCalcStats = document.getElementById("btn-calc-stats");
    if (btnCalcStats) {
        btnCalcStats.addEventListener("click", () => {
            const statsOutput = document.getElementById("stats-output");
            const graphOutput = document.getElementById("graph-output");
            if (!statsOutput) return;

            if (!selectedStationId) {
                statsOutput.innerHTML = `<div class="alert alert-warning">Veuillez selectionner une station dans le tableau pour afficher ses statistiques.</div>`;
                if (graphOutput) graphOutput.innerHTML = "";
                return;
            }

            statsOutput.innerHTML = `<div class="alert alert-info">Chargement des statistiques...</div>`;
            if (graphOutput) graphOutput.innerHTML = "";

            const url = `/api/index.php/statistique?id=${encodeURIComponent(selectedStationId)}`;
            ajaxRequest('GET', url, (result) => {
                if (result.success && result.data) {
                    const data = result.data;
                    
                    let htmlStats = `
                        <div class="row g-3">
                            <div class="col-md-6 col-lg-3">
                                <div class="p-3 bg-light rounded border text-center">
                                    <div class="text-muted small fw-bold text-uppercase">Points de charge</div>
                                    <div class="display-6 fw-bold text-success my-2">${data.total_pdc}</div>
                                    <div class="small text-secondary">PDC physiques connectes</div>
                                </div>
                            </div>
                            <div class="col-md-6 col-lg-3">
                                <div class="p-3 bg-light rounded border text-center">
                                    <div class="text-muted small fw-bold text-uppercase">Puissance max</div>
                                    <div class="display-6 fw-bold text-warning my-2">${data.puissances && data.puissances.puissance_max_kw ? data.puissances.puissance_max_kw : 0} kW</div>
                                    <div class="small text-secondary">Puissance moyenne : ${data.puissances && data.puissances.puissance_moyenne_kw ? data.puissances.puissance_moyenne_kw : 0} kW</div>
                                </div>
                            </div>
                            <div class="col-md-6 col-lg-3">
                                <div class="p-3 bg-light rounded border text-center">
                                    <div class="text-muted small fw-bold text-uppercase">Gratuite</div>
                                    <div class="display-6 fw-bold text-primary my-2">${data.caracteristiques.gratuits}</div>
                                    <div class="small text-secondary">PDC gratuits sur la station</div>
                                </div>
                            </div>
                            <div class="col-md-6 col-lg-3">
                                <div class="p-3 bg-light rounded border text-center">
                                    <div class="text-muted small fw-bold text-uppercase">Reservables</div>
                                    <div class="display-6 fw-bold text-info my-2">${data.caracteristiques.reservables}</div>
                                    <div class="small text-secondary">PDC avec option de reservation</div>
                                </div>
                            </div>
                        </div>
                    `;
                    
                    statsOutput.innerHTML = htmlStats;

                } else {
                    statsOutput.innerHTML = `<div class="alert alert-danger">Impossible de recuperer les statistiques de cette station.</div>`;
                }
            });
        });
    }
});
