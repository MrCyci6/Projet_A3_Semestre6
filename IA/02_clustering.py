import pandas as pd
import folium
from folium.plugins import MarkerCluster

#PREPARATION DES DONNEES
file_path = "C:/Users/Margaux/Documents/GitHub/Projet_A3_Semestre6/Big Data/data/IRVE_clean.csv"
data = pd.read_csv(file_path)

# Nettoyage strict des coordonnées et des puissances manquantes
data_geo = data.dropna(subset=["consolidated_latitude", "consolidated_longitude", "puissance_nominale"]).copy()

# Découpage et labellisation des puissances
data_puiss = [0, 3.7, 7.4, 11, 22, 43, 50, 150, float("inf")]
data_label = ["3.7kW", "7.4kW", "11kW", "22kW", "43kW", "50kW", "50 à 150kW", ">150kW"]

data_geo['categorie_puissance'] = pd.cut(data_geo['puissance_nominale'],
                                         bins=data_puiss,
                                         labels=data_label)

# Dictionnaire de couleurs
palette = {
    "3.7kW" : "#33e923",
    "7.4kW" : "#21a008",
    "11kW" :  "#0d7909",
    "22kW":   "#086d6d",
    "43kW":   "#d12497",
    "50kW" :  "#a51a70",
    "50 à 150kW" : "#4f0b55",
    ">150kW" : "#1e062c"
}

#VISUALISATION
carte = folium.Map(
    location=[46.2276, 2.2137],
    zoom_start=6,
    tiles="CartoDB positron"
)

cluster_principal = MarkerCluster(options={
    "maxClusterRadius": 80, 
    "disableClusteringAtZoom": 14, 
    "spiderfyDistanceMultiplier": 2
}).add_to(carte)

#Extraction des tableaux de données
lats = data_geo["consolidated_latitude"].values
lons = data_geo["consolidated_longitude"].values
puissances = data_geo["categorie_puissance"].astype(str).values

#Génération des marqueurs colorés
for lat, lon, p_label in zip(lats, lons, puissances):
    couleur = palette.get(p_label, "#888888")
    
    folium.CircleMarker(
        location=[lat, lon],
        radius=6,
        color=couleur,
        fill=True,
        fill_color=couleur,
        fill_opacity=0.8,
        popup=f"Puissance: {p_label}"
    ).add_to(cluster_principal)

#SAUVEGARDE
carte.save("C:/Users/Margaux/Desktop/carte_clusters.html")
print("terminé")