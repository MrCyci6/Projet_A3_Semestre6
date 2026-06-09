#options(timeout = 300)
#install.packages("leaflet", dependencies = TRUE)
#install.packages("leaflet.extras")

library(leaflet)
library(maps)
library(leaflet.extras)

#on récupère les données géographiques
data <- fread("./data/IRVE_clean.csv")
data_geo <- data_analyse[, c("latitude", "longitude")]
data_geo <- data_analyse[!is.na(consolidated_latitude) & !is.na(consolidated_longitude), 
                         .(consolidated_longitude, consolidated_latitude)]

#
data_analyse$categorie_puissance <- cut(data_analyse$puissance_nominale,
                                    breaks = c(0, 3.7, 7.4, 11, 22, 43, 50, 150, Inf),
                                    labels = c("3.7kW", "7.4kW", "11kW", "22kW", "43kW",
                                     "50kW", "50 à \n 150kW", ">150kW"))

categories <- c("3.7kW", "7.4kW", "11kW", "22kW", "43kW", "50kW", "50 à 150kW", ">150kW")
categories_ordonnees <- factor(categories, levels = les_categories)

palette_globale <- colorFactor( palette = c("#33e923", "#21a008", "#0d7909", "#086d6d", "#d12497", "#a51a70", "#4f0b55", "#1e062c"),
                                domain = categories_ordonnees)
# Création de la carte interactive 
carte_base <- leaflet(data_geo)
carte_fonds <- addTiles(carte_base)
carte_cadree <- setView(carte_fonds, lng = 2.2137, lat = 46.2276, zoom = 6)
carte_chaleur <- addHeatmap(carte_cadree, lng = ~consolidated_longitude, lat = ~consolidated_latitude, blur = 20, max = 0.05, radius = 15)
carte_marqueur <- addMarkers(carte_chaleur, lng = ~consolidated_longitude, lat = ~consolidated_latitude, clusterOptions = markerClusterOptions())

#Ajout d'une partie supplémentaire sur les bornes de puissances + la légende (avec l'aide de l'ia)
carte_puissance <- addCircleMarkers(carte_marqueur, lng = ~consolidated_longitude, lat = ~consolidated_latitude,
                                radius = 7,color = ~palette_globale(categories_puissance),
                                clusterOptions = markerClusterOptions())
carte_finale <- addLegend(carte_puissance, pal = palette_globale, values = categories_ordonnees,
                        position = "bottomright", title = "Type de recharge")
carte_finale
