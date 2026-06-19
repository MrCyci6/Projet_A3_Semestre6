import os
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
import plotly.express as px
import plotly.io as pio

# --- CHEMIN STRICT POUR WINDOWS VIA WSL ---
# On cible directement ton dossier Windows pour être sûr de voir les fichiers
base_dir = "/mnt/c/Users/Margaux/Documents/GitHub/Projet_A3_Semestre6/IA/client2"
output_dir = os.path.join(base_dir, "outputs")
os.makedirs(output_dir, exist_ok=True)

# Chargement des données
file_path = "/mnt/c/Users/Margaux/Documents/GitHub/Projet_A3_Semestre6/Big Data/data/IRVE_clean.csv"
data = pd.read_csv(file_path, low_memory=False)
print(f"Données chargées : {data.shape[0]} lignes.")

# Récupération des données que l'on souhaite + normalisation
features = ["consolidated_latitude", "consolidated_longitude", "puissance_nominale"]

data_geo = data.dropna(subset=[
    "consolidated_latitude", "consolidated_longitude", "puissance_nominale"
]).copy()

X = data_geo[features].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Détermination du nombre de clusters avec les différentes métriques
k_range = range(3, 11)
silhouette_scores = []
ch_scores = []
db_scores = []
inertias = []

print("Calcul des métriques pour chaque k...")
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    y_pred = kmeans.fit_predict(X_scaled)

    silhouette_scores.append(silhouette_score(X_scaled, y_pred, sample_size=10000, random_state=42))
    ch_scores.append(calinski_harabasz_score(X_scaled, y_pred))
    db_scores.append(davies_bouldin_score(X_scaled, y_pred))
    inertias.append(kmeans.inertia_)

# Configuration Matplotlib pour tourner sans écran sous WSL
plt.switch_backend('Agg')

fig_metriques, axes = plt.subplots(2, 2, figsize=(12, 8))
fig_metriques.suptitle("Évaluation du nombre de clusters (KMeans)", fontsize=14)

axes[0, 0].plot(k_range, inertias, marker='o', color="steelblue")
axes[0, 0].set_title("Inertie (méthode du coude)")
axes[0, 0].set_xlabel("k")
axes[0, 0].grid(True)

axes[0, 1].plot(k_range, silhouette_scores, marker='o', color="seagreen")
axes[0, 1].set_title("Silhouette ↑ (max = meilleur)")
axes[0, 1].set_xlabel("k")
axes[0, 1].grid(True)

axes[1, 0].plot(k_range, ch_scores, marker='o', color="darkorange")
axes[1, 0].set_title("Calinski-Harabasz ↑ (max = meilleur)")
axes[1, 0].set_xlabel("k")
axes[1, 0].grid(True)

axes[1, 1].plot(k_range, db_scores, marker='o', color="crimson")
axes[1, 1].set_title("Davies-Bouldin ↓ (min = meilleur)")
axes[1, 1].set_xlabel("k")
axes[1, 1].grid(True)

plt.tight_layout()

# Sauvegarde forcée du premier graphique
output_metriques = os.path.join(output_dir, "metriques_clustering.png")
plt.savefig(output_metriques, dpi=150)
plt.close()
print(f" 1/2 - Graphique des métriques enregistré ici : {output_metriques}")

# Modèle final
k = 5  
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
y_pred = kmeans.fit_predict(X_scaled)
data_geo["cluster"] = y_pred

# Sauvegarde des objets de modélisation
joblib.dump(kmeans, os.path.join(output_dir, "kmeans_irve.pkl"))
joblib.dump(scaler, os.path.join(output_dir, "scaler_irve.pkl"))

# Visualisation carte
fig_map = px.scatter_map(
    data_geo,
    lat="consolidated_latitude",
    lon="consolidated_longitude",
    color="cluster",
    zoom=5,
    center={"lat": 46.2276, "lon": 2.2137},
    opacity=0.6,
    size_max=6,
    title="Clustering des bornes de recharge IRVE",
    map_style="carto-positron"
)
fig_map.update_traces(marker=dict(size=5))
fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0})

# Sauvegarde forcée de la carte en PNG via Kaleido
output_carte = os.path.join(output_dir, "carte_clustering.png")
fig_map.write_image(output_carte, engine="kaleido")
print(f" 2/2 - Carte PNG enregistrée ici : {output_carte}")