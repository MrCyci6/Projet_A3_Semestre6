import pandas as pd
import folium
from folium.plugins import HeatMap

#PREPARATION DES DONNEES
file_path = "C:/Users/Margaux/Documents/GitHub/Projet_A3_Semestre6/Big Data/data/IRVE_clean.csv"
data = pd.read_csv(file_path)

# Coordonnées géographiques pures sans NA
data_geo = data.dropna(subset=["consolidated_latitude", "consolidated_longitude"]).copy()

# Extraction des coordonnées avec un poids fixe de 1.0
heat_data = [[lat, lon, 1.0] for lat, lon in zip(data_geo["consolidated_latitude"], data_geo["consolidated_longitude"])]

#VISUALISATION
carte1 = folium.Map(
    location=[46.2276, 2.2137],
    zoom_start=6,
    tiles="CartoDB positron"
)

#Ajout de la heatmap
HeatMap(
    heat_data,
    blur=8,
    radius=5,
    min_opacity=0.2,
    max_zoom=12, 
    gradient={
        0.2: "blue",
        0.35: "cyan",      
        0.5: "lime",      
        0.65: "yellow",   
        0.8: "orange",    
        1.0: "red"        
    }
).add_to(carte1)

#Sauvegarde de la carte
carte1.save("C:/Users/Margaux/Desktop/carte_heatmap.html")
print("terminé")