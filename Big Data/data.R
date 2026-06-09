
library(data.table)
library(stringr)

# Read CSV
data <- fread("./data/IRVE.csv", encoding = "UTF-8", na.strings = c("", "NA", "NULL", "null"))

# Nb ligne & colonnes
dim(data)
str(data)

na_par_col <- sort(colSums(is.na(data)), decreasing = TRUE)
print(na_par_col)

summary(data$puissance_nominale)
summary(data$nbre_pdc)

# Suppression des doublons
data <- unique(data)

# Trier du plus au moins récent
if ("date_maj" %in% names(data)) {
  setorder(data, -date_maj)
}

# Dédoublonnage de id_pdc
data <- data[!duplicated(id_pdc_itinerance) | is.na(id_pdc_itinerance)]

# Supprimer les lignes avec id_pdc null
data <- data[!is.na(id_pdc_itinerance)]

# Correction des puissances
data[puissance_nominale > 1000, puissance_nominale := puissance_nominale / 1000]
data[puissance_nominale <= 0 | puissance_nominale > 400, puissance_nominale := NA]

data <- data[is.na(consolidated_longitude) | (consolidated_longitude >= -5.5 & consolidated_longitude <= 9.8 & consolidated_latitude  >= 41   & consolidated_latitude  <= 51.5)]

data[, date_mise_en_service := as.IDate(date_mise_en_service)]
data[date_mise_en_service > Sys.Date() | date_mise_en_service < as.IDate("2010-01-01"), date_mise_en_service := NA]


fwrite(data, "./data/IRVE_clean.csv")
cat("Fichier nettoyé écrit dans ./data/IRVE_clean.csv\n")
