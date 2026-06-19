# Prédiction de la Puissance des Bornes IRVE (Client 4)



**Projet A3 - Semestre 6**



## Prérequis et Installation



Pour faire fonctionner ce projet sur votre machine, vous devez avoir **Python 3.8+** installé.



1. Ouvrez votre terminal (ou invite de commande).

2. Placez-vous dans le dossier du projet.

3. Installez les bibliothèques requises avec la commande suivante :



`pip install pandas numpy scikit-learn matplotlib seaborn streamlit joblib`



---



## Architecture du Projet



Le projet est découpé en plusieurs scripts numérotés pour respecter l'ordre logique d'un pipeline de Data Science :



* `data/IRVE_formatted.csv` : La base de données brute des bornes.

* `01_exploration.py` : Analyse exploratoire et génération des graphiques de justification.

* `02_preprocessing.py` : Nettoyage, encodage, et sauvegarde du pipeline (`preprocessor.pkl`).

* `03_modelisation.py` : Entraînement du modèle Random Forest optimisé par GridSearchCV et sauvegarde (`best_model_rf.pkl`).

* `04_evaluation.py` : Génération de la matrice de confusion pour évaluer les performances.

* `05_predict.py` : Script en ligne de commande pour tester une prédiction isolée.

* `06_app_streamlit.py` : L'interface Web interactive complète.



---



## Comment lancer le projet ?



### Étape 1 : Entraînement et création des modèles (À faire une seule fois)

Avant de pouvoir lancer l'application ou faire des prédictions, vous devez générer les fichiers modèles `.pkl`. Dans votre terminal, exécutez ces deux commandes :



`python 02_preprocessing.py`

`python 03_modelisation.py`



*Note : Le script 03 peut prendre quelques minutes car il teste des centaines de combinaisons (GridSearchCV) pour trouver le meilleur réglage de l'IA.*



### Étape 2 : Utilisation (Deux choix possibles)



**Choix A : L'Interface Graphique Web (Recommandé)**

Pour lancer l'application interactive et tester le modèle via un navigateur web, utilisez Streamlit :



`streamlit run 06_app.py`



Une page web s'ouvrira automatiquement (généralement sur `http://localhost:8501`). Vous pourrez y saisir les caractéristiques d'une borne ou tester une vraie ligne tirée au hasard depuis le fichier CSV.



**Choix B : La Ligne de Commande (Pour les développeurs)**

Pour tester le modèle de manière programmatique sans interface graphique, exécutez le script d'inférence :



`python 05_predict.py`



---



## Comment ça fonctionne ? (Sous le capot)



Le système repose sur deux piliers majeurs sauvegardés sur le disque dur pour éviter de relancer l'apprentissage à chaque requête :



1. **La Pipeline de Prétraitement (`preprocessor.pkl`)** : 

&#x20;  Lorsqu'une nouvelle borne est saisie (ex: Latitude 48.8, Prise CCS cochée), ce pipeline s'assure de nettoyer la donnée, de combler les éventuels vides, de standardiser les coordonnées et d'encoder le texte en valeurs mathématiques (One-Hot Encoding). Il garantit que l'entrée a toujours le même format.



2. **Le Modèle Prédictif (`best_model_rf.pkl`)** :

&#x20;  Il s'agit d'un **Random Forest Classifier** (Forêt Aléatoire). Il interroge simultanément des centaines d'arbres de décision qui ont appris à reconnaître des schémas dans les données (ex: *si une borne a le flag 'Charge Rapide' ET se trouve sur des coordonnées hors centre-ville, elle est généralement Ultra-rapide*). Le modèle consolide les "votes" de chaque arbre et retourne la catégorie finale avec une précision supérieure à 90%.

