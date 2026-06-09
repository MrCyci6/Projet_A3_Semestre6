library(data.table)

# Importation avec fread
df <- fread("IRVE_clean.csv")

dim(df)

# Voir le type de chaque variable (entier, caractère, facteur, etc.)
str(df)
# Le package 'skimr' offre un excellent résumé global très lisible
library(skimr)
skim(df)

# --- Variables numériques ---
# Identifier toutes les variables numériques
vars_num <- names(df)[sapply(df, is.numeric)]

# Résumé classique pour toutes les variables numériques
print(summary(df[, .SD, .SDcols = vars_num]))

# Mesures de dispersion spécifiques pour toutes les variables numériques
print("Écart-types :")
print(df[, lapply(.SD, sd, na.rm = TRUE), .SDcols = vars_num])

print("Variances :")
print(df[, lapply(.SD, var, na.rm = TRUE), .SDcols = vars_num])

print("Écarts interquartiles :")
print(df[, lapply(.SD, IQR, na.rm = TRUE), .SDcols = vars_num])

library(ggplot2)

# Boucle pour générer les graphiques pour chaque variable numérique
for (var in vars_num) {
  # Histogramme pour voir la distribution
  p_hist <- ggplot(df, aes(x = .data[[var]])) +
    geom_histogram(bins = 50, fill = "steelblue", color = "white") +
    theme_minimal() +
    labs(title = paste("Distribution de :", var), x = var, y = "Fréquence")
  print(p_hist)
  
  # Boîte à moustaches (Boxplot) pour repérer les valeurs atypiques (outliers)
  p_box <- ggplot(df, aes(y = .data[[var]])) +
    geom_boxplot(fill = "lightblue") +
    theme_minimal() +
    labs(title = paste("Boxplot de :", var), y = var)
  print(p_box)
}

# --- Variables catégorielles ---
# Identifier toutes les variables catégorielles (caractère ou facteur)
# On s'assure de ne prendre que les variables ayant moins de 50 catégories uniques pour éviter de bloquer les graphiques
vars_cat <- names(df)[sapply(df, function(x) {
  (is.character(x) | is.factor(x)) && length(unique(x[!is.na(x)])) < 50
})]

# Boucle pour générer les tableaux et graphiques pour chaque variable catégorielle
for (var in vars_cat) {
  cat("\n--- Variable catégorielle :", var, "---\n")
  
  # Tableau des effectifs absolus
  effectifs <- table(df[[var]], useNA = "ifany") # useNA permet de voir les valeurs manquantes
  print(effectifs)
  
  # Tableau des fréquences relatives (pourcentages)
  proportions <- prop.table(effectifs) * 100
  print(round(proportions, 2))
  
  # Diagramme en barres
  p_bar <- ggplot(df, aes(x = .data[[var]])) +
    geom_bar(fill = "coral") +
    theme_minimal() +
    labs(title = paste("Répartition de :", var), x = var, y = "Nombre d'observations") +
    coord_flip() # Utile si les noms des catégories sont longs
  print(p_bar)
}

# --- Valeurs manquantes ---
# Pourcentage de NA pour chaque colonne de toute la base
print("Pourcentage de NA par colonne :")
print(sapply(df, function(x) sum(is.na(x)) / length(x) * 100))
