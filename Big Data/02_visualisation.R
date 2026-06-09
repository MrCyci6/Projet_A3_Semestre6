library(data.table)
library(stringr)

#récupération de la base de donnée
data <- fread("./data/IRVE_clean.csv")
head(data$date_mise_en_service)

#tri des données dont on a besoin

#mise en format et bornes temporelles
date_debut <- as.POSIXct("01-01-2021 00:00", format = "%d-%m-%Y %H:%M",)
date_fin <- as.POSIXct("01-01-2027 00:00", format = "%d-%m-%Y %H:%M")
data$date_mise_en_service <- as.POSIXct(data$date_mise_en_service, 
                            format = "%d-%m-/%Y %H:%M")

#récupération des données entre les bornes 
data_analyse <- data[!is.na(data$date_mise_en_service) & 
                    data$date_mise_en_service >= date_debut &
                    data$date_mise_en_service <= date_fin,]

#création d'une nouvelle colonne, puis d'une table avec toutes les données
data_analyse$annee_mois <- format(data_analyse$date_mise_en_service, "%Y-%m")
evolution_stations <- table(data_analyse$annee_mois)
#mise en place d'une data frame pour la visualisation graphique
evolution_tot <- as.data.frame(evolution_stations)
#visualisation graphique
plot(evolution_tot, 
    main="Evolution du nombre de stations mises en service par année/mois",
    xlab = "Temps (année/mois)",
    ylab= "Nombre de station",
    las =2)