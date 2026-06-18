# Clustering Géographique des Bornes IRVE

Ce module utilise l'apprentissage non supervisé (K-Means) pour segmenter géographiquement les Infrastructures de Recharge pour Véhicules Électriques (IRVE) sur le territoire français.

## Objectifs

L'objectif de ce script (`02_clustering.py`) est de regrouper les bornes de recharge en clusters cohérents basés uniquement sur leurs coordonnées GPS (Latitude/Longitude). Cela permet d'identifier des zones de densité et de structurer l'analyse territoriale.

## Fonctionnalités

1.  **Prétraitement** : Filtrage des données sans coordonnées GPS et normalisation via `StandardScaler` pour garantir une pondération équitable des coordonnées.
2.  **Optimisation du modèle** : Évaluation du nombre optimal de clusters ($k$) via quatre métriques :
    *   **Inertie** (Méthode du coude).
    *   **Score de Silhouette** (Qualité de la séparation, calculé sur un échantillon).
    *   **Indice Calinski-Harabasz**.
    *   **Indice Davies-Bouldin**.
3.  **Entraînement final** : Application de l'algorithme K-Means avec $k=5$, identifié comme un compromis optimal.
4.  **Persistance** : Sauvegarde du modèle (`kmeans_irve.pkl`) et du scaler (`scaler_irve.pkl`) via `joblib` pour réutilisation.
5.  **Visualisation** : Génération de graphiques de performance (Matplotlib) et d'une carte de répartition géographique (Plotly Express exporté via Kaleido).

## Prérequis

```bash
pip install pandas numpy scikit-learn matplotlib plotly joblib kaleido
```

## Structure des Sorties

L'exécution du script crée un dossier `outputs/` contenant :

*   `outputs/metriques_clustering.png` : Graphiques d'aide à la décision (Coude, Silhouette, etc.).
*   `outputs/carte_clustering.png` : Visualisation géographique des clusters.
*   `outputs/kmeans_irve.pkl` : Le modèle K-Means entraîné.
*   `outputs/scaler_irve.pkl` : Le scaler (indispensable pour normaliser les nouvelles données de prédiction).

## Utilisation

Vérifiez la configuration des chemins (notamment l'accès WSL vers Windows le cas échéant) et assurez-vous que `IRVE_clean.csv` est accessible, puis lancez :

```bash
python 02_clustering.py
```