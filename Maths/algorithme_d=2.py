# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 11:26:15 2026

@author: gaspa
"""
#Gasparotto Romain/Copilot

donnees = {
    "Tubes acier_1": (10, 1),
    "Tubes acier_2": (9, 2),
    "Tubes acier_3": (7.5, 1.2),
    "Acide chlorhydrique_1": (1, 1),
    "Godet pelleteuse_1": (2, 2),
    "Rails_1": (11, 1),
    "Tubes PVC_1": (3, 2),
    "Echaffaudage_1": (3, 1.3),
    "Verre_1": (3, 2.1),
    "Ciment_1": (4, 1),
    "Bois vrac_1": (5, 0.8),
    "Troncs chênes_1": (6, 1.9),
    "Troncs hêtres_1": (7, 1.6),
    "Pompe à chaleur_1": (5, 1.1),
    "Cuivre_1": (6, 2),
    "Zinc_1": (5, 0.8),
    "Papier_1": (4, 1.6),
    "Carton_1": (7, 1),
    "Verre blanc vrac_1": (9, 0.9),
    "Verre brun vrac_1": (3, 1.6),
    "Briques rouges_1": (5, 1.1),
    "Pièces métalliques_1": (6, 1.6),
    "Pièces métalliques_2": (7, 0.9),
    "Pièces métalliques_3": (3, 1.6),
    "Ardoises_1": (1, 1.8),
    "Tuiles_1": (2, 1.2),
    "Vitraux_1": (4, 0.7),
    "Carrelage_1": (6, 1.2),
    "Tôles_1": (7, 0.6),
    "Tôles_2": (9, 1.7),
    "Tôles_3": (6, 1.9),
    "Tôles_4": (3, 2.2),
    "Tôles_5": (3, 0.5),
    "Mobilier urbain_1": (4, 0.7),
    "Lin_1": (5, 2.2),
    "Textiles à recycler_1": (6, 1.3),
    "Aluminium_1": (6, 1.3),
    "Batteries automobile_1": (7, 1.4),
    "Quincaillerie_1": (6, 1.1),
    "Treuil_1": (7, 0.9),
    "Treuil_2": (8, 0.5),
    "Acier_1": (8, 0.9),
    "Laine de bois_1": (8, 0.9),
    "Ouate de cellusose_1": (5, 1.7),
    "Chanvre isolation_1": (2.2, 1.6),
    "Moteur électrique_1": (4.2, 1.5),
    "Semi conducteurs_1": (3.7, 0.9),
    "Semi conducteurs_2": (5.6, 0.5),
    "Semi conducteurs_3": (4.9, 0.9),
    "Semi conducteurs_4": (8.7, 1.3),
    "Semi conducteurs_5": (6.1, 2.2),
    "Semi conducteurs_6": (3.3, 1.8),
    "Semi conducteurs_7": (2.6, 1.6),
    "Semi conducteurs_8": (2.9, 1.6),
    "Aluminium_2": (2, 1.1),
    "Aluminium_3": (3, 0.6),
    "Aluminium_4": (6, 1),
    "Aluminium_5": (5, 1.3),
    "Aluminium_6": (4, 2.1),
    "Aluminium_7": (6, 1.5),
    "Aluminium_8": (4, 0.8),
    "Aluminium_9": (2, 2),
    "Aluminium_10": (4, 1),
    "Aluminium_11": (6, 1.8),
    "Lithium_1": (6, 1.9),
    "Lithium_2": (3, 2),
    "Lithium_3": (4, 1.5),
    "Lithium_4": (4, 2.1),
    "Lithium_5": (2, 1.2),
    "Lithium_6": (6, 1.3),
    "Lithium_7": (2, 0.8),
    "Contreplaqué_1": (4, 1.4),
    "Contreplaqué_2": (5, 0.6),
    "Contreplaqué_3": (5, 0.6),
    "Contreplaqué_4": (4, 0.7),
    "Contreplaqué_5": (6, 0.5),
    "Contreplaqué_6": (3, 1.5),
    "Contreplaqué_7": (3, 1.4),
    "Contreplaqué_8": (3, 2),
    "Contreplaqué_9": (5, 1.5),
    "Contreplaqué_10": (5, 2.2),
    "Contreplaqué_11": (6, 1.2),
    "Poutre_1": (5, 0.8),
    "Poutre_2": (3, 0.5),
    "Poutre_3": (5, 1.4),
    "Poutre_4": (6, 0.7),
    "Poutre_5": (6, 1.2),
    "Poutre_6": (3, 1.7),
    "Poutre_7": (5, 1.6),
    "Pneus_1": (3, 1.3),
    "Pneus_2": (4, 1.5),
    "Pneus_3": (3, 1.5),
    "Pneus_4": (3, 0.6),
    "Pneus_5": (5, 1.8),
    "Pneus_6": (3, 1.8),
    "Pneus_7": (4, 1.7),
    "Pneus_8": (4, 1.5),
    "Pneus_9": (2, 2.1),
    "Pneus_10": (2, 0.7),
    "Pneus_11": (6, 1.2)
}

import time

def trier_par_surface_decroissante(donnees):
    return dict(
        sorted(
            donnees.items(),
            key=lambda item: item[1][0] * item[1][1],
            reverse=True
        )
    )

def convertir_pour_maximal_rectangles(donnees_triees):
    objets = []
    for nom, (a, b) in donnees_triees.items():
        objets.append((nom, (a, b)))
    return objets

class Rect:
    def __init__(self, x, y, w, h):
        self.x = x  # position x
        self.y = y  # position y
        self.w = w  # largeur
        self.h = h  # hauteur

    def fits(self, w, h):
        return w <= self.w and h <= self.h

def split_free_rect(free_rect, placed_rect):
    new_rects = []

    # Rectangle à droite
    if placed_rect.x + placed_rect.w < free_rect.x + free_rect.w:
        new_rects.append(Rect(
            placed_rect.x + placed_rect.w,
            free_rect.y,
            free_rect.x + free_rect.w - (placed_rect.x + placed_rect.w),
            free_rect.h
        ))

    # Rectangle en dessous
    if placed_rect.y + placed_rect.h < free_rect.y + free_rect.h:
        new_rects.append(Rect(
            free_rect.x,
            placed_rect.y + placed_rect.h,
            free_rect.w,
            free_rect.y + free_rect.h - (placed_rect.y + placed_rect.h)
        ))

    return new_rects

def remove_redundant_rects(free_rects):
    cleaned = []
    for r in free_rects:
        contained = False
        for other in free_rects:
            if r is not other:
                if (r.x >= other.x and r.y >= other.y and
                    r.x + r.w <= other.x + other.w and
                    r.y + r.h <= other.y + other.h):
                    contained = True
                    break
        if not contained:
            cleaned.append(r)
    return cleaned

def best_area_fit(rect, w, h):
    return rect.w * rect.h - w * h

def maximal_rectangles_un_wagon(objets, W, H):
    free_rects = [Rect(0, 0, W, H)]
    placements = []

    for name, (w, h) in objets:
        best_rect = None
        best_score = float("inf")

        # Chercher le meilleur rectangle libre
        for fr in free_rects:
            if fr.fits(w, h):
                score = best_area_fit(fr, w, h)
                if score < best_score:
                    best_score = score
                    best_rect = fr

        if best_rect is None:
            continue  # objet non placé dans ce wagon

        # Placement en haut-gauche du rectangle libre choisi
        placed = Rect(best_rect.x, best_rect.y, w, h)
        placements.append((name, placed.x, placed.y, w, h))

        # Découpage du rectangle libre
        new_rects = split_free_rect(best_rect, placed)
        free_rects.remove(best_rect)
        free_rects.extend(new_rects)

        # Nettoyage
        free_rects = remove_redundant_rects(free_rects)

    return placements

def pack_multi_wagons(objets, W, H):
    wagons = []
    objets_restants = objets.copy()

    while objets_restants:
        placements = maximal_rectangles_un_wagon(objets_restants, W, H)

        if not placements:
            break  # plus rien ne rentre (ou objets trop grands)

        # Ajouter ce wagon
        wagons.append(placements)

        # Retirer les objets placés de la liste restante
        noms_places = {p[0] for p in placements}
        objets_restants = [
            (nom, dims) for (nom, dims) in objets_restants
            if nom not in noms_places
        ]

    return wagons

def surface_restante_2d(W, H, placements):
    """
    W, H : dimensions du wagon (longueur, largeur)
    placements : liste des objets placés (name, x, y, w, h)
    """
    surface_totale = W * H
    surface_occupee = sum(w * h for (_, _, _, w, h) in placements)
    return surface_totale - surface_occupee

import time

def mesurer_temps_execution(fonction, *args, **kwargs):
    """
    Mesure le temps d'exécution d'une fonction.
    fonction : la fonction à exécuter
    *args, **kwargs : paramètres de la fonction
    """
    debut = time.time()
    resultat = fonction(*args, **kwargs)
    fin = time.time()
    temps = fin - debut
    return resultat, temps



# 1) Tri par surface
donnees_triees = trier_par_surface_decroissante(donnees)

# 2) Conversion en liste d’objets
objets = convertir_pour_maximal_rectangles(donnees_triees)

# 3) Paramètres du wagon (à adapter à ton cas)
WAGON_LONGUEUR = 11.583
WAGON_LARGEUR = 2.294

# 4) Packing multi-wagons
wagons = pack_multi_wagons(objets, WAGON_LONGUEUR, WAGON_LARGEUR)

# 5) Affichage simple
for i, wagon in enumerate(wagons, start=1):
    print(f"\nWagon {i}:")
    for name, x, y, w, h in wagon:
        print(f"  - {name} à ({x}, {y}) taille ({w} × {h})")

restant = surface_restante_2d(WAGON_LONGUEUR, WAGON_LARGEUR, wagons[0])
print("Surface restante :", restant)

wagons, temps = mesurer_temps_execution(
    pack_multi_wagons, 
    objets, 
    WAGON_LONGUEUR, 
    WAGON_LARGEUR
)

print("Temps d'exécution :", temps, "secondes")
