## code corriger et assisté par Gemini

library(data.table)
library(dplyr)
library(ggplot2)
library(caret)
library(nnet)
library(e1071)

# Importation et Préparation des données
df <- fread("IRVE_formatted.csv")

# création et Nettoyage de la variable cible (Tarification)
if(!"stringr" %in% installed.packages()) install.packages("stringr")
library(stringr)

df_model <- df %>%
  mutate(
    tarif_clean = tolower(tarification),
    tarif_clean = str_replace_all(tarif_clean, ",", "."),
    # Extraction heuristique du prix au kWh
    prix_kwh_extrait = case_when(
      str_detect(tarif_clean, "([0-9]{2})\\s*cts") ~ as.numeric(str_extract(tarif_clean, "([0-9]{2})(?=\\s*cts)")) / 100,
      str_detect(tarif_clean, "([0-9]+\\.[0-9]+)\\s*€?\\s*/?\\s*kwh") ~ as.numeric(str_extract(tarif_clean, "([0-9]+\\.[0-9]+)(?=\\s*€?\\s*/?\\s*kwh)")),
      str_detect(tarif_clean, "([0-9]+\\.[0-9]+)\\s*€") ~ as.numeric(str_extract(tarif_clean, "([0-9]+\\.[0-9]+)(?=\\s*€)")),
      TRUE ~ NA_real_
    )
  )

# Calcul de la moyenne des tarifs identifiés (pour séparer Modéré / Élevé)
moyenne_prix <- mean(df_model$prix_kwh_extrait, na.rm = TRUE)
cat("\n--- Extraction de la Tarification ---\n")
cat("Prix moyen calculé par Regex :", round(moyenne_prix, 3), "€/kWh\n\n")

df_model <- df_model %>%
  mutate(tarification_groupe = case_when(
    as.logical(gratuit) == TRUE | grepl("\\bgratuit\\b|^0$|^0\\.0+$", tarif_clean) ~ "Bas",
    !is.na(prix_kwh_extrait) & prix_kwh_extrait < moyenne_prix ~ "Modéré",
    !is.na(prix_kwh_extrait) & prix_kwh_extrait >= moyenne_prix ~ "Élevé",
    grepl("forfait|abonnement", tarif_clean) ~ "Modéré",
    TRUE ~ "Inconnu" 
  )) %>%
  mutate(tarification_groupe = factor(tarification_groupe, levels = c("Bas", "Modéré", "Élevé", "Inconnu")))

# Top opérateurs → garder les N plus fréquents, regrouper le reste en "Autre"
top_operateurs <- names(sort(table(df_model$nom_operateur), decreasing = TRUE)[1:20])

df_model <- df_model %>%
  mutate(
    operateur_groupe = ifelse(nom_operateur %in% top_operateurs, 
                              nom_operateur, 
                              "Autre"),
    operateur_groupe = as.factor(operateur_groupe)
  )

# Imputation des valeurs manquantes et Conversion
df_model <- df_model %>%
  mutate(
    # Remplacement des textes manquants par "Non renseigné" AVANT factorisation
    implantation_station = ifelse(is.na(implantation_station) | implantation_station == "", "Non renseigné", implantation_station),
    condition_acces = ifelse(is.na(condition_acces) | condition_acces == "", "Non renseigné", condition_acces),
    
    # Remplacement des booléens manquants par FALSE (on suppose que si ce n'est pas précisé, c'est que la borne n'a pas l'option)
    charge_rapide = ifelse(is.na(charge_rapide), FALSE, charge_rapide),
    gratuit = ifelse(is.na(gratuit), FALSE, gratuit),
    paiement_cb = ifelse(is.na(paiement_cb), FALSE, paiement_cb),
    ouvert_24_7 = ifelse(is.na(ouvert_24_7), FALSE, ouvert_24_7),
    prise_type_combo_ccs = ifelse(is.na(prise_type_combo_ccs), FALSE, prise_type_combo_ccs),
    prise_type_chademo = ifelse(is.na(prise_type_chademo), FALSE, prise_type_chademo),
    
    # Remplacement des numériques par la médiane
    puissance_nominale = ifelse(is.na(puissance_nominale), median(puissance_nominale, na.rm = TRUE), puissance_nominale),
    nbre_pdc = ifelse(is.na(nbre_pdc), median(nbre_pdc, na.rm = TRUE), nbre_pdc)
  ) %>%
  # Une fois les trous bouchés, on convertit proprement en facteurs
  mutate(
    charge_rapide = as.factor(as.logical(charge_rapide)),
    gratuit = as.factor(as.logical(gratuit)),
    paiement_cb = as.factor(as.logical(paiement_cb)),
    ouvert_24_7 = as.factor(as.logical(ouvert_24_7)),
    implantation_station = as.factor(implantation_station),
    condition_acces = as.factor(condition_acces),
    prise_type_combo_ccs = as.factor(as.logical(prise_type_combo_ccs)),
    prise_type_chademo = as.factor(as.logical(prise_type_chademo))
  )

# Sélection des colonnes utiles
# On garde les variables cibles et explicatives (sans supprimer les lignes !)
df_clean <- df_model %>%
  select(tarification_groupe, puissance_nominale, nbre_pdc, 
         charge_rapide, paiement_cb, ouvert_24_7,
         implantation_station,       
         condition_acces,            
         prise_type_combo_ccs,       
         prise_type_chademo,
         operateur_groupe
         ) 

# Séparation des données : Connus vs Inconnus pour le modèle
df_connu <- df_clean %>% filter(tarification_groupe != "Inconnu")
df_inconnu <- df_clean %>% filter(tarification_groupe == "Inconnu")

