
library(data.table)
library(stringr)

# Supprime une ou plusieurs colonnes de `data` (par reference).
# Les noms absents sont ignores (pas d'erreur).
supprimer_colonne <- function(...) {
  cols <- intersect(c(...), names(data))
  if (length(cols)) data[, (cols) := NULL]
  invisible(data)
}

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
data <- fread("D:/COURS/A3/Projet A3 Semestre 6/Big Data/data/IRVE.csv", encoding = "UTF-8", na.strings = c("", "NA", "NULL", "null"), colClasses = list(character = c("consolidated_code_postal", "code_insee_commune")))

# nb ligne et colonne
dim(data); str(data)
# nb NA par colonne
print(sort(colSums(is.na(data)), decreasing = TRUE))

# Correction des accents / encodage
# Reparation des "e accent grave" corrompus dans toutes les colonnes texte.
#  et ¸ sont les caracteres qui ont remplace "è" dans ~240 lignes.
cols_txt <- names(data)[sapply(data, is.character)]
data[, (cols_txt) := lapply(.SD, function(x) {
  x <- gsub("", "è", x, fixed = TRUE)   # "Accs"  -> "Accès" (octet c2 8f)
  x <- gsub("¸", "è", x)   # "Acc¸s" -> "Accès" (octet c2 b8)
  x <- gsub("", "é", x)   # "é" corrompu (octet c2 8e)
  x <- gsub("ˇ", "é", x)   # "é" corrompu, caron (octet cb 87)
  x
}), .SDcols = cols_txt]

# Normalisation des categories de condition_acces (insensible a l'encodage :
# on matche sur la partie ASCII "libre" / "serv" qui n'est jamais accentuee)
data[str_detect(condition_acces, regex("libre", ignore_case = TRUE)),
     condition_acces := "Accès libre"]
data[str_detect(condition_acces, regex("serv", ignore_case = TRUE)),
     condition_acces := "Accès réservé"]

# Normalisation de accessibilite_pmr (fcase = 1er match gagne, evite de se reecraser
# car les valeurs canoniques contiennent "serv")
data[, accessibilite_pmr := fcase(
  str_detect(accessibilite_pmr, regex("inconnu",  ignore_case = TRUE)), "Accessibilité inconnue",
  str_detect(accessibilite_pmr, regex("mais non", ignore_case = TRUE)), "Accessible mais non réservé PMR",
  str_detect(accessibilite_pmr, regex("^\\s*Non",  ignore_case = TRUE)), "Non accessible",
  str_detect(accessibilite_pmr, regex("serv",     ignore_case = TRUE)), "Réservé PMR",
  default = accessibilite_pmr
)]

# Normalisation de implantation_station (ordre : "usage public" avant "public" seul)
data[, implantation_station := fcase(
  str_detect(implantation_station, regex("voirie",       ignore_case = TRUE)), "Voirie",
  str_detect(implantation_station, regex("rapide",       ignore_case = TRUE)), "Station dédiée à la recharge rapide",
  str_detect(implantation_station, regex("client",       ignore_case = TRUE)), "Parking privé réservé à la clientèle",
  str_detect(implantation_station, regex("usage public", ignore_case = TRUE)), "Parking privé à usage public",
  str_detect(implantation_station, regex("public",       ignore_case = TRUE)), "Parking public",
  default = implantation_station
)]

# Normalisation de raccordement (ordre : "indirect" avant "direct", sinon ecrasement)
data[, raccordement := fcase(
  str_detect(raccordement, regex("indirect", ignore_case = TRUE)), "Indirect",
  str_detect(raccordement, regex("direct",   ignore_case = TRUE)), "Direct",
  default = raccordement
)]

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

