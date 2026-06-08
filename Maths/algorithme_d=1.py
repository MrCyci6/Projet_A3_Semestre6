# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 11:26:15 2026

@author: gaspa
"""
#Gasparotto Romain/Copilot

import time 

donnees = {
    "Tubes acier_1": 10,
    "Tubes acier_2": 9,
    "Tubes acier_3": 7.5,
    "Acide chlorhydrique_1": 1,
    "Godet pelleteuse_1": 2,
    "Rails_1": 11,
    "Tubes PVC_1": 3,
    "Echaffaudage_1": 3,
    "Verre_1": 3,
    "Ciment_1": 4,
    "Bois vrac_1": 5,
    "Troncs chênes_1": 6,
    "Troncs hêtres_1": 7,
    "Pompe à chaleur_1": 5,
    "Cuivre_1": 6,
    "Zinc_1": 5,
    "Papier_1": 4,
    "Carton_1": 7,
    "Verre blanc vrac_1": 9,
    "Verre brun vrac_1": 3,
    "Briques rouges_1": 5,
    "Pièces métalliques_1": 6,
    "Pièces métalliques_2": 7,
    "Pièces métalliques_3": 3,
    "Ardoises_1": 1,
    "Tuiles_1": 2,
    "Vitraux_1": 4,
    "Carrelage_1": 6,
    "Tôles_1": 7,
    "Tôles_2": 9,
    "Tôles_3": 6,
    "Tôles_4": 3,
    "Tôles_5": 3,
    "Mobilier urbain_1": 4,
    "Lin_1": 5,
    "Textiles à recycler_1": 6,
    "Aluminium_1": 6,
    "Aluminium_2": 2,
    "Aluminium_3": 3,
    "Aluminium_4": 6,
    "Aluminium_5": 5,
    "Aluminium_6": 4,
    "Aluminium_7": 6,
    "Aluminium_8": 4,
    "Aluminium_9": 2,
    "Aluminium_10": 4,
    "Aluminium_11": 6,
    "Batteries automobile_1": 7,
    "Quincaillerie_1": 6,
    "Treuil_1": 7,
    "Treuil_2": 8,
    "Acier_1": 8,
    "Laine de bois_1": 8,
    "Ouate de cellusose_1": 5,
    "Chanvre isolation_1": 2.2,
    "Moteur électrique_1": 4.2,
    "Semi conducteurs_1": 3.7,
    "Semi conducteurs_2": 5.6,
    "Semi conducteurs_3": 4.9,
    "Semi conducteurs_4": 8.7,
    "Semi conducteurs_5": 6.1,
    "Semi conducteurs_6": 3.3,
    "Semi conducteurs_7": 2.6,
    "Semi conducteurs_8": 2.9,
    "Lithium_1": 6,
    "Lithium_2": 3,
    "Lithium_3": 4,
    "Lithium_4": 4,
    "Lithium_5": 2,
    "Lithium_6": 6,
    "Lithium_7": 2,
    "Contreplaqué_1": 4,
    "Contreplaqué_2": 5,
    "Contreplaqué_3": 5,
    "Contreplaqué_4": 4,
    "Contreplaqué_5": 6,
    "Contreplaqué_6": 3,
    "Contreplaqué_7": 3,
    "Contreplaqué_8": 3,
    "Contreplaqué_9": 5,
    "Contreplaqué_10": 5,
    "Contreplaqué_11": 6,
    "Poutre_1": 5,
    "Poutre_2": 3,
    "Poutre_3": 5,
    "Poutre_4": 6,
    "Poutre_5": 6,
    "Poutre_6": 3,
    "Poutre_7": 5,
    "Pneus_1": 3,
    "Pneus_2": 4,
    "Pneus_3": 3,
    "Pneus_4": 3,
    "Pneus_5": 5,
    "Pneus_6": 3,
    "Pneus_7": 4,
    "Pneus_8": 4,
    "Pneus_9": 2,
    "Pneus_10": 2,
    "Pneus_11": 6
}

def trier_dictionnaire_decroissant(dico):
    items = list(dico.items())
    for i in range(len(items)):
        max_index = i
        for j in range(i + 1, len(items)):
            if items[j][1] > items[max_index][1]:
                max_index = j
        items[i], items[max_index] = items[max_index], items[i]
    return dict(items)

donnees_triees = trier_dictionnaire_decroissant(donnees)
print(donnees_triees)

def remplir_wagons(donnees_triees, capacite_wagon):
    temps_debut = time.time()
    wagons = []

    for objet, poids in donnees_triees.items():
        place = False

        for wagon in wagons:
            if wagon["reste"] >= poids:
                wagon["contenu"].append((objet, poids))
                wagon["reste"] -= poids
                place = True
                break

        if not place:
            wagons.append({
                "contenu": [(objet, poids)],
                "reste": capacite_wagon - poids
            })

    temps_fin = time.time()
    temps_execution = temps_fin - temps_debut
    return wagons, temps_execution

def afficher_wagons(wagons):
    for i, wagon in enumerate(wagons, start=1):
        print(f"\nWagon {i} :")
        print("  Contenu :")
        for objet, poids in wagon["contenu"]:
            print(f"    - {objet} : {poids}")
        print(f"  Capacité restante : {wagon['reste']}")

def total_restes(wagons):
    total = 0
    for wagon in wagons:
        total += wagon["reste"]
    return total

# 🔹 Appel correct de la fonction
wagons, temps_execution = remplir_wagons(donnees_triees, capacite_wagon=11.583)

afficher_wagons(wagons)
print("\nTotal des restes :", total_restes(wagons))
print("Temps d'exécution :", temps_execution, "secondes")
