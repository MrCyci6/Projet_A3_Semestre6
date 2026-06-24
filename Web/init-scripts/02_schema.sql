-- ----------------------------------------------------------
-- Script MYSQL pour mcd (Corrigé)
-- ----------------------------------------------------------

-- ----------------------------
-- Table: type_prise
-- ----------------------------
CREATE TABLE type_prise (
  id_type_prise INT NOT NULL,
  denomination VARCHAR(128) NOT NULL,
  CONSTRAINT type_prise_PK PRIMARY KEY (id_type_prise)
) ENGINE=InnoDB;

-- ----------------------------
-- Table: condition_access
-- ----------------------------
CREATE TABLE condition_access (
  id_condition INT NOT NULL,
  denomination VARCHAR(128) NOT NULL,
  CONSTRAINT condition_access_PK PRIMARY KEY (id_condition),
  CONSTRAINT denomination_UNQ UNIQUE (denomination)
) ENGINE=InnoDB;

-- ----------------------------
-- Table: raccordement
-- ----------------------------
CREATE TABLE raccordement (
  id_raccordement INT NOT NULL,
  denomination VARCHAR(128) NOT NULL,
  CONSTRAINT raccordement_PK PRIMARY KEY (id_raccordement),
  CONSTRAINT denomination_UNQ UNIQUE (denomination)
) ENGINE=InnoDB;

-- ----------------------------
-- Table: type_paiement
-- ----------------------------
CREATE TABLE type_paiement (
  id_type_paiement INT NOT NULL,
  denomination VARCHAR(128) NOT NULL,
  CONSTRAINT type_paiement_PK PRIMARY KEY (id_type_paiement)
) ENGINE=InnoDB;

-- ----------------------------
-- Table: accessibilite_pmr
-- ----------------------------
CREATE TABLE accessibilite_pmr (
  id_accessibilite INT NOT NULL,
  denomination VARCHAR(128) NOT NULL,
  CONSTRAINT accessibilite_pmr_PK PRIMARY KEY (id_accessibilite),
  CONSTRAINT denomination_UNQ UNIQUE (denomination)
) ENGINE=InnoDB;

-- ----------------------------
-- Table: enseigne
-- ----------------------------
CREATE TABLE enseigne (
  id_enseigne INT NOT NULL,
  nom VARCHAR(128) NOT NULL,
  CONSTRAINT enseigne_PK PRIMARY KEY (id_enseigne),
  CONSTRAINT nom_UNQ UNIQUE (nom)
) ENGINE=InnoDB;

-- ----------------------------
-- Table: implantation
-- ----------------------------
CREATE TABLE implantation (
  id_implantation INT NOT NULL,
  denomination VARCHAR(128) NOT NULL,
  CONSTRAINT implantation_PK PRIMARY KEY (id_implantation),
  CONSTRAINT denomination_UNQ UNIQUE (denomination)
) ENGINE=InnoDB;

-- ----------------------------
-- Table: restriction_gabarit
-- ----------------------------
CREATE TABLE restriction_gabarit (
  id_restriction INT NOT NULL,
  denomination VARCHAR(128) NOT NULL,
  CONSTRAINT restriction_gabarit_PK PRIMARY KEY (id_restriction),
  CONSTRAINT denomination_UNQ UNIQUE (denomination)
) ENGINE=InnoDB;

-- ----------------------------
-- Table: amenageur
-- ----------------------------
CREATE TABLE amenageur (
  id_amenageur INT NOT NULL,
  nom VARCHAR(128) NOT NULL,
  siren VARCHAR(128) NOT NULL,
  contact VARCHAR(128) NOT NULL,
  CONSTRAINT amenageur_PK PRIMARY KEY (id_amenageur),
  CONSTRAINT nom_UNQ UNIQUE (nom)
) ENGINE=InnoDB;

-- ----------------------------
-- Table: operateur
-- ----------------------------
CREATE TABLE operateur (
  id_operateur INT NOT NULL,
  nom VARCHAR(128) NOT NULL,
  telephone VARCHAR(128) NOT NULL,
  contact VARCHAR(128) NOT NULL,
  CONSTRAINT operateur_PK PRIMARY KEY (id_operateur),
  CONSTRAINT nom_UNQ UNIQUE (nom)
) ENGINE=InnoDB;

-- ----------------------------
-- Table: pays
-- ----------------------------
CREATE TABLE pays (
  id_pays INT NOT NULL,
  denomination VARCHAR(128) NOT NULL,
  CONSTRAINT pays_PK PRIMARY KEY (id_pays),
  CONSTRAINT pays_denomination_UNQ UNIQUE (denomination)
) ENGINE=InnoDB;

-- ----------------------------
-- Table: region
-- ----------------------------
CREATE TABLE region (
  id_region INT NOT NULL,
  denomination VARCHAR(128) NOT NULL,
  id_pays INT NOT NULL,
  CONSTRAINT region_PK PRIMARY KEY (id_region),
  CONSTRAINT region_denomination_UNQ UNIQUE (denomination),
  CONSTRAINT region_id_pays_FK FOREIGN KEY (id_pays) REFERENCES pays (id_pays)
) ENGINE=InnoDB;

-- ----------------------------
-- Table: departement
-- ----------------------------
CREATE TABLE departement (
  id_departement VARCHAR(10) NOT NULL,
  denomination VARCHAR(128) NOT NULL,
  id_region INT NOT NULL,
  CONSTRAINT departement_PK PRIMARY KEY (id_departement),
  CONSTRAINT departement_denomination_UNQ UNIQUE (denomination),
  CONSTRAINT departement_id_region_FK FOREIGN KEY (id_region) REFERENCES region (id_region)
) ENGINE=InnoDB;

