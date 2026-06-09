library(data.table)
library(stringr)

data <- fread("D:/COURS/A3/Projet A3 Semestre 6/Big Data/data/IRVE_clean.csv",
              encoding = "UTF-8",
              na.strings = c("", "NA", "NULL", "null"),
              colClasses = list(character = c("consolidated_code_postal", "code_insee_commune")))

cat("Dimensions :", nrow(data), "lignes x", ncol(data), "colonnes\n")

################################################################################################
# ENCODAGE / ACCENTS
################################################################################################

cols_txt <- names(data)[sapply(data, is.character)]
data[, (cols_txt) := lapply(.SD, function(x) {
  x <- gsub("\u008f", "\u00e8", x, fixed = TRUE)  # e accent grave corrompu
  x <- gsub("\u00b8", "\u00e8", x)                 # cedille -> e accent grave
  x <- gsub("\u008e", "\u00e9", x, fixed = TRUE)  # e accent aigu corrompu
  x <- gsub("\u02c7", "\u00e9", x)                 # caron -> e accent aigu
  x
}), .SDcols = cols_txt]

################################################################################################
# COLONNES CATEGORIELLES
################################################################################################

# condition_acces
data[str_detect(condition_acces, regex("libre", ignore_case = TRUE)), condition_acces := "Acc\u00e8s libre"]
data[str_detect(condition_acces, regex("serv", ignore_case = TRUE)), condition_acces := "Acc\u00e8s r\u00e9serv\u00e9"]

# accessibilite_pmr
data[, accessibilite_pmr := fcase(
  str_detect(accessibilite_pmr, regex("inconnu",  ignore_case = TRUE)), "Accessibilit\u00e9 inconnue",
  str_detect(accessibilite_pmr, regex("mais non", ignore_case = TRUE)), "Accessible mais non r\u00e9serv\u00e9 PMR",
  str_detect(accessibilite_pmr, regex("^\\s*Non",  ignore_case = TRUE)), "Non accessible",
  str_detect(accessibilite_pmr, regex("serv",     ignore_case = TRUE)), "R\u00e9serv\u00e9 PMR",
  default = accessibilite_pmr
)]

# implantation_station
data[, implantation_station := fcase(
  str_detect(implantation_station, regex("voirie",       ignore_case = TRUE)), "Voirie",
  str_detect(implantation_station, regex("rapide",       ignore_case = TRUE)), "Station d\u00e9di\u00e9e \u00e0 la recharge rapide",
  str_detect(implantation_station, regex("client",       ignore_case = TRUE)), "Parking priv\u00e9 r\u00e9serv\u00e9 \u00e0 la client\u00e8le",
  str_detect(implantation_station, regex("usage public", ignore_case = TRUE)), "Parking priv\u00e9 \u00e0 usage public",
  str_detect(implantation_station, regex("public",       ignore_case = TRUE)), "Parking public",
  default = implantation_station
)]

# raccordement
data[, raccordement := fcase(
  str_detect(raccordement, regex("indirect", ignore_case = TRUE)), "Indirect",
  str_detect(raccordement, regex("direct",   ignore_case = TRUE)), "Direct",
  default = raccordement
)]

################################################################################################
# COLONNES BOOLEENNES
################################################################################################

cols_bool <- c(
  "gratuit", "paiement_acte", "paiement_cb", "paiement_autre",
  "reservation", "station_deux_roues", "cable_t2_attache",
  "prise_type_ef", "prise_type_2", "prise_type_combo_ccs",
  "prise_type_chademo", "prise_type_autre"
)
cols_bool <- intersect(cols_bool, names(data))

vals_true  <- c("true", "True", "TRUE", "1", "oui", "OUI", "Oui")
vals_false <- c("false", "False", "FALSE", "0", "non", "NON", "Non")

data[, (cols_bool) := lapply(.SD, function(x) {
  x <- as.character(x)
  fcase(
    x %in% vals_true,  TRUE,
    x %in% vals_false, FALSE,
    is.na(x),          FALSE,
    default = NA
  )
}), .SDcols = cols_bool]

################################################################################################
# ADRESSE
################################################################################################

# Nettoyage crochets et espaces multiples
data[, adresse_station := str_squish(str_remove_all(
  str_replace_all(adresse_station, "\\]\\s*\\[", " "), "[\\[\\]]"
))]

# Completer CP et commune manquants a partir de l'adresse
data[, consolidated_code_postal := as.character(consolidated_code_postal)]
data[, cp_adresse := str_extract(adresse_station, "\\b\\d{5}\\b")]
data[, commune_adresse := str_squish(str_extract(adresse_station, "(?<=\\d{5}\\s).*$"))]

data[is.na(consolidated_code_postal), consolidated_code_postal := cp_adresse]
data[is.na(consolidated_commune),     consolidated_commune     := commune_adresse]

data[, c("cp_adresse", "commune_adresse") := NULL]

################################################################################################
# TELEPHONE
################################################################################################

data[, telephone_operateur := {
  x <- str_remove_all(telephone_operateur, "[^0-9+]")
  x <- str_replace_all(x, "(?<=.)\\+", "")
  x <- str_replace(x, "^00", "+")
  x <- str_replace(x, "^0(\\d{9})$", "+33\\1")
  x <- str_replace(x, "^(\\d{9})$", "+33\\1")
  x[is.na(x) | x == ""] <- NA_character_
  x
}]

################################################################################################
# HORAIRES
################################################################################################

jours_ordre <- c("Lu","Ma","Me","Je","Ve","Sa","Di")

