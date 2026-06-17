import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib

# Chargement
df = pd.read_csv("../data/IRVE_formatted.csv", low_memory=False)

# Nettoyage de la cible
df['puissance_nominale'] = df['puissance_nominale'].astype(str).str.replace(',', '.').astype(float)
df = df.dropna(subset=['puissance_nominale'])

# Transformation en classes (Binning)
limites = [0, 7.4, 22.0, 149.9, float('inf')]
etiquettes = ['Lente (<=7.4kW)', 'Moyenne (<=22kW)', 'Rapide (<150kW)', 'Ultra-rapide (>=150kW)']
df['categorie_puissance'] = pd.cut(df['puissance_nominale'], bins=limites, labels=etiquettes)
df = df.dropna(subset=['categorie_puissance'])

colonnes_exploitees = [
    'nbre_pdc', 'nb_types_prise', 'consolidated_latitude', 'consolidated_longitude', # Numériques
    'charge_rapide', 'prise_type_combo_ccs', 'prise_type_2', 'prise_type_ef',        # Booléens liés aux prises
    'prise_type_chademo', 'prise_type_autre',                                        
    'gratuit', 'paiement_cb', 'ouvert_24_7',                                         # Booléens liés aux services
    'implantation_station', 'condition_acces'                                        # Catégories
]

# Séparation Features (X) et Cible (y)
X = df[colonnes_exploitees].copy()
y = df['categorie_puissance']

# Conversion explicite des booléens textuels en numériques (0/1)
bool_cols = [
    'charge_rapide', 'prise_type_combo_ccs', 'prise_type_2', 'prise_type_ef',
    'prise_type_chademo', 'prise_type_autre', 'gratuit', 'paiement_cb', 'ouvert_24_7'
]
for col in bool_cols:
    X[col] = (X[col].astype(str).str.upper() == 'TRUE').astype(int)

# Définition des transformations par type de colonne
numeric_features = ['nbre_pdc', 'nb_types_prise', 'consolidated_latitude', 'consolidated_longitude']
categorical_features = ['implantation_station', 'condition_acces']
binary_features = bool_cols

# Pipeline Numérique (Imputation + Normalisation)
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Pipeline Catégoriel (Imputation + One-Hot Encoding)
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='Inconnu')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

# Pipeline Binaire
binary_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent'))
])

# Le ColumnTransformer global
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features),
        ('bin', binary_transformer, binary_features)
    ]
)

# Division Train / Test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Ajuster le préprocesseur sur le jeu d'entraînement uniquement (évite le data leakage)
X_train_transformed = preprocessor.fit_transform(X_train)
X_test_transformed = preprocessor.transform(X_test)

# ENREGISTREMENT DU PRÉPROCESSEUR (Attendu crucial pour la partie Web)
joblib.dump(preprocessor, "outputs/02_preprocessor.pkl")

# Sauvegarde temporaire des données prêtes pour l'étape d'apprentissage
joblib.dump((X_train_transformed, X_test_transformed, y_train, y_test), "outputs/02_data_preparer.pkl")