-- ----------------------------
-- Table: commune
-- ----------------------------
CREATE TABLE commune (
  code_insee VARCHAR(128) NOT NULL,
  nom VARCHAR(128) NOT NULL,
  code_postal VARCHAR(128) NOT NULL,
  id_departement VARCHAR(10) NOT NULL,
  CONSTRAINT commune_PK PRIMARY KEY (code_insee),
  CONSTRAINT commune_id_departement_FK FOREIGN KEY (id_departement) REFERENCES departement (id_departement)
) ENGINE=InnoDB;

-- ----------------------------
-- Table: station
-- ----------------------------
CREATE TABLE station (
  id_station_itinerance VARCHAR(128) NOT NULL,
  nom VARCHAR(128) NOT NULL,
  adresse VARCHAR(128) NOT NULL,
  latitude DECIMAL(10,2) NOT NULL,
  longitude DECIMAL(10,2) NOT NULL,
  horaires VARCHAR(128) NOT NULL,
  ouvert_24_7 TINYINT(1) NOT NULL,
  id_enseigne INT NOT NULL,
  id_amenageur INT NOT NULL,
  id_operateur INT NOT NULL,
  code_insee VARCHAR(128) NOT NULL,
  id_implantation INT,
  CONSTRAINT station_PK PRIMARY KEY (id_station_itinerance),
  CONSTRAINT station_id_enseigne_FK FOREIGN KEY (id_enseigne) REFERENCES enseigne (id_enseigne),
  CONSTRAINT station_id_amenageur_FK FOREIGN KEY (id_amenageur) REFERENCES amenageur (id_amenageur),
  CONSTRAINT station_id_operateur_FK FOREIGN KEY (id_operateur) REFERENCES operateur (id_operateur),
  CONSTRAINT station_code_insee_FK FOREIGN KEY (code_insee) REFERENCES commune (code_insee),
  CONSTRAINT station_id_implantation_FK FOREIGN KEY (id_implantation) REFERENCES implantation (id_implantation)
) ENGINE=InnoDB;

-- ----------------------------
-- Table: pdc
-- ----------------------------
CREATE TABLE pdc (
  id_pdc_itinerance VARCHAR(128) NOT NULL,
  puissance_nomiale DECIMAL(10,2) NOT NULL,
  gratuit TINYINT(1) NOT NULL,
  tarification VARCHAR(128) NOT NULL,
  reservation TINYINT(1) NOT NULL,
  station_deux_roues TINYINT(1) NOT NULL,
  num_pdl VARCHAR(128) NOT NULL,
  date_mise_en_service DATE NOT NULL,
  observations VARCHAR(128) NOT NULL,
  date_maj DATETIME NOT NULL,
  last_modified DATETIME NOT NULL,
  created_at DATETIME NOT NULL,
  charge_rapide TINYINT(1) NOT NULL,
  nbr_pdc INT NOT NULL,
  id_station_itinerance VARCHAR(128) NOT NULL,
  id_raccordement INT,
  id_restriction INT,
  id_accessibilite INT,
  id_condition INT,
  CONSTRAINT pdc_PK PRIMARY KEY (id_pdc_itinerance),
  CONSTRAINT pdc_id_station_itinerance_FK FOREIGN KEY (id_station_itinerance) REFERENCES station (id_station_itinerance),
  CONSTRAINT pdc_id_raccordement_FK FOREIGN KEY (id_raccordement) REFERENCES raccordement (id_raccordement),
  CONSTRAINT pdc_id_restriction_FK FOREIGN KEY (id_restriction) REFERENCES restriction_gabarit (id_restriction),
  CONSTRAINT pdc_id_accessibilite_FK FOREIGN KEY (id_accessibilite) REFERENCES accessibilite_pmr (id_accessibilite),
  CONSTRAINT pdc_id_condition_FK FOREIGN KEY (id_condition) REFERENCES condition_access (id_condition)
) ENGINE=InnoDB;

-- ----------------------------
-- Table: Possede
-- ----------------------------
CREATE TABLE Possede (
  id_pdc_itinerance VARCHAR(128) NOT NULL,
  id_type_prise INT NOT NULL,
  nbr_type_prise INT NOT NULL,
  CONSTRAINT Possede_PK PRIMARY KEY (id_pdc_itinerance, id_type_prise),
  CONSTRAINT Possede_id_pdc_itinerance_FK FOREIGN KEY (id_pdc_itinerance) REFERENCES pdc (id_pdc_itinerance),
  CONSTRAINT Possede_id_type_prise_FK FOREIGN KEY (id_type_prise) REFERENCES type_prise (id_type_prise)
) ENGINE=InnoDB;

-- ----------------------------
-- Table: Avoir
-- ----------------------------
CREATE TABLE Avoir (
  id_pdc_itinerance VARCHAR(128) NOT NULL,
  id_type_paiement INT NOT NULL,
  nbr_type_paiement INT NOT NULL,
  CONSTRAINT Avoir_PK PRIMARY KEY (id_pdc_itinerance, id_type_paiement),
  CONSTRAINT Avoir_id_pdc_itinerance_FK FOREIGN KEY (id_pdc_itinerance) REFERENCES pdc (id_pdc_itinerance),
  CONSTRAINT Avoir_id_type_paiement_FK FOREIGN KEY (id_type_paiement) REFERENCES type_paiement (id_type_paiement)
) ENGINE=InnoDB;