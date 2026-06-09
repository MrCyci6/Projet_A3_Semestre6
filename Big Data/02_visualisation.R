library(data.table)
library(stringr)

#récupération de la base de donnée
data <- fread("./data/IRVE_clean.csv")
head(data$date_mise_en_service)

#tri des données dont on a besoin partie 1 

#mise en format et bornes temporelles (vérifié par ia pour les tirets au lieu de /)
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
#(solution par ia)
evolution_tot$Date <- as.Date(paste0(evolution_tot$Var1, "-01"))
#visualisation graphique
plot(evolution_tot$Date,
    evolution_tot$Freq,
    type ="o",
    main="Evolution du nombre de stations mises en service par année/mois",
    xlab = "Temps (année/mois)",
    ylab= "Nombre de station",
    ylim = c(0, 3000),
    las =1)

#On rentre toutes les années
annees_exactes <- as.Date(c("2021-01-01", "2022-01-01", "2023-01-01", 
                            "2024-01-01", "2025-01-01", "2026-01-01", "2027-01-01"))
#On force l'axe des X à mettre toutes les années (solution par ia)
axis(1, 
     at = annees_exactes, 
     labels = c("2021", "2022", "2023", "2024", "2025", "2026", "2027"), 
     las = 1)

#tri des données étape 2 histogrammes
#puissance nominale

#mise en format, découpage des données en catégories
data_analyse$categorie_puissance <- cut(data_analyse$puissance_nominale,
                                    breaks = c(0, 3.7, 7.4, 11, 22, 43, 50, 150, Inf),
                                    labels = c("3.7kW", "7.4kW", "11kW", "22kW", "43kW",
                                     "50kW", "50 à \n 150kW", ">150kW"))
repartition_puissance <- table(data_analyse$categorie_puissance)

#visualisation graphique
barplot(repartition_puissance,
    horiz = TRUE,
    las = 1,
    main ="Répartition des puissances en kw",
    xlab = "Nombre de stations",
    xlim =c(0,30000),
    ylab = "Puissance")

#type de prise

#on récupère la liste de prises via le fichier csv
prises_charge <- c("prise_type_ef","prise_type_2",
                    "prise_type_combo_ccs","prise_type_chademo",
                    "prise_type_autre")

#on additionne les stations pour chaque type de prise 
comptage_prise <- colSums(data_analyse[,..prises_charge]=="true" |
                         data_analyse[,..prises_charge]==TRUE,
                         )

names(comptage_prise) <- c("Prise EF", "Type 2", "Combo CCS", "CHAdeMO", "Autre")
par(mar = c(5, 7, 4, 2))

barplot(comptage_prise,
    horiz = TRUE,
    las = 1,
    main ="Répartition des prises installées",
    xlab = "Nombre de station concernées",
    xlim =c(0,50000))

