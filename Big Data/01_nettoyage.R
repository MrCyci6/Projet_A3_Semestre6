library(data.table)
library(stringr)

data <- fread("D:/COURS/A3/Projet A3 Semestre 6/Big Data/data/IRVE.csv",
              encoding = "UTF-8",
              na.strings = c("", "NA", "NULL", "null"),
              colClasses = list(character = c("consolidated_code_postal", "code_insee_commune")))

cat("Dimensions initiales :", nrow(data), "lignes x", ncol(data), "colonnes\n")

# Deduplication sur id_pdc_itinerance
# D'abord les lignes 100% identiques, puis 1 ligne par id_pdc_itinerance (la plus recente si date_maj existe)
n_avant <- nrow(data)
data <- unique(data)
if ("date_maj" %in% names(data)) setorder(data, -date_maj)
data <- unique(data, by = "id_pdc_itinerance")
cat("Doublons supprimes :", n_avant - nrow(data), "\n")

# Filtre France metropolitaine (bounding box + exclusion DOM-TOM par code INSEE)
n_avant <- nrow(data)
data <- data[
  consolidated_longitude >= -5.2 & consolidated_longitude <= 9.7 &
  consolidated_latitude  >= 41.3 & consolidated_latitude  <= 51.1 &
  (is.na(code_insee_commune) | !str_detect(code_insee_commune, "^9[78]"))
]
cat("Lignes hors metropole supprimees :", n_avant - nrow(data), "\n")

# Filtre pays etrangers (Belgique, Allemagne, Luxembourg, etc.)
# CP francais : exactement 5 chiffres, departement 01-95 ou 2A/2B
# INSEE francais : exactement 5 caracteres, departement 01-95 ou 2A/2B
cp_fr    <- "^(0[1-9]|[1-8][0-9]|9[0-5]|2[AB])\\d{3}$"
insee_fr <- "^(0[1-9]|[1-8][0-9]|9[0-5]|2[AB])\\d{3}$"
n_avant <- nrow(data)
data <- data[
  (!is.na(code_insee_commune) & str_detect(code_insee_commune, insee_fr)) |
  (!is.na(consolidated_code_postal) & str_detect(consolidated_code_postal, cp_fr))
]
cat("Lignes etrangeres supprimees :", n_avant - nrow(data), "\n")

# Validation des coordonnees pour les lignes consolidated_is_lon_lat_correct == FALSE
# On envoie les coords a l'API adresse.data.gouv.fr en reverse-geocoding
# et on compare CP / commune / score pour decider si on garde ou supprime
idx_false <- which(data$consolidated_is_lon_lat_correct == FALSE |
                   is.na(data$consolidated_is_lon_lat_correct))
cat("Coordonnees a verifier (FALSE) :", length(idx_false), "\n")

if (length(idx_false) > 0) {
  a_verifier <- data[idx_false, .(
    latitude     = consolidated_latitude,
    longitude    = consolidated_longitude,
    cp_declare   = as.character(consolidated_code_postal),
    comm_declare = consolidated_commune
  )]

  taille_lot <- 5000
  lots <- split(seq_len(nrow(a_verifier)), ceiling(seq_len(nrow(a_verifier)) / taille_lot))
  res_cp    <- vector("list", length(lots))
  res_city  <- vector("list", length(lots))

  cat("Reverse-geocoding en", length(lots), "lot(s)...\n")
  for (i in seq_along(lots)) {
    lot <- a_verifier[lots[[i]]]
    tmp_in  <- tempfile(fileext = ".csv")
    tmp_out <- tempfile(fileext = ".csv")
    fwrite(lot[, .(latitude, longitude)], tmp_in)

    resp <- httr::POST(
      url = "https://api-adresse.data.gouv.fr/reverse/csv/",
      body = list(data = httr::upload_file(tmp_in)),
      encode = "multipart"
    )

    if (httr::status_code(resp) == 200) {
      writeBin(httr::content(resp, "raw"), tmp_out)
      res <- fread(tmp_out, encoding = "UTF-8", colClasses = list(character = "result_postcode"))
      res_cp[[i]]    <- res$result_postcode
      res_city[[i]]  <- res$result_city
    } else {
      cat("  Lot", i, ": erreur HTTP", httr::status_code(resp), "\n")
      n_lot <- length(lots[[i]])
      res_cp[[i]]    <- rep(NA_character_, n_lot)
      res_city[[i]]  <- rep(NA_character_, n_lot)
    }

    file.remove(tmp_in, tmp_out)
    if (i < length(lots)) Sys.sleep(1)
  }

  a_verifier[, cp_reverse   := unlist(res_cp)]
  a_verifier[, city_reverse := unlist(res_city)]
  norm_str <- function(x) tolower(stringi::stri_trans_general(x, "Latin-ASCII"))

  a_verifier[, coord_validee := FALSE]

  # 1) CP exact match -> on garde
  a_verifier[!is.na(cp_reverse) & !is.na(cp_declare) & cp_reverse == cp_declare, coord_validee := TRUE]

  # 2) CP different mais commune match -> on garde
  a_verifier[coord_validee == FALSE & !is.na(city_reverse) & !is.na(comm_declare) & norm_str(city_reverse) == norm_str(comm_declare), coord_validee := TRUE]


  n_recuperees <- sum(a_verifier$coord_validee)
  n_supprimees <- sum(!a_verifier$coord_validee)
  cat("Coordonnees FALSE recuperees :", n_recuperees, "\n")
  cat("Coordonnees FALSE supprimees :", n_supprimees, "\n")

  data <- data[-idx_false[!a_verifier$coord_validee]]
}

# Suppression des colonnes de metadonnees de consolidation
cols_meta <- intersect(c("consolidated_is_lon_lat_correct",
                         "consolidated_is_code_insee_verified",
                         "consolidated_is_code_insee_modified"), names(data))
data[, (cols_meta) := NULL]

cat("\n--- VERIFICATION ---\n")
cat("Lignes restantes :", nrow(data), "\n")
cat("Doublons id_pdc_itinerance (doit etre 0) :", sum(duplicated(data, by = "id_pdc_itinerance")), "\n")
cat("Stations distinctes :", uniqueN(data$id_station_itinerance), "| PDC :", nrow(data), "\n")

fwrite(data, "D:/COURS/A3/Projet A3 Semestre 6/Big Data/data/IRVE_clean.csv", bom = FALSE)
cat("Fichier ecrit dans ./data/IRVE_clean.csv\n")