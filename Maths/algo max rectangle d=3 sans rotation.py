# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 08:32:20 2026

@author: gaspa
"""
#Gasparotto Romain/Copilot

donnees = {
    "Tubes acier_1": (10, 1, 0.5),
    "Tubes acier_2": (9, 2, 0.7),
    "Tubes acier_3": (7.5, 1.2, 0.4),
    "Acide chlorhydrique_1": (1, 1, 1),
    "Godet pelleteuse_1": (2, 2, 1),
    "Rails_1": (11, 1, 0.2),
    "Tubes PVC_1": (3, 2, 0.6),
    "Echaffaudage_1": (3, 1.3, 1.8),
    "Verre_1": (3, 2.1, 0.6),
    "Ciment_1": (4, 1, 0.5),
    "Bois vrac_1": (5, 0.8, 1),
    "Troncs chênes_1": (6, 1.9, 1),
    "Troncs hêtres_1": (7, 1.6, 1.5),
    "Pompe à chaleur_1": (5, 1.1, 2.3),
    "Cuivre_1": (6, 2, 1.4),
    "Zinc_1": (5, 0.8, 0.8),
    "Papier_1": (4, 1.6, 0.6),
    "Carton_1": (7, 1, 1.3),
    "Verre blanc vrac_1": (9, 0.9, 2.2),
    "Verre brun vrac_1": (3, 1.6, 0.9),
    "Briques rouges_1": (5, 1.1, 2.4),
    "Pièces métalliques_1": (6, 1.6, 1.4),
    "Pièces métalliques_2": (7, 0.9, 1.2),
    "Pièces métalliques_3": (3, 1.6, 1.9),
    "Ardoises_1": (1, 1.8, 1),
    "Tuiles_1": (2, 1.2, 2.3),
    "Vitraux_1": (4, 0.7, 1.2),
    "Carrelage_1": (6, 1.2, 2.5),
    "Tôles_1": (7, 0.6, 1.5),
    "Tôles_2": (9, 1.7, 1),
    "Tôles_3": (6, 1.9, 1.6),
    "Tôles_4": (3, 2.2, 2.2),
    "Tôles_5": (3, 0.5, 2.2),
    "Mobilier urbain_1": (4, 0.7, 1.9),
    "Lin_1": (5, 2.2, 0.7),
    "Textiles à recycler_1": (6, 1.3, 2.5),
    "Aluminium_1": (6, 1.3, 1.2),
    "Batteries automobile_1": (7, 1.4, 2.5),
    "Quincaillerie_1": (6, 1.1, 1),
    "Treuil_1": (7, 0.9, 1.3),
    "Treuil_2": (8, 0.5, 0.5),
    "Acier_1": (8, 0.9, 1.7),
    "Laine de bois_1": (8, 0.9, 1.8),
    "Ouate de cellusose_1": (5, 1.7, 1.2),
    "Chanvre isolation_1": (2.2, 1.6, 1.1),
    "Moteur électrique_1": (4.2, 1.5, 0.8),
    "Semi conducteurs_1": (3.7, 0.9, 1.4),
    "Semi conducteurs_2": (5.6, 0.5, 1.4),
    "Semi conducteurs_3": (4.9, 0.9, 2.5),
    "Semi conducteurs_4": (8.7, 1.3, 1.3),
    "Semi conducteurs_5": (6.1, 2.2, 2.3),
    "Semi conducteurs_6": (3.3, 1.8, 2.3),
    "Semi conducteurs_7": (2.6, 1.6, 2.3),
    "Semi conducteurs_8": (2.9, 1.6, 2),
    "Aluminium_2": (2, 1.1, 0.6),
    "Aluminium_3": (3, 0.6, 1.2),
    "Aluminium_4": (6, 1, 0.8),
    "Aluminium_5": (5, 1.3, 0.6),
    "Aluminium_6": (4, 2.1, 2.1),
    "Aluminium_7": (6, 1.5, 1.9),
    "Aluminium_8": (4, 0.8, 2.1),
    "Aluminium_9": (2, 2, 2.3),
    "Aluminium_10": (4, 1, 1.1),
    "Aluminium_11": (6, 1.8, 1.1),
    "Lithium_1": (6, 1.9, 0.9),
    "Lithium_2": (3, 2, 2.2),
    "Lithium_3": (4, 1.5, 0.9),
    "Lithium_4": (4, 2.1, 2.5),
    "Lithium_5": (2, 1.2, 1.5),
    "Lithium_6": (6, 1.3, 2),
    "Lithium_7": (2, 0.8, 1.1),
    "Contreplaqué_1": (4, 1.4, 2),
    "Contreplaqué_2": (5, 0.6, 0.5),
    "Contreplaqué_3": (5, 0.6, 1.8),
    "Contreplaqué_4": (4, 0.7, 1.4),
    "Contreplaqué_5": (6, 0.5, 0.7),
    "Contreplaqué_6": (3, 1.5, 1.8),
    "Contreplaqué_7": (3, 1.4, 2),
    "Contreplaqué_8": (3, 2, 2.3),
    "Contreplaqué_9": (5, 1.5, 0.7),
    "Contreplaqué_10": (5, 2.2, 0.5),
    "Contreplaqué_11": (6, 1.2, 1.2),
    "Poutre_1": (5, 0.8, 0.7),
    "Poutre_2": (3, 0.5, 1.9),
    "Poutre_3": (5, 1.4, 0.7),
    "Poutre_4": (6, 0.7, 0.7),
    "Poutre_5": (6, 1.2, 2),
    "Poutre_6": (3, 1.7, 1.1),
    "Poutre_7": (5, 1.6, 2.1),
    "Pneus_1": (3, 1.3, 1.7),
    "Pneus_2": (4, 1.5, 1.7),
    "Pneus_3": (3, 1.5, 1.9),
    "Pneus_4": (3, 0.6, 1.9),
    "Pneus_5": (5, 1.8, 0.5),
    "Pneus_6": (3, 1.8, 0.7),
    "Pneus_7": (4, 1.7, 1.4),
    "Pneus_8": (4, 1.5, 0.5),
    "Pneus_9": (2, 2.1, 1.8),
    "Pneus_10": (2, 0.7, 1.1),
    "Pneus_11": (6, 1.2, 1.3)
}

class Box:
    def __init__(self, x, y, z, L, W, H):
        self.x = x
        self.y = y
        self.z = z
        self.L = L  # longueur
        self.W = W  # largeur
        self.H = H  # hauteur

    def fits(self, L, W, H):
        return L <= self.L and W <= self.W and H <= self.H

def split_free_box(free_box, placed_box):
    new_boxes = []

    # Boîte à droite
    if placed_box.x + placed_box.L < free_box.x + free_box.L:
        new_boxes.append(Box(
            placed_box.x + placed_box.L,
            free_box.y,
            free_box.z,
            free_box.x + free_box.L - (placed_box.x + placed_box.L),
            free_box.W,
            free_box.H
        ))

    # Boîte devant
    if placed_box.y + placed_box.W < free_box.y + free_box.W:
        new_boxes.append(Box(
            free_box.x,
            placed_box.y + placed_box.W,
            free_box.z,
            free_box.L,
            free_box.y + free_box.W - (placed_box.y + placed_box.W),
            free_box.H
        ))

    # Boîte au-dessus
    if placed_box.z + placed_box.H < free_box.z + free_box.H:
        new_boxes.append(Box(
            free_box.x,
            free_box.y,
            placed_box.z + placed_box.H,
            free_box.L,
            free_box.W,
            free_box.z + free_box.H - (placed_box.z + placed_box.H)
        ))

    return new_boxes

def remove_redundant_boxes(free_boxes):
    cleaned = []
    for b in free_boxes:
        contained = False
        for other in free_boxes:
            if b is not other:
                if (b.x >= other.x and b.y >= other.y and b.z >= other.z and
                    b.x + b.L <= other.x + other.L and
                    b.y + b.W <= other.y + other.W and
                    b.z + b.H <= other.z + other.H):
                    contained = True
                    break
        if not contained:
            cleaned.append(b)
    return cleaned

def best_volume_fit(box, L, W, H):
    return box.L * box.W * box.H - L * W * H

def maximal_boxes_un_wagon(objets, Lmax, Wmax, Hmax):
    free_boxes = [Box(0, 0, 0, Lmax, Wmax, Hmax)]
    placements = []

    for name, (L, W, H) in objets:
        best_box = None
        best_score = float("inf")

        # Chercher la meilleure boîte libre
        for fb in free_boxes:
            if fb.fits(L, W, H):
                score = best_volume_fit(fb, L, W, H)
                if score < best_score:
                    best_score = score
                    best_box = fb

        if best_box is None:
            continue  # objet non placé dans ce wagon

        # Placement
        placed = Box(best_box.x, best_box.y, best_box.z, L, W, H)
        placements.append((name, placed.x, placed.y, placed.z, L, W, H))

        # Découpage
        new_boxes = split_free_box(best_box, placed)
        free_boxes.remove(best_box)
        free_boxes.extend(new_boxes)

        # Nettoyage
        free_boxes = remove_redundant_boxes(free_boxes)

    return placements

def pack_multi_wagons(objets, Lmax, Wmax, Hmax):
    wagons = []
    objets_restants = objets.copy()

    while objets_restants:
        placements = maximal_boxes_un_wagon(objets_restants, Lmax, Wmax, Hmax)

        if not placements:
            break

        wagons.append(placements)

        noms_places = {p[0] for p in placements}
        objets_restants = [
            (nom, dims) for (nom, dims) in objets_restants
            if nom not in noms_places
        ]

    return wagons

def trier_par_volume(donnees):
    return dict(
        sorted(
            donnees.items(),
            key=lambda item: item[1][0] * item[1][1] * item[1][2],
            reverse=True
        )
    )

def convertir_3d(donnees_triees):
    return [(nom, dims) for nom, dims in donnees_triees.items()]

def afficher_wagons_simplifie(wagons):
    for i, wagon in enumerate(wagons, start=1):
        print(f"\n===== WAGON {i} =====")
        print("Contenu :")
        for item in wagon:
            nom = item[0]  
            print(f"  - {nom}")

def volume_restante_3d(Lmax, Wmax, Hmax, placements):
    """
    Lmax, Wmax, Hmax : dimensions du wagon
    placements : liste des objets placés (name, x, y, z, L, W, H)
    """
    volume_total = Lmax * Wmax * Hmax
    volume_occupe = sum(L * W * H for (_, _, _, _, L, W, H) in placements)
    return volume_total - volume_occupe

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



donnees_triees = trier_par_volume(donnees)
objets = convertir_3d(donnees_triees)

Lmax = 11.583
Wmax = 2.294
Hmax = 2.569  

wagons = pack_multi_wagons(objets, Lmax, Wmax, Hmax)
afficher_wagons_simplifie(wagons)

restant = volume_restante_3d(Lmax, Wmax, Hmax, wagons[0])
print("Volume restant :", restant)

wagons, temps = mesurer_temps_execution(
    pack_multi_wagons,
    objets,
    Lmax,
    Wmax,
    Hmax
)

print("Temps d'exécution :", temps, "secondes")
