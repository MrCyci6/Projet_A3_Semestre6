-- ============================================================================
-- SCRIPT D'INSERTION COMPLET (insertion.sql)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Dictionnaires
-- ----------------------------------------------------------------------------
INSERT INTO implantation (id_implantation, denomination) VALUES
(1, 'Station dédiée à la recharge rapide'),
(2, 'Parking privé à usage public');

INSERT INTO condition_access (id_condition, denomination) VALUES
(1, 'Accès réservé'),
(2, 'Accès libre');

INSERT INTO raccordement (id_raccordement, denomination) VALUES
(1, 'Direct'),
(2, 'Inconnu/Non précisé');

INSERT INTO accessibilite_pmr (id_accessibilite, denomination) VALUES
(1, 'Accessible mais non réservé PMR'),
(2, 'Accessibilité inconnue');

INSERT INTO restriction_gabarit (id_restriction, denomination) VALUES
(1, 'ras'),
(2, 'Aucune restriction connue'),
(3, 'no restriction');

INSERT INTO type_prise (id_type_prise, denomination) VALUES
(1, 'Prise Type EF'),
(2, 'Prise Type 2'),
(3, 'Prise Type Combo CCS'),
(4, 'Prise Type CHAdeMO'),
(5, 'Prise Type Autre');

INSERT INTO type_paiement (id_type_paiement, denomination) VALUES
(1, 'Paiement à l''acte'),
(2, 'Paiement par CB'),
(3, 'Paiement autre');

INSERT INTO enseigne (id_enseigne, nom) VALUES
(1, 'ZETRA'),
(2, 'SPV COM'),
(3, 'Atlante - Blois - Hôtel initial by Balladins Blois');

INSERT INTO amenageur (id_amenageur, nom, siren, contact) VALUES
(1, 'ZETRA Distribution', '895193019', 'contact@zetra.com'),
(2, 'R3', '902726488', 'kg@lastmilesolutions.com'),
(3, 'Atlante', '911482628', 'digital@atlante.energy');

INSERT INTO operateur (id_operateur, nom, telephone, contact) VALUES
(1, 'ZETRA Distribution SAS', '+33170946050', 'contact@zetra.com'),
(2, 'R3', '+352253636404', 'kg@lastmilesolutions.com'),
(3, 'Atlante France', '+33183750725', 'support.france@atlante.energy');

-- ----------------------------------------------------------------------------
-- 2. Hiérarchie Géographique (Pays -> Région -> Département -> Commune)
-- ----------------------------------------------------------------------------
-- Pays
INSERT INTO pays (id_pays, denomination) VALUES
(1, 'France');

-- Régions
INSERT INTO region (id_region, denomination, id_pays) VALUES
(1, 'Hauts-de-France', 1),
(2, 'Occitanie', 1),
(3, 'Centre-Val de Loire', 1);

-- Départements (Code en VARCHAR pour la compatibilité Corse 2A/2B)
INSERT INTO departement (id_departement, denomination, id_region) VALUES
('59', 'Nord', 1),
('31', 'Haute-Garonne', 2),
('41', 'Loir-et-Cher', 3);

-- Communes liées aux Départements
INSERT INTO commune (code_insee, nom, code_postal, id_departement) VALUES
('59359', 'Loon-Plage', '59279', '59'),
('31585', 'Estancarbon', '31800', '31'),
('41018', 'Blois', '41000', '41');


-- ----------------------------------------------------------------------------
-- 3. Stations
-- ----------------------------------------------------------------------------
INSERT INTO station (
    id_station_itinerance, nom, adresse, latitude, longitude, 
    horaires, ouvert_24_7, id_enseigne, id_amenageur, id_operateur, 
    code_insee, id_implantation
) VALUES
('Non concerné', 'DUNKERQUE FERMEE', '1518 route des Amériques 59279 Loon-Plage', 51.01, 2.19, 'Lu-Di 00:00-23:59', 1, 1, 1, 1, '59359', 1),
('FR3R3P90222922', 'R3 - Estancarbon - Chaussea', '5 Av. du Cagire', 43.12, 0.76, 'Lu-Di 00:00-23:59', 1, 2, 2, 2, '31585', 2),
('FRATLPBLOI0001', 'Atlante - Blois - Hôtel initial by Balladins Blois', 'Rue des 11 Arpents, 7, Blois', 47.61, 1.34, 'Lu-Di 00:00-23:59', 1, 3, 3, 3, '41018', 2);


