-- ============================================================================
-- SCRIPT D'INSERTION COMPLET (insertion.sql) CORRIGÉ
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Table : type_prise
-- ----------------------------------------------------------------------------
INSERT INTO type_prise (id_type_prise, denomination) VALUES
(1, 'Prise Type EF'),
(2, 'Prise Type 2'),
(3, 'Prise Type Combo CCS'),
(4, 'Prise Type CHAdeMO'),
(5, 'Prise Type Autre');

-- ----------------------------------------------------------------------------
-- 2. Table : type_paiement
-- ----------------------------------------------------------------------------
INSERT INTO type_paiement (id_type_paiement, denomination) VALUES
(1, 'Paiement à l''acte'),
(2, 'Paiement par CB'),
(3, 'Paiement autre');

-- ----------------------------------------------------------------------------
-- 3. Table : enseigne
-- ----------------------------------------------------------------------------
INSERT INTO enseigne (id_enseigne, nom) VALUES
(1, 'ZETRA'),
(2, 'SPV COM'),
(3, 'Atlante - Blois - Hôtel initial by Balladins Blois');

-- ----------------------------------------------------------------------------
-- 4. Table : commune
-- ----------------------------------------------------------------------------
INSERT INTO commune (code_insee, nom, code_postal) VALUES
('59359', 'Loon-Plage', '59279'),
('31585', 'Estancarbon', '31800'),
('41018', 'Blois', '41000');

-- ----------------------------------------------------------------------------
-- 5. Table : amenageur
-- ----------------------------------------------------------------------------
INSERT INTO amenageur (id_amenageur, nom, siren, contact) VALUES
(1, 'ZETRA Distribution', '895193019', 'contact@zetra.com'),
(2, 'R3', '902726488', 'kg@lastmilesolutions.com'),
(3, 'Atlante', '911482628', 'digital@atlante.energy');

-- ----------------------------------------------------------------------------
-- 6. Table : operateur
-- ----------------------------------------------------------------------------
INSERT INTO operateur (id_operateur, nom, telephone, contact) VALUES
(1, 'ZETRA Distribution SAS', '+33170946050', 'contact@zetra.com'),
(2, 'R3', '+352253636404', 'kg@lastmilesolutions.com'),
(3, 'Atlante France', '+33183750725', 'support.france@atlante.energy');

-- ----------------------------------------------------------------------------
-- 7. Table : station
-- ----------------------------------------------------------------------------
INSERT INTO station (
    id_station_itinerance, nom, implantation, adresse, 
    latitude, longitude, horaires, ouvert_24_7, 
    id_enseigne, id_amenageur, id_operateur, code_insee
) VALUES
('Non concerné', 'DUNKERQUE FERMEE', 'Station dédiée à la recharge rapide', '1518 route des Amériques 59279 Loon-Plage', 51.01, 2.19, 'Lu-Di 00:00-23:59', 1, 1, 1, 1, '59359'),
('FR3R3P90222922', 'R3 - Estancarbon - Chaussea', 'Parking privé à usage public', '5 Av. du Cagire', 43.12, 0.76, 'Lu-Di 00:00-23:59', 1, 2, 2, 2, '31585'),
('FRATLPBLOI0001', 'Atlante - Blois - Hôtel initial by Balladins Blois', 'Parking privé à usage public', 'Rue des 11 Arpents, 7, Blois', 47.61, 1.34, 'Lu-Di 00:00-23:59', 1, 3, 3, 3, '41018');

-- ----------------------------------------------------------------------------
-- 8. Table : pdc (Points De Charge)
-- ----------------------------------------------------------------------------
INSERT INTO pdc (
    id_pdc_itinerance, puissance_nomiale, gratuit, tarification, condition_access, 
    reservation, accessibilite_pmr, restriction_gabarit, station_deux_roues, 
    raccordement, num_pdl, date_mise_en_service, observations, date_maj, 
    last_modified, created_at, charge_rapide, nbr_pdc, id_station_itinerance
) VALUES 
-- Ligne 1 (ZETRA)
('Non concerné', 200.00, 0, '', 'Accès réservé', 1, 'Accessible mais non réservé PMR', 'ras', 0, 'Direct', '50018307609364', '2026-05-19', '', '2026-06-16 00:00:00', '2025-06-18 03:41:20', '2025-06-17 15:36:54', 1, 1, 'Non concerné'),

