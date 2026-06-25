// Fallback pour httpErrors s'il n'est pas défini globalement
if (typeof httpErrors === 'undefined') {
    window.httpErrors = function(status) {
        console.error("Erreur HTTP : " + status);
        const alertBox = document.getElementById("admin-alert");
        if (alertBox) {
            alertBox.classList.remove("d-none");
            alertBox.classList.remove("alert-success");
            alertBox.classList.add("alert-danger");
            alertBox.innerText = "Une erreur de communication est survenue avec le serveur (code " + status + ").";
        }
        const btnSubmit = document.getElementById("btn-submit-pdc");
        if (btnSubmit) {
            btnSubmit.disabled = false;
            btnSubmit.innerHTML = "Créer le PDC";
        }
    };
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form-add-pdc");
    const btnSubmit = document.getElementById("btn-submit-pdc");
    const alertBox = document.getElementById("admin-alert");

    addPriseRow();
    addPaiementRow();

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        
        btnSubmit.disabled = true;
        btnSubmit.innerHTML = "Création en cours...";
        alertBox.classList.add("d-none");
        alertBox.classList.remove("alert-success", "alert-danger");

        const prises = [];
        document.querySelectorAll(".prise-row").forEach(row => {
            const idType = parseInt(row.querySelector(".sel-prise-type").value);
            const nbr = parseInt(row.querySelector(".inp-prise-nbr").value);
            if (idType > 0 && nbr > 0) {
                prises.push({ id_type_prise: idType, nbr: nbr });
            }
        });

        const paiements = [];
        document.querySelectorAll(".paiement-row").forEach(row => {
            const idType = parseInt(row.querySelector(".sel-paiement-type").value);
            const nbr = parseInt(row.querySelector(".inp-paiement-nbr").value);
            if (idType > 0 && nbr > 0) {
                paiements.push({ id_type_paiement: idType, nbr: nbr });
            }
        });

        const formData = new FormData();
        formData.append("id_pdc_itinerance", form.querySelector("[name='id_pdc_itinerance']").value);
        formData.append("id_station_itinerance", form.querySelector("[name='id_station_itinerance']").value);
        formData.append("puissance_nomiale", form.querySelector("[name='puissance_nomiale']").value);
        formData.append("nbr_pdc", form.querySelector("[name='nbr_pdc']").value);
        formData.append("date_mise_en_service", form.querySelector("[name='date_mise_en_service']").value);
        
        formData.append("id_raccordement", form.querySelector("[name='id_raccordement']").value);
        formData.append("id_restriction", form.querySelector("[name='id_restriction']").value);
        formData.append("id_accessibilite", form.querySelector("[name='id_accessibilite']").value);
        formData.append("id_condition", form.querySelector("[name='id_condition']").value);
        
        formData.append("num_pdl", form.querySelector("[name='num_pdl']").value);
        formData.append("tarification", form.querySelector("[name='tarification']").value);
        formData.append("observations", form.querySelector("[name='observations']").value);
        
        formData.append("charge_rapide", form.querySelector("[name='charge_rapide']").checked ? 1 : 0);
        formData.append("gratuit", form.querySelector("[name='gratuit']").checked ? 1 : 0);
        formData.append("reservation", form.querySelector("[name='reservation']").checked ? 1 : 0);
        formData.append("station_deux_roues", form.querySelector("[name='station_deux_roues']").checked ? 1 : 0);
        
        formData.append("prises", JSON.stringify(prises));
        formData.append("paiements", JSON.stringify(paiements));

        const urlEncodedData = new URLSearchParams(formData).toString();

        ajaxRequest('POST', '/api/index.php/pdc', (data) => {
            alertBox.classList.remove("d-none");
            if (data && data.success) {
                alertBox.classList.add("alert-success");
                alertBox.innerText = "Point de charge créé avec succès !";
                form.reset();
                document.getElementById("prises-container").innerHTML = "";
                document.getElementById("paiements-container").innerHTML = "";
                addPriseRow();
                addPaiementRow();
            } else {
                alertBox.classList.add("alert-danger");
                alertBox.innerText = "Erreur : " + (data ? data.message : "Impossible de créer le PDC.");
            }
            btnSubmit.disabled = false;
            btnSubmit.innerHTML = "Créer le PDC";
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }, urlEncodedData);
    });
});

let priseCounter = 0;
function addPriseRow() {
    priseCounter++;
    const container = document.getElementById("prises-container");
    const div = document.createElement("div");
    div.className = "row g-2 mb-2 prise-row align-items-end";
    div.id = `prise-row-${priseCounter}`;
    div.innerHTML = `
        <div class="col-6">
            <select class="form-select sel-prise-type">
                <option value="0">Sélectionner...</option>
                <option value="1">EF</option>
                <option value="2">Type 2</option>
                <option value="3">Combo CCS</option>
                <option value="4">CHAdeMO</option>
                <option value="5">Autre</option>
            </select>
        </div>
        <div class="col-4">
            <input type="number" class="form-control inp-prise-nbr" value="1" min="1" placeholder="Qté">
        </div>
        <div class="col-2 text-end">
            <button type="button" class="btn btn-sm btn-outline-danger w-100" onclick="document.getElementById('prise-row-${priseCounter}').remove()">X</button>
        </div>
    `;
    container.appendChild(div);
}

let paiementCounter = 0;
function addPaiementRow() {
    paiementCounter++;
    const container = document.getElementById("paiements-container");
    const div = document.createElement("div");
    div.className = "row g-2 mb-2 paiement-row align-items-end";
    div.id = `paiement-row-${paiementCounter}`;
    div.innerHTML = `
        <div class="col-6">
            <select class="form-select sel-paiement-type">
                <option value="0">Sélectionner...</option>
                <option value="1">Acte</option>
                <option value="2">CB</option>
                <option value="3">Autre</option>
            </select>
        </div>
        <div class="col-4">
            <input type="number" class="form-control inp-paiement-nbr" value="1" min="1" placeholder="Qté">
        </div>
        <div class="col-2 text-end">
            <button type="button" class="btn btn-sm btn-outline-danger w-100" onclick="document.getElementById('paiement-row-${paiementCounter}').remove()">X</button>
        </div>
    `;
    container.appendChild(div);
}
