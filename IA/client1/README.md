# Visualisation Cartographique des Bornes IRVE

Ce module est dédié à la représentation spatiale et à l'analyse statistique des Infrastructures de Recharge pour Véhicules Électriques (IRVE) en France.

## Objectifs

Le script `01_visualisation_carte.py` permet de transformer les données de localisation et de caractéristiques techniques en outils d'aide à la décision visuels, facilitant la compréhension de la densité du réseau et de la segmentation par puissance.

## Fonctionnalités

1.  **Heatmap de Densité** : Identification visuelle immédiate des zones de forte concentration (métropoles et axes routiers) via `HeatMap`.
2.  **Analyse Statistique** : Génération d'un graphique (Matplotlib) montrant la répartition des bornes selon 8 paliers de puissance (de 3.7kW à plus de 150kW).
3.  **Carte de Clusters Interactive** :
    *   Regroupement dynamique des points via `MarkerCluster` pour une navigation fluide.
    *   Code couleur thématique basé sur la puissance nominale.
    *   Popups enrichis affichant l'opérateur, la puissance exacte, la gratuité et l'accessibilité PMR.

## Prérequis

```bash
pip install pandas folium matplotlib branca
```

## Structure des Sorties

Le script crée un dossier `outputs/` contenant :

*   `outputs/carte_heatmap.html` : Carte de chaleur interactive.
*   `outputs/distribution_puissances.png` : Graphique de répartition des puissances.
*   `outputs/carte_clusters.html` : Carte détaillée avec clusters et légendes personnalisées.

## Utilisation

Assurez-vous que le chemin vers le dataset `IRVE_clean.csv` est correctement configuré (notamment pour l'accès WSL), puis lancez :

```bash
python 01_visualisation_carte.py
```