# France metropolitaine uniquement : coords presentes + box (metropole + Corse)
# + exclusion des DOM par code INSEE (departements 97x / 98x)
n_avant_geo <- nrow(data)
data <- data[
  !is.na(consolidated_longitude) & !is.na(consolidated_latitude) &
  consolidated_longitude >= -5.2 & consolidated_longitude <= 9.7 &
  consolidated_latitude  >= 41.3 & consolidated_latitude  <= 51.1 &
  (is.na(code_insee_commune) | !str_detect(code_insee_commune, "^9[78]"))
]
cat("Bornes hors metropole supprimees :", n_avant_geo - nrow(data), "\n")

data[, date_mise_en_service := as.IDate(date_mise_en_service)]
data[date_mise_en_service > Sys.Date() | date_mise_en_service < as.IDate("2010-01-01"), date_mise_en_service := NA]

data[, adresse_station := str_squish(str_remove_all(str_replace_all(adresse_station, "\\]\\s*\\[", " "), "[\\[\\]]"))]

data[, cp_adresse := str_extract(adresse_station, "\\b\\d{5}\\b")]          # 5 chiffres
data[, commune_adresse := str_squish(str_extract(adresse_station, "(?<=\\d{5}\\s).*$"))]  # texte après le CP
data[, consolidated_code_postal := as.character(consolidated_code_postal)]

data[is.na(consolidated_code_postal), consolidated_code_postal := cp_adresse]
data[is.na(consolidated_commune),     consolidated_commune     := commune_adresse]

data[, c("cp_adresse", "commune_adresse") := NULL]

# Telephone : format international unique "+..." (vides -> NA)
normaliser_tel <- function(x) {
  x <- str_remove_all(x, "[^0-9+]")            # ne garder que les chiffres et le +
  x <- str_replace_all(x, "(?<=.)\\+", "")     # un seul + autorise, en tete
  x <- str_replace(x, "^00", "+")              # prefixe international 00... -> +...
  x <- str_replace(x, "^0(\\d{9})$", "+33\\1") # national FR 0X... (10 chiffres) -> +33X...
  x <- str_replace(x, "^(\\d{9})$", "+33\\1")  # numero a 9 chiffres -> +33...
  x[is.na(x) | x == ""] <- "+33000000000"      # vide / NA -> numero factice
  x
}
data[, telephone_operateur := normaliser_tel(telephone_operateur)]

# Horaires
jours_ordre <- c("Lu","Ma","Me","Je","Ve","Sa","Di")

normaliser_horaires <- function(h) {
  h <- str_squish(h)
  h <- str_replace_all(h, "\\s+:\\s+", " ")                       # "Lun-Ven : 08:00" -> ...
  h <- str_replace_all(h, "00:00-24:00|00:00-00:00|00:00-23:5[0-9]", "00:00-23:59")
  h <- str_replace_all(h, "24:00", "23:59")
  h <- str_replace(h, "^24/7$", "Lu-Di 00:00-23:59")
  trad <- c("Mon"="Lu","Tue"="Ma","Wed"="Me","Thu"="Je","Fri"="Ve","Sat"="Sa","Sun"="Di","Lun"="Lu","Mar"="Ma","Mer"="Me","Jeu"="Je","Ven"="Ve","Sam"="Sa","Dim"="Di","Mo"="Lu","Tu"="Ma","We"="Me","Th"="Je","Fr"="Ve","Sa"="Sa","Su"="Di")
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
  if (!nrow(m)) return(h)                       # rien de reconnaissable -> tel quel
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
map  <- setNames(vapply(uniq, function(x) formater_horaires(normaliser_horaires(x)),character(1)), uniq)
data[!is.na(horaires), horaires := map[horaires]]

supprimer_colonne("id_pdc_local")
supprimer_colonne("id_station_local")

cat("\n--- VERIFICATION ---\n")
cat("Lignes finales :", nrow(data), "\n")

fwrite(data, "D:/COURS/A3/Projet A3 Semestre 6/Big Data/data/IRVE_clean.csv", bom = TRUE)
cat("Fichier nettoye ecrit dans ./data/IRVE_clean.csv\n")
