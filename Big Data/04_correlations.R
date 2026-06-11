# Fonctionnalité 4 : Étude des corrélations (Variables Qualitatives)

library(data.table)
library(dplyr)

# 1. Importation des données
df <- fread("D:/COURS/A3/Projet A3 Semestre 6/Big Data/data/IRVE_formatted.csv") 

# 2. Préparation des variables (Transformation en catégories)
df_quali <- df %>%
  select(charge_rapide, gratuit, paiement_cb, ouvert_24_7, implantation_station, nbre_pdc) %>%
  mutate(across(everything(), as.factor)) %>%
  na.omit()

# EXEMPLE 1 : Gratuité vs Charge Rapide
cat("\n--- Tableau croisé : Gratuit vs Charge Rapide ---\n")
tab_gratuit_rapide <- table(df_quali$gratuit, df_quali$charge_rapide)
print(tab_gratuit_rapide)

cat("\n--- Test du Chi-2 : Gratuit vs Charge Rapide ---\n")
print(chisq.test(tab_gratuit_rapide))

mosaicplot(tab_gratuit_rapide, 
           main = "Relation entre Gratuité et Charge Rapide",
           xlab = "Gratuit", 
           ylab = "Charge Rapide",
           color = c("#e74c3c", "#3498db"))

# EXEMPLE 2 : Localisation vs Équipement (Implantation vs Nombre de prises)
# On regroupe le nombre de prises (PDC) pour que le tableau soit lisible
df_implant <- df %>%
  filter(!is.na(implantation_station), !is.na(nbre_pdc)) %>%
  mutate(taille_station = case_when(
    nbre_pdc == 1            ~ "1 prise",
    nbre_pdc <= 4            ~ "2 à 4 prises",
    TRUE                     ~ "5 prises et +"
  )) %>%
  mutate(taille_station = as.factor(taille_station))

cat("\n--- Tableau croisé : Implantation vs Taille de station ---\n")
tab_implant <- table(df_implant$implantation_station, df_implant$taille_station)
print(tab_implant)

cat("\n--- Test du Chi-2 : Implantation vs Taille de station ---\n")
print(chisq.test(tab_implant))

mosaicplot(tab_implant,
           main = "Implantation de la station vs Taille (nb de prises)",
           xlab = "Type d'implantation",
           ylab = "Taille de la station",
           color = c("#3498db", "#e67e22", "#2ecc71"),
           las = 2) # las=2 permet d'écrire les labels à la verticale


# EXEMPLE 3 : Ouverture 24/7 vs Implantation
cat("\n--- Tableau croisé : Ouverture 24/7 vs Implantation ---\n")
tab_24_implant <- table(df_quali$ouvert_24_7, df_quali$implantation_station)
print(tab_24_implant)

cat("\n--- Test du Chi-2 : Ouverture 24/7 vs Implantation ---\n")
print(chisq.test(tab_24_implant))

mosaicplot(tab_24_implant, 
           main = "Disponibilité 24h/7j selon l'implantation",
           xlab = "Ouvert 24h/24 et 7j/7", 
           ylab = "Type d'implantation",
           color = c("#9b59b6", "#34495e"),
           las = 2) # las=2 pour incliner le texte si besoin