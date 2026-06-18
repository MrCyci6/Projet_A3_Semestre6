import pandas as pd
import numpy as np
import joblib

# Nous chargeons le modèle et les encodeurs/scaler (cela doit être exécuté après avoir lancé train_model.py)
try:
    modele = joblib.load('modele_final.pkl')
    encoders = joblib.load('encoders.pkl')
    scaler = joblib.load('scaler.pkl')
    features = joblib.load('features.pkl')
except FileNotFoundError:
    print("Erreur : Fichiers du modèle introuvables. Veuillez d'abord exécuter train_model.py.")
    exit()

def predire_implantation(borne: dict) -> str:
    """
    Prédit le type d'implantation d'une borne de recharge.
    
    Paramètres :
    ------------
    borne : dict contenant les caractéristiques de la borne
    
    Retourne :
    ----------
    str : type d'implantation prédit
    """
    df_borne = pd.DataFrame([borne])
    
    # 1. Ajout des features calculées
    top_operateurs = [c for c in encoders['operateur_groupe'].classes_ if c != 'Autre']
    df_borne['operateur_groupe'] = df_borne.get('nom_operateur', '').apply(
        lambda x: x if x in top_operateurs else 'Autre'
    )
    
    # Ajout de departement
    if 'code_insee_commune' in df_borne.columns:
        df_borne['departement'] = df_borne['code_insee_commune'].astype(str).str[:2]
    else:
        df_borne['departement'] = 'Inconnu'
    
    # 2. Encodage booléens
    bool_cols = ['charge_rapide', 'ouvert_24_7', 'paiement_cb', 'paiement_acte',
                 'paiement_autre', 'gratuit', 'reservation', 'cable_t2_attache',
                 'station_deux_roues', 'prise_type_ef', 'prise_type_2',
                 'prise_type_combo_ccs', 'prise_type_chademo', 'prise_type_autre']
    for col in bool_cols:
        # Si la colonne manque dans le dict, on met 0 par défaut
        if col not in df_borne.columns:
            df_borne[col] = 0
        else:
            df_borne[col] = df_borne[col].astype(int)
    
    # 3. Encodage catégorielles
    cat_cols = ['condition_acces', 'raccordement', 'accessibilite_pmr',
                'operateur_groupe', 'departement']
    for col in cat_cols:
        le = encoders[col]
        val = str(df_borne[col].values[0]) if col in df_borne.columns else 'Inconnu'
        if val not in le.classes_:
            df_borne[col] = le.transform([le.classes_[0]])[0]  # valeur de secours
        else:
            df_borne[col] = le.transform([val])[0]
    
    # 4. Normalisation
    num_cols = ['puissance_nominale', 'nbre_pdc', 'nb_types_prise']
    for col in num_cols:
        if col not in df_borne.columns:
            df_borne[col] = 0
    df_borne[num_cols] = scaler.transform(df_borne[num_cols])
    
    # 5. Sélection des features dans le bon ordre (tel que défini par l'entraînement)
    X = df_borne[features]
    
    # 6. Prédiction
    prediction = modele.predict(X)[0]
    proba = modele.predict_proba(X)[0]
    classes = modele.classes_
    
    # Affichage des résultats
    print(f"\n{'='*55}")
    print(f"  Implantation prédite : {prediction}")
    print(f"{'='*55}")
    print("\n  Probabilités par classe :")
    for c, p in sorted(zip(classes, proba), key=lambda x: -x[1]):
        barre = '█' * int(p * 30)
        print(f"  {c:<45} {barre} {p:.1%}")
    print(f"{'='*55}\n")
    
    return prediction


if __name__ == "__main__":
    # --- TEST ---
    borne_test = {
        'puissance_nominale': 150,
        'nbre_pdc': 4,
        'nb_types_prise': 2,
        'charge_rapide': True,
        'ouvert_24_7': True,
        'paiement_cb': True,
        'paiement_acte': True,
        'paiement_autre': False,
        'gratuit': False,
        'reservation': False,
        'cable_t2_attache': False,
        'station_deux_roues': False,
        'prise_type_ef': False,
        'prise_type_2': False,
        'prise_type_combo_ccs': True,
        'prise_type_chademo': True,
        'prise_type_autre': False,
        'condition_acces': 'Accès libre',
        'raccordement': 'Direct',
        'accessibilite_pmr': 'Accessible mais non conforme',
        'nom_operateur': 'TotalEnergies Charging Services',
        'code_insee_commune': 75056
    }

    print("Lancement d'une prédiction de test...")
    predire_implantation(borne_test)
