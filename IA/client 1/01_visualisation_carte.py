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

#VISUALISATION CARTE
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

#CLUSTERING VISUEL 

import pandas as pd
import folium
from folium.plugins import MarkerCluster
import branca
import matplotlib.pyplot as plt

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

#VISUALISATION GRAPHIQUE
counts = data_geo['categorie_puissance'].value_counts().reindex(data_label)

fig, ax = plt.subplots(figsize=(10, 5))

bars = ax.bar(counts.index, counts.values,
              color=list(palette.values()), edgecolor='white', linewidth=0.6)

# Valeurs au-dessus des barres
for bar in bars:
    h = bar.get_height()
    if h > 0:
        ax.text(bar.get_x() + bar.get_width() / 2, h + counts.max() * 0.01,
                f'{int(h):,}', ha='center', va='bottom', fontsize=9)

ax.set_title("Distribution des bornes de recharge par puissance nominale", fontsize=13, pad=12)
ax.set_xlabel("Catégorie de puissance", fontsize=11)
ax.set_ylabel("Nombre de points de recharge", fontsize=11)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))
ax.spines[['top', 'right']].set_visible(False)
ax.grid(axis='y', linestyle='--', alpha=0.4)

plt.tight_layout()
plt.show()

#VISUALISATION CARTE
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

#Extraction des tableaux de données qui nous intéressent
lats = data_geo["consolidated_latitude"].values
lons = data_geo["consolidated_longitude"].values
puissances = data_geo["categorie_puissance"].astype(str).values
gratuites = data_geo["gratuit"].astype(str).values  
pmrs = data_geo["accessibilite_pmr"].astype(str).values
op = data_geo["nom_operateur"].astype(str).values


#Génération des marqueurs colorés et texte de popup
for lat, lon, p_label, gratuit, pmr, operateur in zip(lats, lons, puissances, gratuites, pmrs, op):
    couleur = palette.get(p_label, "#888888")
    texte_popup = (
        f"<b>Opérateur :</b> {operateur}<br>"
        f"<b>Puissance :</b> {p_label}<br>"
        f"<b>Gratuit :</b> {gratuit}<br>"
        f"<b>Accès PMR :</b> {pmr}"
    )
    
    folium.CircleMarker(
        location=[lat, lon],
        radius=6,
        color=couleur,
        fill=True,
        fill_color=couleur,
        fill_opacity=0.8,
        popup=folium.Popup(texte_popup, min_width=200, max_width=300)
    ).add_to(cluster_principal)

legende = branca.colormap.StepColormap(
    colors=list(palette.values()),
    vmin=0,
    vmax=len(palette),
    caption="Puissance Nominale des Bornes de Recharge"
)   

html_items = "".join([f"<div><span style='display:inline-block;width:12px;height:12px;background:{c};border-radius:50%;margin-right:8px;'></span><span style='color:black;'>{k}</span></div>" for k, c in palette.items()])

html_final = f"<div style='position:fixed;bottom:30px;right:30px;z-index:9999;background:white;padding:10px;border:1px solid gray;border-radius:5px;font-family:sans-serif;font-size:12px;box-shadow:2px 2px 5px rgba(0,0,0,0.2);'><b style='color:black;display:block;margin-bottom:5px;'>Puissance</b>{html_items}</div>"

#rajout de la légende sur la carte
carte.get_root().html.add_child(branca.element.Element(html_final))


#SAUVEGARDE
carte.save("C:/Users/Margaux/Desktop/carte_clusters.html")
print("terminé")