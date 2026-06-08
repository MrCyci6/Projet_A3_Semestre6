
library(data.table)
library(stringr)

cols_a_supprimer <- c(
  "contact_amenageur", "contact_operateur", "telephone_operateur",
  "num_pdl", "observations",
  "datagouv_dataset_id", "datagouv_resource_id",
  "datagouv_organization_or_owner", "id_station_local", "id_pdc_local"
)

cols_a_normaliser <- c(
  "gratuit", "paiement_acte", "paiement_cb", "paiement_autre",
  "reservation", "station_deux_roues", "cable_t2_attache",
  "prise_type_ef", "prise_type_2", "prise_type_combo_ccs",
  "prise_type_chademo", "prise_type_autre"
)
regles_remplacement <- list(
  "FALSE" = c("false", "False", "0", "non", "NON", "Non", NA),
  "TRUE"  = c("true",  "True",  "1", "oui", "OUI", "Oui")
)

cols_cle_doublons <- c("id_pdc_itinerance")

cols_obligatoires <- c("id_pdc_itinerance", "id_station_itinerance")

################################################################################################
data <- fread("./data/IRVE.csv", encoding = "UTF-8", na.strings = c("", "NA", "NULL", "null"))

# nb ligne et colonne
dim(data); str(data)
# nb NA par colonne
print(sort(colSums(is.na(data)), decreasing = TRUE))

# Suppresion
a_supprimer <- intersect(cols_a_supprimer, names(data))
if (length(a_supprimer)) data[, (a_supprimer) := NULL]

# Normalisation
a_normaliser <- intersect(cols_a_normaliser, names(data))

data[, (a_normaliser) := lapply(.SD, as.character), .SDcols = a_normaliser]
for (col in a_normaliser) {
  for (val_finale in names(regles_remplacement)) {
    vals <- regles_remplacement[[val_finale]]
    data[get(col) %in% vals, (col) := val_finale]
    if (any(is.na(vals)))
      data[is.na(get(col)), (col) := val_finale]
  }
}

# Doublons
data <- unique(data)
if ("date_maj" %in% names(data)) setorder(data, -date_maj)
data <- unique(data, by = cols_cle_doublons)

# Lignes obligatoires
for (col in intersect(cols_obligatoires, names(data))) {
  data <- data[!is.na(get(col))]
}

# Aberrations
data[puissance_nominale > 1000, puissance_nominale := puissance_nominale / 1000]
data[puissance_nominale <= 0 | puissance_nominale > 400, puissance_nominale := NA]

data <- data[is.na(consolidated_longitude) | (consolidated_longitude >= -5.5 & consolidated_longitude <= 9.8 & consolidated_latitude  >= 41   & consolidated_latitude  <= 51.5)]

data[, date_mise_en_service := as.IDate(date_mise_en_service)]
data[date_mise_en_service > Sys.Date() | date_mise_en_service < as.IDate("2010-01-01"), date_mise_en_service := NA]


cat("\n--- VERIFICATION ---\n")
cat("Lignes finales :", nrow(data), "\n")
cat("Doublons restants sur la cle :", sum(duplicated(data, by = cols_cle_doublons)), "\n")
for (col in intersect(cols_obligatoires, names(data))) {
  cat("NA restants dans", col, ":", sum(is.na(data[[col]])), "\n")
}
print(sort(colSums(is.na(data)), decreasing = TRUE))

fwrite(data, "./data/IRVE_clean.csv")
cat("Fichier nettoye ecrit dans ./data/IRVE_clean.csv\n")
