import argparse
import sys
import warnings
import pandas as pd
import numpy as np
import joblib
import json

warnings.filterwarnings("ignore", category=UserWarning, module='sklearn')

# Nous chargeons le modèle et les encodeurs/scaler (cela doit être exécuté après avoir lancé train_model.py)
try:
    modele = joblib.load('/var/www/scripts/models/modele_final.pkl')
    encoders = joblib.load('/var/www/scripts/models/encoders.pkl')
    scaler = joblib.load('/var/www/scripts/models/scaler.pkl')
    features = joblib.load('/var/www/scripts/models/features.pkl')
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
    
    return {
        "prediction": str(prediction),
        "probabilites": {str(c): float(p) for c, p in zip(classes, proba)}
    }


def main():
    parser = argparse.ArgumentParser(description="Prédiction d'implantation de borne")
    
    parser.add_argument('--puissance_nominale', type=float, default=22.0)
    parser.add_argument('--nbre_pdc', type=int, default=2)
    parser.add_argument('--nb_types_prise', type=int, default=1)
    parser.add_argument('--charge_rapide', type=int, default=0)
    parser.add_argument('--ouvert_24_7', type=int, default=1)
    parser.add_argument('--paiement_cb', type=int, default=0)
    parser.add_argument('--paiement_acte', type=int, default=0)
    parser.add_argument('--paiement_autre', type=int, default=0)
    parser.add_argument('--gratuit', type=int, default=0)
    parser.add_argument('--reservation', type=int, default=0)
    parser.add_argument('--cable_t2_attache', type=int, default=0)
    parser.add_argument('--station_deux_roues', type=int, default=0)
    parser.add_argument('--prise_type_ef', type=int, default=0)
    parser.add_argument('--prise_type_2', type=int, default=0)
    parser.add_argument('--prise_type_combo_ccs', type=int, default=0)
    parser.add_argument('--prise_type_chademo', type=int, default=0)
    parser.add_argument('--prise_type_autre', type=int, default=0)
    
    parser.add_argument('--condition_acces', type=str, default='Accès libre')
    parser.add_argument('--raccordement', type=str, default='Direct')
    parser.add_argument('--accessibilite_pmr', type=str, default='Inconnu')
    parser.add_argument('--nom_operateur', type=str, default='Autre')
    parser.add_argument('--code_insee_commune', type=str, default='00000')

    args = parser.parse_args()
    
    borne_data = vars(args)
    
    bool_cols = ['charge_rapide', 'ouvert_24_7', 'paiement_cb', 'paiement_acte', 
                 'paiement_autre', 'gratuit', 'reservation', 'cable_t2_attache', 
                 'station_deux_roues', 'prise_type_ef', 'prise_type_2', 
                 'prise_type_combo_ccs', 'prise_type_chademo', 'prise_type_autre']
    
    for col in bool_cols:
        borne_data[col] = bool(borne_data[col])

    resultat_dict = predire_implantation(borne_data)
    
    print(json.dumps(resultat_dict))

if __name__ == "__main__":
    main()