#options(timeout = 300)
#install.packages("leaflet", dependencies = TRUE)
#install.packages("leaflet.extras")

library(leaflet)
library(maps)
library(leaflet.extras)
library(data.table)

#on récupère les données géographiques
data_analyse <- fread("C:/Users/Margaux/Documents/GitHub/Projet_A3_Semestre6/Big Data/data/IRVE_clean.csv")
data_geo <- data_analyse[, c("consolidated_latitude", "consolidated_longitude")]
data_geo <- data_analyse[!is.na(consolidated_latitude) & !is.na(consolidated_longitude), 
                         .(consolidated_longitude, consolidated_latitude)]

#On récupère les puissance découpées en catégories
data_analyse$categorie_puissance <- cut(data_analyse$puissance_nominale,
                                    breaks = c(0, 3.7, 7.4, 11, 22, 43, 50, 150, Inf),
                                    labels = c("3.7kW", "7.4kW", "11kW", "22kW", "43kW",
                                     "50kW", "50 à 150kW", ">150kW"))

categories <- c("3.7kW", "7.4kW", "11kW", "22kW", "43kW", "50kW", "50 à 150kW", ">150kW")

#On range les catégories dans l'ordre croissant
categories_ordonnees <- factor(categories, levels = categories)

# Création d'une palette pour les catégories de puissance 
palette_globale <- colorFactor( palette = c("#33e923", "#21a008", "#0d7909", "#086d6d", "#d12497", "#a51a70", "#4f0b55", "#1e062c"),
                                domain = categories_ordonnees)
lignes_valides <- !is.na(data_analyse$consolidated_latitude) & !is.na(data_analyse$consolidated_longitude)

#On relie les données entre elles
data_geo$categorie_puissance <- data_analyse[lignes_valides]$categorie_puissance
brut_gratuit <- data_analyse[lignes_valides]$gratuit
data_geo$texte_gratuit <- ifelse(brut_gratuit == TRUE | brut_gratuit == "VRAI", "Oui", "Non")

# Création de la carte interactive 
carte_base <- leaflet(data_geo)
carte_fonds <- addTiles(carte_base)
carte_cadree <- setView(carte_fonds, lng = 2.2137, lat = 46.2276, zoom = 6)
carte_chaleur <- addHeatmap(carte_cadree, lng = ~consolidated_longitude, lat = ~consolidated_latitude, blur = 20, max = 0.05, radius = 15, clusterOptions = markerClusterOptions(maxZoom = 5))
carte_marqueur <- addMarkers(carte_chaleur, lng = ~consolidated_longitude, lat = ~consolidated_latitude, clusterOptions = markerClusterOptions())

#Ajout d'une partie supplémentaire sur les bornes de puissances + un popup si gratuit ou non(avec l'aide de l'ia)
carte_puissance <- addCircleMarkers(carte_marqueur, lng = ~consolidated_longitude, lat = ~consolidated_latitude,
                                radius = 7,color = ~palette_globale(categorie_puissance),
                                clusterOptions = markerClusterOptions(spiderfyDistanceMultiplier = 2),
                                popup = ~paste0("Gratuit : ", texte_gratuit),
                                options = popupOptions(closeButton = TRUE))
#Ajout d'une légende afin de voir la puissance de la borne
carte_legende <- addLegend(carte_puissance, pal = palette_globale, values = categories_ordonnees,
                        position = "bottomright", title = "Type de recharge")
                          
carte_legende
