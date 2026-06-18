import pandas as pd
import joblib

def predire_puissance(nouvelle_borne_dict):
    """
    Prend en entrée les caractéristiques d'une borne (dictionnaire)
    et renvoie la catégorie de puissance prédite.
    """
    try:
        preprocessor = joblib.load("outputs/02_preprocessor.pkl")
        model = joblib.load("outputs/03_best_model_rf.pkl")
    except FileNotFoundError:
        return "Erreur : Les fichiers du modèle sont introuvables. Lancez les scripts 02 et 03 d'abord."

    df_nouveau = pd.DataFrame([nouvelle_borne_dict])

    try:
        X_nouveau_transforme = preprocessor.transform(df_nouveau)
    except ValueError as e:
        return f"Erreur dans les données fournies : {e}"

    prediction = model.predict(X_nouveau_transforme)
    
    return prediction[0]

# ==========================================
# TEST DU SCRIPT
# ==========================================
if __name__ == "__main__":
    borne_test_utilisateur = {
        'nbre_pdc': 5,
        'nb_types_prise': 1,
        'consolidated_latitude': 49.24,
        'consolidated_longitude': 6.13,
        'charge_rapide': 1,              
        'prise_type_combo_ccs': 1,       
        'prise_type_2': 0,               
        'prise_type_ef': 0,              
        'prise_type_chademo': 0,        
        'prise_type_autre': 0,          
        'gratuit': 0,                   
        'paiement_cb': 0,               
        'ouvert_24_7': 1,               
        'implantation_station': 'Parking privé à usage public',
        'condition_acces': 'Accès libre'
    }

    print("--- SIMULATEUR DE PRÉDICTION ---")
    print("Caractéristiques reçues :", borne_test_utilisateur)
    
    resultat = predire_puissance(borne_test_utilisateur)
    
    print(f"\n=> PRÉDICTION DU MODÈLE : Cette borne appartient à la catégorie : {resultat}")