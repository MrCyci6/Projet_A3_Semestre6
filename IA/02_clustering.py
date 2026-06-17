import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
import plotly.express as px

#Chargement des données
file_path = 'C:/Users/Margaux/Documents/GitHub/Projet_A3_Semestre6/Big Data/data/IRVE_clean.csv'
data = pd.read_csv(file_path)
print(data)

#Récupération des données que l'on souhaite + normalisation
data_geo = data.dropna(subset=[
    "consolidated_latitude", "consolidated_longitude"
]).copy()
features = ["consolidated_latitude", "consolidated_longitude"]
X = data_geo[features].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print(X)

#Détermination du nombre de clusters
k_range = range(3, 11)
silhouette_scores = []
ch_scores = []
db_scores = []
inertias = []

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    y_pred = kmeans.fit_predict(X_scaled)

    silhouette_scores.append(silhouette_score(X_scaled, y_pred, sample_size=10000, random_state=42))
    ch_scores.append(calinski_harabasz_score(X_scaled, y_pred))
    db_scores.append(davies_bouldin_score(X_scaled, y_pred))
    inertias.append(kmeans.inertia_)

    print(f"k={k} | Silhouette={silhouette_scores[-1]:.4f} | CH={ch_scores[-1]:.1f} | DB={db_scores[-1]:.4f}")

#Mise en forme visuelle des données en utilisant des métriques (Silhouette Coefficient , Calinski-Harabasz Index , Davies-Bouldin Index)
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("Évaluation du nombre de clusters (KMeans)", fontsize=14)

axes[0, 0].plot(k_range, inertias, marker='o', color="steelblue")
axes[0, 0].set_title("Inertie (méthode du coude)")
axes[0, 0].set_xlabel("k")
axes[0, 0].set_ylabel("Inertie")
axes[0, 0].grid(True)

axes[0, 1].plot(k_range, silhouette_scores, marker='o', color="seagreen")
axes[0, 1].set_title("Silhouette ↑ (max = meilleur)")
axes[0, 1].set_xlabel("k")
axes[0, 1].set_ylabel("Score")
axes[0, 1].grid(True)

axes[1, 0].plot(k_range, ch_scores, marker='o', color="darkorange")
axes[1, 0].set_title("Calinski-Harabasz ↑ (max = meilleur)")
axes[1, 0].set_xlabel("k")
axes[1, 0].set_ylabel("Score")
axes[1, 0].grid(True)

axes[1, 1].plot(k_range, db_scores, marker='o', color="crimson")
axes[1, 1].set_title("Davies-Bouldin ↓ (min = meilleur)")
axes[1, 1].set_xlabel("k")
axes[1, 1].set_ylabel("Score")
axes[1, 1].grid(True)

plt.tight_layout()
plt.savefig("metriques_clustering.png", dpi=150)
plt.show()

#Modèle final
k = 5  # à ajuster après avoir vu les graphiques

kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
y_pred = kmeans.fit_predict(X_scaled)
data_geo["cluster"] = y_pred

print(kmeans.cluster_centers_)

# Sauvegarde du modèle ET du scaler
joblib.dump(kmeans, "kmeans_irve.pkl")
joblib.dump(scaler, "scaler_irve.pkl")
print("Modèle sauvegardé")

#Visualisation sous forme de carte
fig = px.scatter_map(
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

fig.update_traces(marker=dict(size=5))
fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
fig.show()

#Script de prédiction + test
kmeans = joblib.load("kmeans_irve.pkl")
scaler = joblib.load("scaler_irve.pkl")

def predire_cluster(latitude, longitude) -> int:
    X_new = np.array([[latitude, longitude]])
    X_new_scaled = scaler.transform(X_new)
    return int(kmeans.predict(X_new_scaled)[0])

# Test
cluster = predire_cluster(48.8566, 2.3522)
print(f"Cluster prédit : {cluster}")