normaliser_horaires <- function(h) {
  h <- str_squish(h)
  h <- str_replace_all(h, "\\s+:\\s+", " ")
  h <- str_replace_all(h, "00:00-24:00|00:00-00:00|00:00-23:5[0-9]", "00:00-23:59")
  h <- str_replace_all(h, "24:00", "23:59")
  h <- str_replace(h, "^24/7$", "Lu-Di 00:00-23:59")
  h <- str_replace(h, "^(\\d{2}:\\d{2}-\\d{2}:\\d{2})$", "Lu-Di \\1")
  trad <- c("Mon"="Lu","Tue"="Ma","Wed"="Me","Thu"="Je","Fri"="Ve","Sat"="Sa","Sun"="Di",
            "Lun"="Lu","Mar"="Ma","Mer"="Me","Jeu"="Je","Ven"="Ve","Sam"="Sa","Dim"="Di",
            "Mo"="Lu","Tu"="Ma","We"="Me","Th"="Je","Fr"="Ve","Sa"="Sa","Su"="Di")
  for (j in names(trad)) h <- str_replace_all(h, paste0("\\b", j, "\\b"), trad[[j]])
  str_squish(h)
}

expand_jours <- function(expr) {
  out <- character(0)
  for (p in str_squish(str_split(expr, ",")[[1]])) {
    if (str_detect(p, "-")) {
      b <- str_squish(str_split(p, "-")[[1]])
      i1 <- match(b[1], jours_ordre); i2 <- match(b[2], jours_ordre)
      if (!is.na(i1) && !is.na(i2)) out <- c(out, jours_ordre[i1:i2])
    } else if (p %in% jours_ordre) out <- c(out, p)
  }
  out
}

compress_jours <- function(js) {
  idx <- sort(unique(match(js, jours_ordre))); idx <- idx[!is.na(idx)]
  if (!length(idx)) return(NA_character_)
  groupes <- split(idx, cumsum(c(1, diff(idx) != 1)))
  morceaux <- vapply(groupes, function(g)
    if (length(g) == 1) jours_ordre[g]
    else paste0(jours_ordre[g[1]], "-", jours_ordre[g[length(g)]]),
    character(1))
  paste(morceaux, collapse = ", ")
}

formater_horaires <- function(h) {
  if (is.na(h) || str_squish(h) == "") return(NA_character_)
  m <- str_match_all(h, "((?:Lu|Ma|Me|Je|Ve|Sa|Di|[\\s,\\-])+?)\\s*(\\d{2}:\\d{2}-\\d{2}:\\d{2})")[[1]]
  if (!nrow(m)) return(h)
  paires <- do.call(rbind, lapply(seq_len(nrow(m)), function(i) {
    js <- expand_jours(m[i, 2]); if (!length(js)) js <- jours_ordre
    data.frame(jour = js, plage = m[i, 3], stringsAsFactors = FALSE)
  }))
  paires <- unique(paires)
  res <- lapply(unique(paires$plage), function(pl) {
    js <- paires$jour[paires$plage == pl]
    list(txt = paste(compress_jours(js), pl),
         premier = min(match(js, jours_ordre)), debut = pl)
  })
  ord <- order(vapply(res, `[[`, 1, "premier"), vapply(res, `[[`, "", "debut"))
  paste(vapply(res[ord], `[[`, "", "txt"), collapse = ", ")
}

uniq <- unique(data$horaires)
map  <- setNames(vapply(uniq, function(x) formater_horaires(normaliser_horaires(x)), character(1)), uniq)
data[!is.na(horaires), horaires := map[horaires]]

################################################################################################
# VALEURS ABERRANTES
################################################################################################

# Puissance : correction W -> kW, puis bornes realistes
data[puissance_nominale > 1000, puissance_nominale := puissance_nominale / 1000]
data[puissance_nominale <= 0 | puissance_nominale > 400, puissance_nominale := NA]

# Date de mise en service : dates aberrantes -> NA
data[, date_mise_en_service := as.IDate(date_mise_en_service)]
data[date_mise_en_service > Sys.Date() | date_mise_en_service < as.IDate("2010-01-01"),
     date_mise_en_service := NA]

################################################################################################
# SUPPRESSION COLONNES INUTILES
################################################################################################

cols_suppr <- intersect(c(
  "datagouv_dataset_id", "datagouv_resource_id", "datagouv_organization_or_owner",
  "id_pdc_local", "id_station_local", "coordonneesXY"
), names(data))
if (length(cols_suppr)) data[, (cols_suppr) := NULL]

################################################################################################
# FEATURE ENGINEERING
################################################################################################

data[, charge_rapide  := puissance_nominale >= 50]
data[, ouvert_24_7    := horaires == "Lu-Di 00:00-23:59"]
data[, nb_types_prise := rowSums(.SD, na.rm = TRUE),
     .SDcols = intersect(c("prise_type_ef", "prise_type_2", "prise_type_combo_ccs",
                            "prise_type_chademo", "prise_type_autre"), names(data))]

################################################################################################
# VERIFICATION ET EXPORT
################################################################################################

cat("\n--- VERIFICATION ---\n")
cat("Lignes finales :", nrow(data), "\n")
cat("Colonnes       :", ncol(data), "\n")
cat("Doublons id_pdc (doit etre 0) :",
    sum(duplicated(data, by = "id_pdc_itinerance")), "\n")
cat("Stations distinctes :", uniqueN(data$id_station_itinerance),
    "| PDC :", nrow(data), "\n")

fwrite(data, "D:/COURS/A3/Projet A3 Semestre 6/Big Data/data/IRVE_formatted.csv", bom = FALSE)
cat("Fichier formate ecrit dans ./data/IRVE_formatted.csv\n")