# Nettoyage des niveaux de facteurs
df_connu$tarification_groupe <- droplevels(df_connu$tarification_groupe)

# --- Analyse Diagnostique : Opérateurs dans les données Inconnues ---
cat("\n--- Top Opérateurs dans df_inconnu ---\n")
df_inconnu %>%
  count(operateur_groupe, sort = TRUE) %>%
  head(15) %>%
  print()

cat("\n--- Distribution des tarifs pour ces mêmes Opérateurs dans df_connu ---\n")
df_connu %>%
  count(operateur_groupe, tarification_groupe) %>%
  group_by(operateur_groupe) %>%
  mutate(pct = round(n / sum(n) * 100, 1)) %>%
  filter(operateur_groupe %in% head(df_inconnu %>% count(operateur_groupe, sort=TRUE) %>% pull(operateur_groupe), 5)) %>%
  print()

# Séparation Train / Test UNIQUEMENT sur les tarifs connus
set.seed(43)
index_train <- createDataPartition(df_connu$tarification_groupe, p = 0.8, list = FALSE)
train_data <- df_connu[index_train, ]
test_data  <- df_connu[-index_train, ]


# Régression Logistique Multinomiale (Tarification)

# Entraînement du modèle (multinom pour 3 classes)
modele_logistique <- multinom(
  tarification_groupe ~ charge_rapide + nbre_pdc + ouvert_24_7 + paiement_cb + 
    puissance_nominale + implantation_station + condition_acces + 
    prise_type_combo_ccs + prise_type_chademo + operateur_groupe,
  data = train_data
)

# Affichage d'un résumé du modèle
print(summary(modele_logistique))

# Prédiction sur le jeu de Test
predictions_tarif <- predict(modele_logistique, newdata = test_data)

# Évaluation : MATRICE DE CONFUSION !
cat("\n--- Matrice de Confusion (Évaluation du modèle) ---\n")
matrice_confusion <- confusionMatrix(predictions_tarif, test_data$tarification_groupe)
print(matrice_confusion)

# --- Représentation Graphique du Modèle 1 ---

# Graphique A : Heatmap de la Matrice de Confusion
matrice_df <- as.data.frame(matrice_confusion$table)
p_conf <- ggplot(data = matrice_df, aes(x = Reference, y = Prediction)) +
  geom_tile(aes(fill = Freq), color = "white") +
  scale_fill_gradient(low = "#f8f9fa", high = "#3498db") +
  geom_text(aes(label = Freq), fontface = "bold", size = 5) +
  theme_minimal() +
  labs(title = "Modèle 1 : Matrice de Confusion (Performance)",
       subtitle = "Comparaison entre les vrais tarifs et ceux prédits par l'IA",
       x = "Tarification Réelle",
       y = "Tarification Prédite",
       fill = "Nombre")
print(p_conf)

# Application : Deviner le tarif des stations "Inconnu"
cat("\n--- Application : Remplissage des tarifs 'Inconnus' ---\n")
probs <- predict(modele_logistique, newdata = df_inconnu, type = "probs")
predictions_inconnus <- apply(probs[, c("Modéré", "Élevé")], 1, 
                               function(x) names(which.max(x)))
cat("Voici la répartition estimée par le modèle pour les bornes dont le tarif n'était pas affiché :\n")
print(table(predictions_inconnus))

#  Barplot des tarifs "devinés"
df_inconnu$prediction <- predictions_inconnus
p_inconnu <- ggplot(df_inconnu, aes(x = prediction, fill = prediction)) +
  geom_bar(alpha = 0.9) +
  theme_minimal() +
  scale_fill_brewer(palette = "Set1") +
  labs(title = "Modèle 1 : Tarifs estimés pour les stations 'Inconnu'",
       subtitle = "L'intelligence artificielle a rempli les trous !",
       x = "Tarification Estimée par l'IA",
       y = "Nombre de Stations") +
  theme(legend.position = "none")
print(p_inconnu)


#  Régression Linéaire Multiple 

# Entraînement du modèle de régression linéaire (Uniquement sur les vraies données connues)
modele_lineaire <- lm(puissance_nominale ~ nbre_pdc + charge_rapide + ouvert_24_7 + tarification_groupe +
                        implantation_station + prise_type_combo_ccs + prise_type_chademo + operateur_groupe, data = train_data)

# Affichage des coefficients et des p-values 
print(summary(modele_lineaire))

# Prédiction sur le jeu de test
predictions_puissance <- predict(modele_lineaire, newdata = test_data)

# Évaluation du modèle
# Calcul du RMSE et du R²
rmse <- sqrt(mean((test_data$puissance_nominale - predictions_puissance)^2))
r_carre <- cor(test_data$puissance_nominale, predictions_puissance)^2

cat("\n--- Performances du Modèle Linéaire ---\n")
cat("RMSE (Erreur moyenne en kW) :", round(rmse, 2), "\n")
cat("R-carré (Variance expliquée) :", round(r_carre, 4), "\n")

# Graphique de comparaison : Valeurs Réelles vs Prédictions
p_pred <- ggplot(data.frame(Reel = test_data$puissance_nominale, Predit = predictions_puissance), aes(x = Reel, y = Predit)) +
  geom_point(alpha = 0.5, color = "darkblue") +
  geom_abline(intercept = 0, slope = 1, color = "red", linetype = "dashed", linewidth = 1) +
  theme_minimal() +
  labs(title = "Régression Linéaire : Puissance Réelle vs Prédite",
       subtitle = "La ligne rouge pointillée représente une prédiction parfaite",
       x = "Puissance Réelle (kW)",
       y = "Puissance Prédite (kW)")

print(p_pred)

