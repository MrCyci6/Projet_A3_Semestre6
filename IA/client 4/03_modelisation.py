import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, accuracy_score

print("1. Chargement des données prétraitées...")
# On charge les matrices prêtes à l'emploi que nous avons sauvegardées à l'étape précédente
X_train_transformed, X_test_transformed, y_train, y_test = joblib.load("outputs/02_data_preparer.pkl")

print("2. Configuration du modèle et du GridSearchCV...")
# On initialise le modèle de base
rf = RandomForestClassifier(class_weight='balanced', random_state=42)

# On définit la "grille" d'hyperparamètres à tester. 
# Le GridSearchCV va tester toutes les combinaisons possibles.
param_grid = {
    'n_estimators': [200, 300, 500],           # Plus d'arbres
    'max_depth': [20, 30, None],               # Jusqu'où creuser ?
    'min_samples_split': [2, 5, 10],           # Échantillons min pour diviser un nœud
    'min_samples_leaf': [1, 2, 4],             # Échantillons min pour créer une feuille finale
    'max_features': ['sqrt', 'log2']           # Formule mathématique pour la sélection des colonnes
}

# Configuration du GridSearch (cv=3 signifie validation croisée en 3 plis, n_jobs=-1 utilise tous les cœurs du CPU)
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, scoring='f1_weighted', n_jobs=-1, verbose=2)

print("3. Entraînement et recherche des meilleurs paramètres (cela peut prendre quelques minutes)...")
grid_search.fit(X_train_transformed, y_train)

# Affichage des meilleurs paramètres trouvés
print("\n--- RÉSULTATS DU GRIDSEARCH ---")
print(f"Meilleurs hyperparamètres : {grid_search.best_params_}")

# Récupération du meilleur modèle
best_model = grid_search.best_estimator_

print("\n4. Évaluation sur le jeu de Test...")
y_pred = best_model.predict(X_test_transformed)

print(f"Précision globale (Accuracy) : {accuracy_score(y_test, y_pred):.4f}\n")
print("Rapport de classification détaillé :")
print(classification_report(y_test, y_pred))

# 5. Sauvegarde du modèle final
joblib.dump(best_model, "outputs/03_best_model_rf.pkl")
print("Le modèle optimisé a été sauvegardé sous 'outputs/03_best_model_rf.pkl'.")