-- ----------------------------------------------------------------------------
-- 4. Points de Charge (PDC)
-- ----------------------------------------------------------------------------
INSERT INTO pdc (
    id_pdc_itinerance, puissance_nomiale, gratuit, tarification, reservation, 
    station_deux_roues, num_pdl, date_mise_en_service, observations, date_maj, 
    last_modified, created_at, charge_rapide, nbr_pdc, id_station_itinerance,
    id_raccordement, id_restriction, id_accessibilite, id_condition
) VALUES 
-- ZETRA
('Non concerné', 200.00, 0, '', 1, 0, '50018307609364', '2026-05-19', '', '2026-06-16 00:00:00', '2025-06-18 03:41:20', '2025-06-17 15:36:54', 1, 1, 'Non concerné', 1, 1, 1, 1),

-- R3
('FR3R3E10000849971', 7.36, 0, '', 1, 0, '50051595176309', '1970-01-01', '', '2026-01-12 00:00:00', '2026-01-11 13:39:31', '2025-05-05 13:28:02', 0, 6, 'FR3R3P90222922', 1, 2, 2, 2),
('FR3R3E10000849972', 7.36, 0, '', 1, 0, '50051595176309', '1970-01-01', '', '2026-01-12 00:00:00', '2026-01-11 13:39:31', '2025-05-05 13:28:02', 0, 6, 'FR3R3P90222922', 1, 2, 2, 2),
('FR3R3E10001456681', 150.00, 0, '', 1, 0, '50051595176309', '1970-01-01', '', '2026-01-12 00:00:00', '2026-01-11 13:39:31', '2025-05-05 13:28:02', 1, 6, 'FR3R3P90222922', 1, 2, 2, 2),
('FR3R3E10001456682', 150.00, 0, '', 1, 0, '50051595176309', '1970-01-01', '', '2026-01-12 00:00:00', '2026-01-11 13:39:31', '2025-05-05 13:28:02', 1, 6, 'FR3R3P90222922', 1, 2, 2, 2),
('FR3R3E10001456691', 150.00, 0, '', 1, 0, '50051595176309', '1970-01-01', '', '2026-01-12 00:00:00', '2026-01-11 13:39:31', '2025-05-05 13:28:02', 1, 6, 'FR3R3P90222922', 1, 2, 2, 2),
('FR3R3E10001456692', 150.00, 0, '', 1, 0, '50051595176309', '1970-01-01', '', '2026-01-12 00:00:00', '2026-01-11 13:39:31', '2025-05-05 13:28:02', 1, 6, 'FR3R3P90222922', 1, 2, 2, 2),

-- Atlante
('FRATLE000031', 150.00, 0, '', 0, 0, '50034523241156', '1970-01-01', '', '2026-01-12 00:00:00', '2026-01-11 13:39:31', '2025-05-05 13:28:02', 1, 4, 'FRATLPBLOI0001', 2, 3, 1, 2),
('FRATLE000032', 150.00, 0, '', 0, 0, '50034523241156', '1970-01-01', '', '2026-01-12 00:00:00', '2026-01-11 13:39:31', '2025-05-05 13:28:02', 1, 4, 'FRATLPBLOI0001', 2, 3, 1, 2);


-- ----------------------------------------------------------------------------
-- 5. Tables d'association (Prises et Paiements)
-- ----------------------------------------------------------------------------
INSERT INTO Possede (id_pdc_itinerance, id_type_prise, nbr_type_prise) VALUES
('Non concerné', 3, 1),
('FR3R3E10000849971', 2, 1),
('FR3R3E10000849972', 2, 1),
('FR3R3E10001456681', 3, 1),
('FR3R3E10001456682', 3, 1),
('FR3R3E10001456691', 3, 1),
('FR3R3E10001456692', 3, 1),
('FRATLE000031', 3, 1),
('FRATLE000032', 3, 1);

INSERT INTO Avoir (id_pdc_itinerance, id_type_paiement, nbr_type_paiement) VALUES
('Non concerné', 3, 1),
('FRATLE000031', 2, 1),
('FRATLE000032', 2, 1);