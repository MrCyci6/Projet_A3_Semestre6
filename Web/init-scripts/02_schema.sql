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
-- Table: enseigne
-- ----------------------------
CREATE TABLE enseigne (
  id_enseigne INT NOT NULL,
  nom VARCHAR(128) NOT NULL,
  CONSTRAINT enseigne_PK PRIMARY KEY (id_enseigne),
  CONSTRAINT nom_UNQ UNIQUE (nom)
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
-- Table: commune
-- ----------------------------
CREATE TABLE commune (
  code_insee VARCHAR(128) NOT NULL,
  nom VARCHAR(128) NOT NULL,
  code_postal VARCHAR(128) NOT NULL,
  CONSTRAINT commune_PK PRIMARY KEY (code_insee)
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
-- Table: station
-- ----------------------------
CREATE TABLE station (
  id_station_itinerance VARCHAR(128) NOT NULL,
  nom VARCHAR(128) NOT NULL,
  implantation VARCHAR(128) NOT NULL,
  adresse VARCHAR(128) NOT NULL,
  latitude DECIMAL(10,2) NOT NULL,
  longitude DECIMAL(10,2) NOT NULL,
  horaires VARCHAR(128) NOT NULL,
  ouvert_24_7 TINYINT(1) NOT NULL, -- Corrigé : passé de DATE à TINYINT(1) pour les booléens
  id_enseigne INT NOT NULL,
  id_amenageur INT NOT NULL,
  id_operateur INT NOT NULL,
  code_insee VARCHAR(128) NOT NULL,
  CONSTRAINT station_PK PRIMARY KEY (id_station_itinerance),
  CONSTRAINT station_id_enseigne_FK FOREIGN KEY (id_enseigne) REFERENCES enseigne (id_enseigne),
  CONSTRAINT station_id_amenageur_FK FOREIGN KEY (id_amenageur) REFERENCES amenageur (id_amenageur),
  CONSTRAINT station_id_operateur_FK FOREIGN KEY (id_operateur) REFERENCES operateur (id_operateur),
  CONSTRAINT station_code_insee_FK FOREIGN KEY (code_insee) REFERENCES commune (code_insee)
) ENGINE=InnoDB;

-- ----------------------------
-- Table: pdc
-- ----------------------------
CREATE TABLE pdc (
  id_pdc_itinerance VARCHAR(128) NOT NULL,
  puissance_nomiale DECIMAL(10,2) NOT NULL,
  gratuit TINYINT(1) NOT NULL,
  tarification VARCHAR(128) NOT NULL,
  condition_access VARCHAR(128) NOT NULL,
  reservation TINYINT(1) NOT NULL,
  accessibilite_pmr VARCHAR(128) NOT NULL,
  restriction_gabarit VARCHAR(128) NOT NULL,
  station_deux_roues TINYINT(1) NOT NULL,
  raccordement VARCHAR(128) NOT NULL,
  num_pdl VARCHAR(128) NOT NULL,
  date_mise_en_service DATE NOT NULL,
  observations VARCHAR(128) NOT NULL,
  date_maj DATETIME NOT NULL,
  last_modified DATETIME NOT NULL,
  created_at DATETIME NOT NULL,
  charge_rapide TINYINT(1) NOT NULL,
  nbr_pdc INT NOT NULL,
  id_station_itinerance VARCHAR(128) NOT NULL,
  CONSTRAINT pdc_PK PRIMARY KEY (id_pdc_itinerance),
  CONSTRAINT pdc_id_station_itinerance_FK FOREIGN KEY (id_station_itinerance) REFERENCES station (id_station_itinerance)
) ENGINE=InnoDB;

-- ----------------------------
-- Table: type_prise_pdc
-- ----------------------------
CREATE TABLE type_prise_pdc (
  id_pdc_itinerance VARCHAR(128) NOT NULL,
  id_type_prise INT NOT NULL,
  nbr_type_prise INT NOT NULL,
  CONSTRAINT type_prise_pdc_PK PRIMARY KEY (id_pdc_itinerance, id_type_prise),
  CONSTRAINT type_prise_pdc_id_pdc_itinerance_FK FOREIGN KEY (id_pdc_itinerance) REFERENCES pdc (id_pdc_itinerance),
  CONSTRAINT type_prise_pdc_id_type_prise_FK FOREIGN KEY (id_type_prise) REFERENCES type_prise (id_type_prise)
) ENGINE=InnoDB;

-- ----------------------------
-- Table: type_paiement_pdc
-- ----------------------------
CREATE TABLE type_paiement_pdc (
  id_pdc_itinerance VARCHAR(128) NOT NULL,
  id_type_paiement INT NOT NULL,
  nbr_type_paiement INT NOT NULL,
  CONSTRAINT type_paiement_pdc_PK PRIMARY KEY (id_pdc_itinerance, id_type_paiement),
  CONSTRAINT type_paiement_pdc_id_pdc_itinerance_FK FOREIGN KEY (id_pdc_itinerance) REFERENCES pdc (id_pdc_itinerance),
  CONSTRAINT type_paiement_pdc_id_type_paiement_FK FOREIGN KEY (id_type_paiement) REFERENCES type_paiement (id_type_paiement)
) ENGINE=InnoDB;