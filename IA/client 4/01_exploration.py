import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Chargement
df = pd.read_csv("../data/IRVE_formatted.csv", low_memory=False)

# Nettoyage de la cible
df['puissance_nominale'] = df['puissance_nominale'].astype(str).str.replace(',', '.').astype(float)
df = df.dropna(subset=['puissance_nominale'])

# Arrondir les coordonnées à 2 décimales (1km de précision)
df['consolidated_latitude'] = df['consolidated_latitude'].round(2)
df['consolidated_longitude'] = df['consolidated_longitude'].round(2)

# Transformation en classes (Binning)
limites = [0, 7.4, 22.0, 149.9, float('inf')]
etiquettes = ['Lente (<=7.4kW)', 'Moyenne (<=22kW)', 'Rapide (<150kW)', 'Ultra-rapide (>=150kW)']
df['categorie_puissance'] = pd.cut(df['puissance_nominale'], bins=limites, labels=etiquettes)
df = df.dropna(subset=['categorie_puissance'])

# Répartition des classes de puissance
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='categorie_puissance', order=etiquettes, palette='viridis')
plt.title("Répartition des bornes par catégorie de puissance")
plt.xlabel("Catégorie")
plt.ylabel("Nombre de bornes")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig("outputs/01_distribution_puissance.png")
plt.close()

# Justification de l'impact du type de prise (ex: Combo CCS)
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='categorie_puissance', hue='charge_rapide', order=etiquettes)
plt.title("Impact de la variable 'charge_rapide' sur la catégorie de puissance")
plt.xlabel("Catégorie de puissance")
plt.ylabel("Nombre de bornes")
plt.tight_layout()
plt.savefig("outputs/01_justification_charge_rapide.png")
plt.close()