# Projet d'Optimisation et de Chargement de Marchandises

## Présentation

Ce projet regroupe plusieurs algorithmes d'optimisation appliqués à des problèmes de transport et de chargement :

* **Problème du sac à dos (Knapsack Problem)** :

  * Algorithme glouton
  * Branch and Bound
  * Force brute

* **Problème de chargement de marchandises dans des conteneurs** :

  * Cas en 1 dimension
  * Cas en 2 dimensions
  * Cas en 3 dimensions
  * Heuristiques de placement

L'objectif est de comparer différentes approches algorithmiques afin de maximiser l'utilisation de l'espace disponible ou l'utilité des objets transportés tout en respectant des contraintes de capacité.

---

## Structure du projet

```text
.
├── data/
│   ├── marchandises.csv
│   ├── Données marchandises.xlsx
│   ├── Tableau données sac à dos Vélo.csv
│   └── Tableau données sac à dos Vélo.xlsx
│
├── modules/
│   ├── sac/
│   │   ├── Glouton.py
│   │   ├── BranchAndBound.py
│   │   └── bab/
│   │       └── Node.py
│   │
│   └── train/
│       ├── HeuristiqueBF.py
│       ├── PointsExtremes.py
│       ├── RectangleMaximaux.py
│       ├── RectangleMaximaux3D.py
│       └── objects/
│           ├── d1/
│           ├── d2/
│           └── d3/
│
├── algo_force_brute.py
├── algorithme_d=1.py
├── algorithme_d=2.py
├── algo max rectangle d=3 sans rotation.py
└── main.py
```

---

## Algorithmes implémentés

### 1. Sac à dos glouton

Fichier :

```text
modules/sac/Glouton.py
```

Principe :

1. Calcul du ratio :

```text
utilité / poids
```

2. Tri décroissant des objets selon ce ratio.
3. Ajout successif des objets dans le sac tant que la capacité maximale n'est pas dépassée.

**Avantages :**

* Très rapide
* Facile à implémenter

**Inconvénients :**

* Ne garantit pas toujours la solution optimale.

---

### 2. Branch and Bound

Fichier :

```text
modules/sac/BranchAndBound.py
```

Principe :

* Construction d'un arbre de recherche.
* Calcul d'une borne supérieure sur chaque nœud.
* Élimination des branches incapables d'améliorer la meilleure solution connue.

**Avantages :**

* Trouve la solution optimale.
* Réduit fortement l'espace de recherche.

**Inconvénients :**

* Plus coûteux en temps de calcul que l'algorithme glouton.

---

### 3. Force brute

Fichier :

```text
algo_force_brute.py
```

Principe :

* Génération de toutes les combinaisons possibles d'objets.
* Évaluation de chaque solution.
* Conservation de la meilleure solution.

**Avantages :**

* Solution optimale garantie.

**Inconvénients :**

* Temps de calcul exponentiel.
* Peu adapté aux grands ensembles de données.

---

## Chargement de marchandises

### Cas 1D

Fichier :

```text
algorithme_d=1.py
```

Les marchandises sont représentées par une seule dimension (longueur).

Objectif :

* Trier et organiser les éléments afin d'optimiser leur placement.

---

### Cas 2D

Fichier :

```text
algorithme_d=2.py
```

Les marchandises possèdent :

* Longueur
* Largeur

L'objectif est d'optimiser leur disposition dans une surface donnée.

---

### Cas 3D

Fichiers :

```text
modules/train/RectangleMaximaux3D.py
modules/train/PointsExtremes.py
modules/train/objects/d3/
```

Les colis possèdent :

* Longueur
* Largeur
* Hauteur

Les algorithmes cherchent à :

* Maximiser le taux de remplissage
* Réduire l'espace perdu
* Respecter les contraintes géométriques

---

## Données

Les données utilisées sont stockées dans le dossier :

```text
data/
```

Formats disponibles :

* CSV
* Excel (.xlsx)

Elles contiennent les caractéristiques des objets et marchandises utilisées pour les tests.

---

## Installation

### Prérequis

* Python 3.12+ (ou version compatible)
* pandas

Installation :

```bash
pip install pandas
```

---

## Exécution

### Lancer le programme principal

```bash
python main.py
```

### Tester le sac à dos glouton

```bash
python algo_force_brute.py
```

ou en utilisant directement les classes :

```python
from modules.sac.Glouton import Glouton

algo = Glouton(objets)
sac, stats = algo.run(5)
```

### Tester Branch and Bound

```python
from modules.sac.BranchAndBound import BranchAndBound

algo = BranchAndBound(objets, 5)
solution = algo.run()
```

---

## Comparaison des méthodes

| Méthode          | Optimale | Rapidité    |
| ---------------- | -------- | ----------- |
| Glouton          | Non      | Très rapide |
| Branch and Bound | Oui      | Rapide      |
| Force brute      | Oui      | Lente       |