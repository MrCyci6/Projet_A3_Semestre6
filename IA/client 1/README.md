# Visualisation des Bornes de Recharge (IRVE)

Ce module est dédié à la visualisation cartographique et statistique des Infrastructures de Recharge pour Véhicules Électriques (IRVE). Il permet de transformer les données brutes de localisation et de puissance en cartes interactives exploitables.

## Fonctionnalités

Le script `01_visualisation_carte.py` génère trois types de rendus :

1. **Carte de Chaleur (Heatmap)** : 
   - Visualise la densité des points de charge sur le territoire français.
   - Permet d'identifier rapidement les zones de forte concentration (zones urbaines, axes routiers majeurs).
   - Exporté sous : `carte_heatmap.html`.

2. **Analyse Statistique** :
   - Génère un graphique à barres (Matplotlib) montrant la distribution des bornes par catégories de puissance nominale (de 3.7kW à plus de 150kW).

3. **Carte de Clustering Interactive** :
   - Regroupe les bornes par proximité géographique (MarkerCluster).
   - Utilise un code couleur spécifique pour chaque palier de puissance.
   - Affiche des popups détaillés pour chaque borne : Nom de l'opérateur, Puissance, Gratuité, et Accessibilité PMR.
   - Exporté sous : `carte_clusters.html`.

## Prérequis

Les bibliothèques Python suivantes sont nécessaires :

```bash
pip install pandas folium matplotlib branca
```

## Structure des Données

Le script s'appuie sur le fichier `IRVE_clean.csv`. Les colonnes critiques utilisées sont :
- `consolidated_latitude` & `consolidated_longitude` : Coordonnées GPS.
- `puissance_nominale` : Puissance de la borne en kW.
- `nom_operateur`, `gratuit`, `accessibilite_pmr` : Informations descriptives pour les popups.

## Utilisation

Lancez simplement le script pour générer les fichiers HTML sur votre bureau :
`python 01_visualisation_carte.py`