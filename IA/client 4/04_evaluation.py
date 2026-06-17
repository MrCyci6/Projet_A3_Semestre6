import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

# 1. Chargement des données de test et du modèle optimisé
_, X_test_transformed, _, y_test = joblib.load("outputs/02_data_preparer.pkl")
best_model = joblib.load("outputs/03_best_model_rf.pkl")

# 2. Prédictions
y_pred = best_model.predict(X_test_transformed)

# 3. Création de la matrice de confusion
etiquettes = ['Lente', 'Moyenne', 'Rapide', 'Ultra-rapide']
cm = confusion_matrix(y_test, y_pred, labels=['Lente (<=7.4kW)', 'Moyenne (<=22kW)', 'Rapide (<150kW)', 'Ultra-rapide (>=150kW)'])

# 4. Affichage graphique
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=etiquettes, yticklabels=etiquettes)
plt.title("Matrice de Confusion du Modèle Random Forest")
plt.ylabel("Vraie Catégorie")
plt.xlabel("Catégorie Prédite")
plt.tight_layout()
plt.savefig("outputs/04_matrice_confusion.png")
print("Le graphique 'outputs/04_matrice_confusion.png' a été généré avec succès pour votre rapport.")