# Clustering Géographique des Bornes IRVE

Ce module utilise l'apprentissage non supervisé (K-Means) pour segmenter géographiquement les Infrastructures de Recharge pour Véhicules Électriques (IRVE) sur le territoire français.

## Objectifs

L'objectif de ce script (`02_clustering.py`) est de regrouper les bornes de recharge en clusters cohérents basés uniquement sur leurs coordonnées GPS (Latitude/Longitude). Cela permet d'identifier des zones de densité et de structurer l'analyse territoriale.

## Fonctionnalités

1.  **Prétraitement** : Nettoyage des coordonnées manquantes et normalisation des données avec `StandardScaler`.
2.  **Optimisation du modèle** : Évaluation du nombre optimal de clusters ($k$) via quatre métriques :
    *   **Inertie** (Méthode du coude).
    *   **Coefficient de Silhouette** (Qualité de la séparation).
    *   **Indice Calinski-Harabasz**.
    *   **Indice Davies-Bouldin**.
3.  **Entraînement final** : Application de l'algorithme K-Means avec $k=5$ (paramétrable).
4.  **Persistance** : Sauvegarde du modèle entraîné et du scaler pour une utilisation ultérieure (prédictions en production).
5.  **Visualisation Interactive** : Génération d'une carte interactive via Plotly Express.

## Prérequis

```bash
pip install pandas numpy scikit-learn matplotlib plotly joblib
```

## Structure des Sorties

L'exécution du script génère les fichiers suivants :

*   `metriques_clustering.png` : Graphiques d'aide à la décision pour le choix de $k$.
*   `kmeans_irve.pkl` : Le modèle K-Means sauvegardé.
*   `scaler_irve.pkl` : Le scaler utilisé pour la normalisation (indispensable pour les nouvelles données).

## Utilisation

Assurez-vous que le fichier `IRVE_clean.csv` est présent dans le dossier de données, puis lancez :

```bash
python 02_clustering.py
```
