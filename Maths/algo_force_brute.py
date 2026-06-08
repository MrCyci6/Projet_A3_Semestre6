# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 15:18:44 2026

@author: gaspa
"""
#Gasparotto Romain/Copilot

objets: dict[str, dict[str, float]] = {
        "Arrache Manivelle": {
            "poids": 0.4,
            "utilite": 0,
            "ratio": 0
        },
        "Batterie Portable": {
            "poids": 0.5,
            "utilite": 0.4,
            "ratio": 0
        },
        "Pantalon de pluie": {
            "poids": 0.4,
            "utilite": 0.75,
            "ratio": 0
        },
        "Gourde": {
            "poids": 1,
            "utilite": 2,
            "ratio": 0
        },
        "Pince multiprise": {
            "poids": 0.4,
            "utilite": 0.8,
            "ratio": 0
        },
        "Carte IGN": {
            "poids": 0.1,
            "utilite": 0.2,
            "ratio": 0
        },
        "Barre de céréales": {
            "poids": 0.4,
            "utilite": 0.8,
            "ratio": 0
        },
        "Fruits": {
            "poids": 0.6,
            "utilite": 1.3,
            "ratio": 0
        },
        "Chambre à air": {
            "poids": 0.2,
            "utilite": 0.5,
            "ratio": 0
        },
        "Veste de pluie": {
            "poids": 0.4,
            "utilite": 1,
            "ratio": 0
        },
        "Désinfectant": {
            "poids": 0.2,
            "utilite": 0.6,
            "ratio": 0
        },
        "Clé de 15": {
            "poids": 0.3,
            "utilite": 1,
            "ratio": 0
        },
        "Compresses": {
            "poids": 0.1,
            "utilite": 0.4,
            "ratio": 0
        },
        "Crème solaire": {
            "poids": 0.4,
            "utilite": 1.75,
            "ratio": 0
        },
        "Téléphone mobile": {
            "poids": 0.4,
            "utilite": 2,
            "ratio": 0
        },
        "Lampes": {
            "poids": 0.3,
            "utilite": 1.8,
            "ratio": 0
        },
        "Pompe": {
            "poids": 0.2,
            "utilite": 1.5,
            "ratio": 0
        },
        "Couteau suisse": {
            "poids": 0.2,
            "utilite": 1.5,
            "ratio": 0
        },
        "Multi-tool": {
            "poids": 0.2,
            "utilite": 1.7,
            "ratio": 0
        },
        "Bouchon valve chromé bleu": {
            "poids": 0.01,
            "utilite": 0.1,
            "ratio": 0
        },
        "Démonte-pneus": {
            "poids": 0.1,
            "utilite": 1.5,
            "ratio": 0
        },
        "Maillon rapide": {
            "poids": 0.05,
            "utilite": 1.4,
            "ratio": 0
        },
        "Rustines": {
            "poids": 0.05,
            "utilite": 1.5
        }
        }

import itertools
import time

def force_brute_sac_a_dos_exact(liste_objets: dict, poids_max_float: float):
    meilleure_utilite = -1
    meilleure_combinaison = []
    meilleur_poids = 0
    
    # 1. On convertit le poids max en entier (ex: 3.0 kg -> 300)
    poids_max_int = int(round(poids_max_float * 100))
    
    # 2. On convertit les floats du dictionnaire en entiers (multiplié par 100)
    # Format : (nom, poids_original, utilite_original, poids_entier, utilite_entier)
    items = []
    for nom, info in liste_objets.items():
        p_int = int(round(info["poids"] * 100))
        u_int = int(round(info["utilite"] * 100))
        items.append((nom, info["poids"], info["utilite"], p_int, u_int))
        
    n = len(items)
    temps_debut=time.time()
    # 3. Boucle de force brute
    for r in range(n + 1):
        for comb in itertools.combinations(items, r):
            # Calcul en utilisant les valeurs entières (strictement exact)
            poids_total_int = sum(item[3] for item in comb)
            
            if poids_total_int > poids_max_int:
                continue
                
            utilite_total_int = sum(item[4] for item in comb)
            
            if utilite_total_int > meilleure_utilite:
                meilleure_utilite = utilite_total_int
                meilleure_combinaison = comb
                
    # 4. On recalcule les totaux exacts à partir des valeurs d'origine pour l'affichage
    poids_final_reel = sum(item[1] for item in meilleure_combinaison)
    utilite_finale_reelle = sum(item[2] for item in meilleure_combinaison)
    temps_fin=time.time()
    temps_execution=temps_fin - temps_debut
    print(temps_execution)
    return meilleure_combinaison, poids_final_reel, utilite_finale_reelle
    
# --- Exécution ---
POIDS_MAXIMUM = 5  # Capacité max du sac en kg


choix, poids_total, utilite_totale = force_brute_sac_a_dos_exact(objets, POIDS_MAXIMUM)

print("\n--- MEILLEURE COMBINAISON TROUVÉE ---")

    
print(f"\nNombre d'objets embarqués : {len(choix)}")
print(f"Poids total final : {round(poids_total, 2)} kg / {POIDS_MAXIMUM} kg")
print(f"Utilité totale finale : {round(utilite_totale, 2)}")
