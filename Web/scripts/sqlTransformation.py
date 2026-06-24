import pandas as pd
import requests
import math

# ==========================================
# CONFIGURATION
# ==========================================
CSV_FILE = '../data/IRVE_formatted.csv'
OUTPUT_SQL_FILE = 'insertions_automatiques.sql'
GEO_API_URL = "https://geo.api.gouv.fr/communes/{}?fields=nom,codesPostaux,departement,region"

# ==========================================
# CACHES ET DICTIONNAIRES (Auto-Increment)
# ==========================================
cache_geo = {}

regions = {}
departements = {}
communes = {}

# Référentiels simples (Nom -> ID)
enseignes = {}
implantations = {}
raccordements = {}
restrictions = {}
accessibilites = {}
conditions = {}

# Référentiels complexes (Nom -> (ID, champ1, champ2...))
operateurs = {}
amenageurs = {}

# ==========================================
# FONCTIONS UTILITAIRES
# ==========================================
def escape_sql(value):
    """Échappe les apostrophes pour éviter de casser la requête SQL"""
    if pd.isna(value) or value == "":
        return "Non renseigné"
    return str(value).replace("'", "''")

def format_bool(value):
    """Convertit TRUE/FALSE en 1/0"""
    return 1 if str(value).strip().upper() == 'TRUE' else 0

def format_date(value):
    """Extrait la date YYYY-MM-DD"""
    if pd.isna(value) or str(value).strip() == "":
        return "1970-01-01"
    return str(value)[:10]

def format_datetime(value):
    """Convertit un format ISO (2025-06-18T03:41:20.122Z) en DATETIME MySQL"""
    if pd.isna(value) or str(value).strip() == "":
        return "1970-01-01 00:00:00"
    # Remplace le 'T' par un espace et coupe avant les millisecondes
    return str(value).replace('T', ' ')[:19]

def get_simple_id(val, dictionary):
    """Gère l'auto-incrément des tables de référence simples"""
    val = escape_sql(val)
    if val not in dictionary:
        dictionary[val] = len(dictionary) + 1
    return dictionary[val]

def get_geo_info(code_insee):
    """Interroge l'API Geo pour compléter la région et le département"""
    if code_insee in cache_geo:
        return cache_geo[code_insee]
    
    try:
        response = requests.get(GEO_API_URL.format(code_insee), timeout=5)
        if response.status_code == 200:
            data = response.json()
            info = {
                'nom_commune': data.get('nom', 'Inconnue'),
                'code_postal': data.get('codesPostaux', ['00000'])[0],
                'code_departement': data.get('departement', {}).get('code', '00'),
                'nom_departement': data.get('departement', {}).get('nom', 'Inconnu'),
                'nom_region': data.get('region', {}).get('nom', 'Inconnue')
            }
            cache_geo[code_insee] = info
            return info
    except:
        pass
    
    return {'nom_commune': 'Inconnue', 'code_postal': '00000', 'code_departement': '00', 'nom_departement': 'Inconnu', 'nom_region': 'Inconnue'}