-- Lignes 2 à 7 (R3)
('FR3R3E10000849971', 7.36, 0, '', 'Accès libre', 1, 'Accessibilité inconnue', 'Aucune restriction connue', 0, 'Direct', '50051595176309', '1970-01-01', '', '2026-01-12 00:00:00', '2026-01-11 13:39:31', '2025-05-05 13:28:02', 0, 6, 'FR3R3P90222922'),
('FR3R3E10000849972', 7.36, 0, '', 'Accès libre', 1, 'Accessibilité inconnue', 'Aucune restriction connue', 0, 'Direct', '50051595176309', '1970-01-01', '', '2026-01-12 00:00:00', '2026-01-11 13:39:31', '2025-05-05 13:28:02', 0, 6, 'FR3R3P90222922'),
('FR3R3E10001456681', 150.00, 0, '', 'Accès libre', 1, 'Accessibilité inconnue', 'Aucune restriction connue', 0, 'Direct', '50051595176309', '1970-01-01', '', '2026-01-12 00:00:00', '2026-01-11 13:39:31', '2025-05-05 13:28:02', 1, 6, 'FR3R3P90222922'),
('FR3R3E10001456682', 150.00, 0, '', 'Accès libre', 1, 'Accessibilité inconnue', 'Aucune restriction connue', 0, 'Direct', '50051595176309', '1970-01-01', '', '2026-01-12 00:00:00', '2026-01-11 13:39:31', '2025-05-05 13:28:02', 1, 6, 'FR3R3P90222922'),
('FR3R3E10001456691', 150.00, 0, '', 'Accès libre', 1, 'Accessibilité inconnue', 'Aucune restriction connue', 0, 'Direct', '50051595176309', '1970-01-01', '', '2026-01-12 00:00:00', '2026-01-11 13:39:31', '2025-05-05 13:28:02', 1, 6, 'FR3R3P90222922'),
('FR3R3E10001456692', 150.00, 0, '', 'Accès libre', 1, 'Accessibilité inconnue', 'Aucune restriction connue', 0, 'Direct', '50051595176309', '1970-01-01', '', '2026-01-12 00:00:00', '2026-01-11 13:39:31', '2025-05-05 13:28:02', 1, 6, 'FR3R3P90222922'),

-- Lignes 8 et 9 (Atlante)
('FRATLE000031', 150.00, 0, '', 'Accès libre', 0, 'Accessible mais non réservé PMR', 'no restriction', 0, '', '50034523241156', '1970-01-01', '', '2026-01-12 00:00:00', '2026-01-11 13:39:31', '2025-05-05 13:28:02', 1, 4, 'FRATLPBLOI0001'),
('FRATLE000032', 150.00, 0, '', 'Accès libre', 0, 'Accessible mais non réservé PMR', 'no restriction', 0, '', '50034523241156', '1970-01-01', '', '2026-01-12 00:00:00', '2026-01-11 13:39:31', '2025-05-05 13:28:02', 1, 4, 'FRATLPBLOI0001');

-- ----------------------------------------------------------------------------
-- 9. Table d'association : type_prise_pdc
-- ----------------------------------------------------------------------------
-- nbr_type_prise est extrait de la colonne nb_types_prise ou défini par défaut à 1
INSERT INTO type_prise_pdc (id_pdc_itinerance, id_type_prise, nbr_type_prise) VALUES
('Non concerné', 3, 1),       -- Combo CCS pour ZETRA
('FR3R3E10000849971', 2, 1), -- Type 2 pour R3
('FR3R3E10000849972', 2, 1), -- Type 2 pour R3
('FR3R3E10001456681', 3, 1), -- Combo CCS pour R3
('FR3R3E10001456682', 3, 1), -- Combo CCS pour R3
('FR3R3E10001456691', 3, 1), -- Combo CCS pour R3
('FR3R3E10001456692', 3, 1), -- Combo CCS pour R3
('FRATLE000031', 3, 1),      -- Combo CCS pour Atlante
('FRATLE000032', 3, 1);      -- Combo CCS pour Atlante

-- ----------------------------------------------------------------------------
-- 10. Table d'association : type_paiement_pdc
-- ----------------------------------------------------------------------------
INSERT INTO type_paiement_pdc (id_pdc_itinerance, id_type_paiement, nbr_type_paiement) VALUES
('Non concerné', 3, 1),  -- Paiement autre pour ZETRA
('FRATLE000031', 2, 1), -- Paiement par CB pour Atlante
('FRATLE000032', 2, 1); -- Paiement par CB pour Atlante