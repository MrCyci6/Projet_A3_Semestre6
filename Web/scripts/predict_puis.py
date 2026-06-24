import pandas as pd
import joblib
import argparse

def predire_puissance(nouvelle_borne_dict):
    try:
        preprocessor = joblib.load("/var/www/scripts/models/02_preprocessor.pkl")
        model = joblib.load("/var/www/scripts/models/03_best_model_rf.pkl")
    except FileNotFoundError:
        return "Erreur : Les fichiers du modèle sont introuvables."

    df_nouveau = pd.DataFrame([nouvelle_borne_dict])
    try:
        X_nouveau_transforme = preprocessor.transform(df_nouveau)
    except ValueError as e:
        return f"Erreur dans les données : {e}"

    prediction = model.predict(X_nouveau_transforme)
    return prediction[0]

def main():
    parser = argparse.ArgumentParser(description="Prédire la puissance d'une borne")
    
    parser.add_argument('--nbre_pdc', type=int, default=5)
    parser.add_argument('--nb_types_prise', type=int, default=1)
    parser.add_argument('--consolidated_latitude', type=float, default=49.24)
    parser.add_argument('--consolidated_longitude', type=float, default=6.13)
    parser.add_argument('--charge_rapide', type=int, default=1)
    parser.add_argument('--prise_type_combo_ccs', type=int, default=1)
    parser.add_argument('--prise_type_2', type=int, default=0)
    parser.add_argument('--prise_type_ef', type=int, default=0)
    parser.add_argument('--prise_type_chademo', type=int, default=0)
    parser.add_argument('--prise_type_autre', type=int, default=0)
    parser.add_argument('--gratuit', type=int, default=0)
    parser.add_argument('--paiement_cb', type=int, default=0)
    parser.add_argument('--ouvert_24_7', type=int, default=1)
    parser.add_argument('--implantation_station', type=str, default='Parking privé à usage public')
    parser.add_argument('--condition_acces', type=str, default='Accès libre')
    
    args = parser.parse_args()
    
    borne_test_utilisateur = vars(args)
    
    resultat = predire_puissance(borne_test_utilisateur)
    print(resultat)
    

if __name__ == "__main__":
    main()