# ==========================================
# SCRIPT PRINCIPAL
# ==========================================
def main():
    print("Lecture du fichier CSV...")
    df = pd.read_csv(CSV_FILE, low_memory=False, dtype=str).fillna('')
    
    sql_stations = []
    sql_pdc = []

    print("Traitement des données en cours...")
    for row in df.itertuples(index=False):
        
        # 1. GÉOGRAPHIE
        code_insee = str(row.code_insee_commune).zfill(5)
        geo = get_geo_info(code_insee)
        
        id_region = get_simple_id(geo['nom_region'], regions)
        departements[geo['code_departement']] = (escape_sql(geo['nom_departement']), id_region)
        communes[code_insee] = (escape_sql(row.consolidated_commune if row.consolidated_commune else geo['nom_commune']), 
                                escape_sql(row.consolidated_code_postal if row.consolidated_code_postal else geo['code_postal']), 
                                geo['code_departement'])

        # 2. RÉFÉRENTIELS COMPLEXES
        nom_am = escape_sql(row.nom_amenageur)
        if nom_am not in amenageurs:
            amenageurs[nom_am] = (len(amenageurs) + 1, escape_sql(row.siren_amenageur), escape_sql(row.contact_amenageur))
        id_amenageur = amenageurs[nom_am][0]

        nom_op = escape_sql(row.nom_operateur)
        if nom_op not in operateurs:
            operateurs[nom_op] = (len(operateurs) + 1, escape_sql(row.telephone_operateur), escape_sql(row.contact_operateur))
        id_operateur = operateurs[nom_op][0]

        # 3. RÉFÉRENTIELS SIMPLES
        id_enseigne = get_simple_id(row.nom_enseigne, enseignes)
        id_implantation = get_simple_id(row.implantation_station, implantations)
        id_raccordement = get_simple_id(row.raccordement, raccordements)
        id_restriction = get_simple_id(row.restriction_gabarit, restrictions)
        id_accessibilite = get_simple_id(row.accessibilite_pmr, accessibilites)
        id_condition = get_simple_id(row.condition_acces, conditions)

        # 4. PRÉPARATION DE LA STATION
        id_station = escape_sql(row.id_station_itinerance)
        
        # Gestion sécurisée des coordonnées
        try: lat = float(row.consolidated_latitude)
        except: lat = 0.0
        try: lng = float(row.consolidated_longitude)
        except: lng = 0.0

        sql_stations.append(
            f"('{id_station}', '{escape_sql(row.nom_station)}', '{escape_sql(row.adresse_station)}', "
            f"{lat}, {lng}, '{escape_sql(row.horaires)}', {format_bool(row.ouvert_24_7)}, "
            f"{id_enseigne}, {id_amenageur}, {id_operateur}, '{code_insee}', {id_implantation})"
        )

        # 5. PRÉPARATION DU PDC
        try: puissance = float(row.puissance_nominale)
        except: puissance = 0.0
        
        try: nbre_pdc = int(row.nbre_pdc)
        except: nbre_pdc = 1

        sql_pdc.append(
            f"('{escape_sql(row.id_pdc_itinerance)}', {puissance}, {format_bool(row.gratuit)}, "
            f"'{escape_sql(row.tarification)}', {format_bool(row.reservation)}, {format_bool(row.station_deux_roues)}, "
            f"'{escape_sql(row.num_pdl)}', '{format_date(row.date_mise_en_service)}', '{escape_sql(row.observations)}', "
            f"'{format_datetime(row.date_maj)}', '{format_datetime(row.last_modified)}', '{format_datetime(row.created_at)}', "
            f"{format_bool(row.charge_rapide)}, {nbre_pdc}, '{id_station}', "
            f"{id_raccordement}, {id_restriction}, {id_accessibilite}, {id_condition})"
        )

        print(len(sql_pdc), end="\r")

    # ==========================================
    # ÉCRITURE DU FICHIER SQL FINAL
    # ==========================================
    print("Génération du fichier SQL...")
    with open(OUTPUT_SQL_FILE, 'w', encoding='utf-8') as f:
        f.write("-- ==========================================================\n")
        f.write("-- SCRIPT D'INSERTION GÉNÉRÉ AUTOMATIQUEMENT\n")
        f.write("-- ==========================================================\n\n")
        
        f.write("INSERT IGNORE INTO pays (id_pays, denomination) VALUES (1, 'France');\n\n")
        
        f.write("-- ----------------------------\n-- Géographie\n-- ----------------------------\n")
        for nom, id_reg in regions.items():
            f.write(f"INSERT IGNORE INTO region (id_region, denomination, id_pays) VALUES ({id_reg}, '{nom}', 1);\n")
        for code_dep, data in departements.items():
            f.write(f"INSERT IGNORE INTO departement (id_departement, denomination, id_region) VALUES ('{code_dep}', '{data[0]}', {data[1]});\n")
        for insee, data in communes.items():
            f.write(f"INSERT IGNORE INTO commune (code_insee, nom, code_postal, id_departement) VALUES ('{insee}', '{data[0]}', '{data[1]}', '{data[2]}');\n")
            
        f.write("\n-- ----------------------------\n-- Référentiels\n-- ----------------------------\n")
        for nom, id_ens in enseignes.items():
            f.write(f"INSERT IGNORE INTO enseigne (id_enseigne, nom) VALUES ({id_ens}, '{nom}');\n")
        for nom, data in operateurs.items():
            f.write(f"INSERT IGNORE INTO operateur (id_operateur, nom, telephone, contact) VALUES ({data[0]}, '{nom}', '{data[1]}', '{data[2]}');\n")
        for nom, data in amenageurs.items():
            f.write(f"INSERT IGNORE INTO amenageur (id_amenageur, nom, siren, contact) VALUES ({data[0]}, '{nom}', '{data[1]}', '{data[2]}');\n")
            
        for nom, id_val in implantations.items():
            f.write(f"INSERT IGNORE INTO implantation (id_implantation, denomination) VALUES ({id_val}, '{nom}');\n")
        for nom, id_val in raccordements.items():
            f.write(f"INSERT IGNORE INTO raccordement (id_raccordement, denomination) VALUES ({id_val}, '{nom}');\n")
        for nom, id_val in restrictions.items():
            f.write(f"INSERT IGNORE INTO restriction_gabarit (id_restriction, denomination) VALUES ({id_val}, '{nom}');\n")
        for nom, id_val in accessibilites.items():
            f.write(f"INSERT IGNORE INTO accessibilite_pmr (id_accessibilite, denomination) VALUES ({id_val}, '{nom}');\n")
        for nom, id_val in conditions.items():
            f.write(f"INSERT IGNORE INTO condition_access (id_condition, denomination) VALUES ({id_val}, '{nom}');\n")

        # Insertion par lots pour de meilleures performances SQL
        f.write("\n-- ----------------------------\n-- Stations\n-- ----------------------------\n")
        for i in range(0, len(sql_stations), 1000):
            batch = ",\n".join(sql_stations[i:i+1000])
            f.write(f"INSERT IGNORE INTO station (id_station_itinerance, nom, adresse, latitude, longitude, horaires, ouvert_24_7, id_enseigne, id_amenageur, id_operateur, code_insee, id_implantation) VALUES \n{batch};\n")

        f.write("\n-- ----------------------------\n-- Points de Charge (PDC)\n-- ----------------------------\n")
        for i in range(0, len(sql_pdc), 1000):
            batch = ",\n".join(sql_pdc[i:i+1000])
            f.write(f"INSERT IGNORE INTO pdc (id_pdc_itinerance, puissance_nomiale, gratuit, tarification, reservation, station_deux_roues, num_pdl, date_mise_en_service, observations, date_maj, last_modified, created_at, charge_rapide, nbr_pdc, id_station_itinerance, id_raccordement, id_restriction, id_accessibilite, id_condition) VALUES \n{batch};\n")

    print(f"Terminé ! Le fichier '{OUTPUT_SQL_FILE}' a été généré avec succès.")

if __name__ == "__main__":
    main()