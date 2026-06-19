# 🗺️ Clustering des Bornes de Recharge IRVE (Client 2)
**Projet A3 - Semestre 6**

Ce projet utilise l'Intelligence Artificielle (Machine Learning) pour regrouper automatiquement les bornes de recharge électrique (IRVE) en clusters homogènes, selon leur **localisation géographique**, afin d'identifier des profils d'infrastructure sur le territoire français.

---

## 🛠️ Prérequis et Installation

Pour faire fonctionner ce projet sur votre machine, vous devez avoir **Python 3.8+** installé, ainsi que **WSL** (Windows Subsystem for Linux) si vous êtes sous Windows.

1. Ouvrez votre terminal WSL.
2. Placez-vous dans le dossier du projet.
3. Installez les bibliothèques requises avec la commande suivante :

`pip install pandas numpy scikit-learn matplotlib plotly kaleido joblib`

---

## 📂 Architecture du Projet

```
Projet_A3_Semestre6/
├── Big Data/
│   └── data/
│       └── IRVE_clean.csv           ← Base de données des bornes (à fournir)
└── IA/
    └── client2/
        ├── clustering_irve.py       ← Script principal
        └── outputs/                 ← Générés automatiquement
            ├── metriques_clustering.png
            ├── carte_clustering.png
            ├── kmeans_irve.pkl
            └── scaler_irve.pkl
```

---

## 🚀 Comment lancer le projet ?

### Étape unique : Lancer le script de clustering

`python clustering_irve.py`

Le script va enchaîner automatiquement toutes les étapes : chargement des données, évaluation des métriques, entraînement du modèle final et génération des visualisations.

*Note : Le calcul des métriques pour k de 3 à 10 peut prendre quelques minutes selon la taille du jeu de données.*

Les fichiers générés apparaîtront dans le dossier `outputs/` :

```
1/2 - Graphique des métriques enregistré ici : .../outputs/metriques_clustering.png
2/2 - Carte PNG enregistrée ici : .../outputs/carte_clustering.png
```

---

## 🧠 Comment ça fonctionne ? (Sous le capot)

Le pipeline repose sur trois grandes étapes :

### 1. Préparation des données

Les 3 features retenues sont extraites du CSV, les lignes avec des valeurs manquantes sur ces colonnes sont exclues, puis l'ensemble est normalisé avec un `StandardScaler` pour que latitude, longitude et puissance aient le même poids statistique.

| Feature | Description |
|---|---|
| `consolidated_latitude` | Latitude GPS de la borne |
| `consolidated_longitude` | Longitude GPS de la borne |
| `puissance_nominale` | Puissance en kW |

### 2. Choix du nombre de clusters

Le script teste automatiquement les valeurs de `k` de 3 à 10 et génère un graphique avec 4 métriques complémentaires :

| Métrique | Objectif |
|---|---|
| **Inertie** | Méthode du coude — repérer la cassure dans la courbe |
| **Silhouette** ↑ | Plus la valeur est haute, mieux les clusters sont séparés |
| **Calinski-Harabasz** ↑ | Plus la valeur est haute, plus les clusters sont denses |
| **Davies-Bouldin** ↓ | Plus la valeur est basse, meilleure est la séparation |

### 3. Modèle final et visualisation

Le modèle **KMeans** est entraîné avec **k = 5** (choisi après analyse des métriques). Deux objets sont sauvegardés pour pouvoir refaire des prédictions sans réentraîner :

- **`kmeans_irve.pkl`** : le modèle KMeans entraîné
- **`scaler_irve.pkl`** : le scaler de normalisation (indispensable pour transformer de nouvelles données dans le même espace)

Une carte interactive est ensuite générée avec Plotly et exportée en PNG via **Kaleido**, avec une couleur distincte par cluster, centrée sur la France métropolitaine.

---

## ⚙️ Paramètres à ajuster

- **Nombre de clusters** : modifier la variable `k = 5` dans le script pour tester une autre valeur suggérée par les métriques.
- **Poids de la puissance** : la puissance est incluse dans le clustering mais peut être amplifiée en la multipliant avant le scaling si les clusters semblent trop géographiques :

