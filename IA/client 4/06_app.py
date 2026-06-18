import streamlit as st
import pandas as pd
import joblib

# Configuration de la page
st.set_page_config(page_title="Prédiction IRVE", page_icon="⚡", layout="centered")

# ==========================================
# CHARGEMENT DES MODÈLES ET DONNÉES
# ==========================================
@st.cache_resource
def load_models():
    try:
        preprocessor = joblib.load("outputs/02_preprocessor.pkl")
        model = joblib.load("outputs/03_best_model_rf.pkl")
        return preprocessor, model
    except Exception as e:
        return None, None

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("../data/IRVE_formatted.csv", low_memory=False)
        # Nettoyage de la cible comme dans l'entraînement
        df['puissance_nominale'] = df['puissance_nominale'].astype(str).str.replace(',', '.').astype(float)
        df = df.dropna(subset=['puissance_nominale'])
        
        limites = [0, 7.4, 22.0, 149.9, float('inf')]
        etiquettes = ['Lente (<=7.4kW)', 'Moyenne (<=22kW)', 'Rapide (<150kW)', 'Ultra-rapide (>=150kW)']
        df['vraie_categorie'] = pd.cut(df['puissance_nominale'], bins=limites, labels=etiquettes)
        df = df.dropna(subset=['vraie_categorie'])
        return df
    except Exception as e:
        return None

preprocessor, model = load_models()
df_real = load_data()

# ==========================================
# INTERFACE UTILISATEUR
# ==========================================
st.title("⚡ Estimateur de Puissance IRVE")

if preprocessor is None or model is None:
    st.error("Erreur : Impossible de charger les modèles (.pkl).")
    st.stop()

# Création des onglets
tab1, tab2 = st.tabs(["✍️ Saisie Manuelle", "🎲 Test depuis le CSV réel"])

# ------------------------------------------
# ONGLET 1 : SAISIE MANUELLE
# ------------------------------------------
with tab1:
    st.markdown("Renseignez les caractéristiques de la borne pour prédire sa catégorie de puissance nominale.")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📍 Localisation & Accès")
        lat = st.number_input("Latitude", value=48.85, format="%.2f")
        lon = st.number_input("Longitude", value=2.35, format="%.2f")
        
        implantation = st.selectbox("Implantation de la station", [
            "Voirie", "Parking privé à usage public", "Station dédiée à la recharge rapide",
            "Parking public", "Etablissement commercial"
        ])
        acces = st.selectbox("Condition d'accès", ["Accès libre", "Accès réservé"])
        
        st.subheader("⚙️ Équipement")
        nbre_pdc = st.slider("Nombre de points de charge", min_value=1, max_value=20, value=2)
        nb_types_prise = st.slider("Diversité des prises", min_value=1, max_value=5, value=2)

    with col2:
        st.subheader("🔌 Types de prises")
        charge_rapide = st.checkbox("Option Charge Rapide globale activée", value=False)
        prise_ccs = st.checkbox("Prise Combo CCS (Standard Rapide)", value=False)
        prise_chademo = st.checkbox("Prise CHAdeMO (Standard Asiatique)", value=False)
        prise_t2 = st.checkbox("Prise Type 2 (Standard AC)", value=True)
        prise_ef = st.checkbox("Prise Type EF (Domestique)", value=False)
        prise_autre = st.checkbox("Autre type de prise", value=False)
        
        st.subheader("💶 Services")
        ouvert_24_7 = st.checkbox("Ouvert 24h/24 et 7j/7", value=True)
        paiement_cb = st.checkbox("Paiement par Carte Bancaire", value=True)
        gratuit = st.checkbox("Recharge Gratuite", value=False)

    st.markdown("---")
    if st.button("🚀 Estimer la puissance", use_container_width=True):
        borne_dict = {
            'nbre_pdc': nbre_pdc, 'nb_types_prise': nb_types_prise, 'consolidated_latitude': lat,
            'consolidated_longitude': lon, 'charge_rapide': int(charge_rapide),
            'prise_type_combo_ccs': int(prise_ccs), 'prise_type_2': int(prise_t2),
            'prise_type_ef': int(prise_ef), 'prise_type_chademo': int(prise_chademo),
            'prise_type_autre': int(prise_autre), 'gratuit': int(gratuit),
            'paiement_cb': int(paiement_cb), 'ouvert_24_7': int(ouvert_24_7),
            'implantation_station': implantation, 'condition_acces': acces
        }
        
        df_nouveau = pd.DataFrame([borne_dict])
        
        try:
            X_transforme = preprocessor.transform(df_nouveau)
            prediction = model.predict(X_transforme)[0]
            st.success("### Prédiction réussie !")
            st.markdown(f"<h2 style='text-align: center; color: #4CAF50;'>Catégorie : {prediction}</h2>", unsafe_allow_html=True)
        except ValueError as e:
            st.error(f"Erreur de traitement : {e}")

