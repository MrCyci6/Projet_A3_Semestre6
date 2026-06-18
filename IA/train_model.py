import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import warnings

# Ignorer certains avertissements pour un affichage plus propre
warnings.filterwarnings('ignore')

def train_and_save_model(data_path="IRVE_formatted.csv"):
    print("--- 1. Chargement des données ---")
    try:
        # On lit le dataset
        df = pd.read_csv(data_path, low_memory=False)
    except FileNotFoundError:
        print(f"Erreur : le fichier {data_path} est introuvable. Veuillez vérifier le chemin.")
        return
        
    print(f"Données chargées : {df.shape[0]} lignes.")

    print("\n--- 2. Imputation et nettoyage ---")
    df['puissance_nominale'] = df['puissance_nominale'].fillna(df['puissance_nominale'].median())
    df['charge_rapide'] = df['charge_rapide'].fillna(False).infer_objects(copy=False)
    df['raccordement'] = df['raccordement'].fillna('Inconnu')

    print("\n--- 3. Création de nouvelles features ---")
    top_operateurs = df['nom_operateur'].value_counts().nlargest(20).index
    df['operateur_groupe'] = df['nom_operateur'].apply(
        lambda x: x if x in top_operateurs else 'Autre'
    )
    df['departement'] = df['code_insee_commune'].astype(str).str[:2]

    print("\n--- 4. Encodage ---")
    # Encodage booléens
    bool_cols = ['charge_rapide', 'ouvert_24_7', 'paiement_cb', 'paiement_acte',
                 'paiement_autre', 'gratuit', 'reservation', 'cable_t2_attache',
                 'station_deux_roues', 'prise_type_ef', 'prise_type_2',
                 'prise_type_combo_ccs', 'prise_type_chademo', 'prise_type_autre']
    for col in bool_cols:
        df[col] = df[col].astype(int)

    # Encodage catégorielles
    cat_cols = ['condition_acces', 'raccordement', 'accessibilite_pmr', 
                'operateur_groupe', 'departement']
    encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

    joblib.dump(encoders, 'encoders.pkl')
    print("Encodeurs sauvegardés dans 'encoders.pkl'")

    print("\n--- 5. Normalisation ---")
    scaler = StandardScaler()
    num_cols = ['puissance_nominale', 'nbre_pdc', 'nb_types_prise']
    df[num_cols] = scaler.fit_transform(df[num_cols])
    
    joblib.dump(scaler, 'scaler.pkl')
    print("Scaler sauvegardé dans 'scaler.pkl'")

    print("\n--- 6. Préparation pour l'entraînement ---")
    features = [
        'puissance_nominale', 'nbre_pdc', 'nb_types_prise',
        'charge_rapide', 'ouvert_24_7', 'paiement_cb', 'paiement_acte',
        'paiement_autre', 'gratuit', 'reservation', 'cable_t2_attache',
        'station_deux_roues', 'prise_type_ef', 'prise_type_2',
        'prise_type_combo_ccs', 'prise_type_chademo', 'prise_type_autre',
        'condition_acces', 'raccordement', 'accessibilite_pmr',
        'operateur_groupe', 'departement'
    ]

    joblib.dump(features, 'features.pkl')
    print("Liste des features sauvegardée dans 'features.pkl'")

    X = df[features]
    y = df['implantation_station']

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Train : {X_train.shape[0]} lignes | Test : {X_test.shape[0]} lignes")

    print("\n--- 7. Entraînement et GridSearchCV ---")
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [None, 20, 30],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2]
    }

    grid_search = GridSearchCV(
        RandomForestClassifier(class_weight='balanced', random_state=42, n_jobs=-1),
        param_grid,
        cv=3,
        scoring='f1_macro',
        verbose=1,
        n_jobs=-1
    )

    print("Lancement de la recherche d'hyperparamètres (GridSearchCV)...")
    grid_search.fit(X_train, y_train)

    print(f"\nMeilleurs paramètres : {grid_search.best_params_}")
    print(f"Meilleur score CV    : {grid_search.best_score_:.4f}")

    print("\n--- 8. Évaluation sur les données de test ---")
    y_pred_best = grid_search.best_estimator_.predict(X_test)
    print("\n--- Rapport final ---")
    print(classification_report(y_test, y_pred_best))

    print("\n--- 9. Sauvegarde du modèle final ---")
    joblib.dump(grid_search.best_estimator_, 'modele_final.pkl')
    print("Modèle sauvegardé dans 'modele_final.pkl'")
    print("Processus d'entraînement terminé avec succès !")

if __name__ == "__main__":
    # Vous pouvez changer le chemin ici si besoin
    train_and_save_model("IRVE_formatted.csv")