# ------------------------------------------
# ONGLET 2 : TEST DEPUIS LE CSV
# ------------------------------------------
with tab2:
    st.markdown("Testez le modèle sur une vraie borne de la base de données IRVE.")
    
    if df_real is None:
        st.error("Fichier data/IRVE_formatted.csv introuvable.")
    else:
        # Bouton pour tirer une ligne au hasard
        if st.button("🎲 Tirer une borne au hasard", type="primary"):
            # Sélection d'une ligne aléatoire
            sample = df_real.sample(1).iloc[0]
            st.session_state['current_sample'] = sample
            
        # Si une ligne a été tirée (stockée dans la session pour ne pas disparaître)
        if 'current_sample' in st.session_state:
            sample = st.session_state['current_sample']
            
            # Affichage des informations brutes (pour vérification)
            st.info(f"**Station analysée :** {sample.get('nom_station', 'Inconnu')}")
            
            # Préparation du dictionnaire pour la prédiction
            # ATTENTION: Il faut reformater les booléens comme dans le script 02
            borne_csv_dict = {
                'nbre_pdc': sample['nbre_pdc'],
                'nb_types_prise': sample['nb_types_prise'],
                'consolidated_latitude': sample['consolidated_latitude'],
                'consolidated_longitude': sample['consolidated_longitude'],
                'charge_rapide': int(str(sample['charge_rapide']).upper() == 'TRUE'),
                'prise_type_combo_ccs': int(str(sample['prise_type_combo_ccs']).upper() == 'TRUE'),
                'prise_type_2': int(str(sample['prise_type_2']).upper() == 'TRUE'),
                'prise_type_ef': int(str(sample['prise_type_ef']).upper() == 'TRUE'),
                'prise_type_chademo': int(str(sample['prise_type_chademo']).upper() == 'TRUE'),
                'prise_type_autre': int(str(sample['prise_type_autre']).upper() == 'TRUE'),
                'gratuit': int(str(sample['gratuit']).upper() == 'TRUE'),
                'paiement_cb': int(str(sample['paiement_cb']).upper() == 'TRUE'),
                'ouvert_24_7': int(str(sample['ouvert_24_7']).upper() == 'TRUE'),
                'implantation_station': sample['implantation_station'],
                'condition_acces': sample['condition_acces']
            }
            
            df_test = pd.DataFrame([borne_csv_dict])
            
            # Affichage des données préparées (pour montrer que ça correspond au formulaire)
            with st.expander("Voir les caractéristiques envoyées au modèle"):
                st.dataframe(df_test)
            
            try:
                # Prédiction
                X_test_trans = preprocessor.transform(df_test)
                pred_csv = model.predict(X_test_trans)[0]
                vraie_valeur = sample['vraie_categorie']
                puissance_brute = sample['puissance_nominale']
                
                st.markdown("### Résultat de l'évaluation")
                
                # Comparaison et affichage
                col_res1, col_res2 = st.columns(2)
                with col_res1:
                    st.metric(label="Prédiction du Modèle (IA)", value=str(pred_csv))
                with col_res2:
                    st.metric(label=f"Réalité (Terrain : {puissance_brute} kW)", value=str(vraie_valeur))
                
                if str(pred_csv) == str(vraie_valeur):
                    st.success("✅ **Le modèle a vu juste !** La prédiction correspond parfaitement à la réalité du terrain.")
                else:
                    st.error("❌ **Erreur de prédiction.** Le modèle s'est trompé de catégorie pour cette borne spécifique.")
                    
            except Exception as e:
                st.error(f"Erreur lors de la prédiction : {e}")