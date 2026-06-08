# cyriac
from modules.sac.Glouton import Glouton
from modules.sac.BranchAndBound import BranchAndBound

import pandas as pd
from time import time

from modules.train.HeuristiqueBF import HeuristiqueBF
from modules.train.PointsExtremes import PointsExtremes
from modules.train.RectangleMaximaux import RectangleMaximaux
from modules.train.RectangleMaximaux3D import RectangleMaximaux3D
from modules.train.objects.d3.Colis import Colis

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

if __name__ == "__main__":

    """glouton = Glouton(objets)
    sac, stats = glouton.run(5)
    print(sac, stats)

    branchAndBound = BranchAndBound(objets, 0.6)
    stats = branchAndBound.run()
    print(sac, stats)"""

    container = {
        "longueur": 11.583,
        "largeur": 2.294,
        "hauteur": 2.569
    }

    data = pd.read_csv("./data/marchandises.csv", sep=";")

    """# d1
    bf = HeuristiqueBF(container["longueur"])
    startTime = time()

    for i, row in data.iterrows():
        bf.addObject(row)

    endTime = time()

    bf.print()
    print(endTime-startTime)"""


    """# d2
    startTime = time()

    data = [Colis(d) for d in data.iterrows()]
    rectangleMaximaux = RectangleMaximaux(container)

    for row in data:
        rectangleMaximaux.addObject(row)

    endTime = time()

    rectangleMaximaux.print()
    print(endTime-startTime)"""

    # d3
    startTime = time()

    data = [Colis(d) for d in data.iterrows()]
    rectangleMaximaux3D = RectangleMaximaux3D(container)

    for row in data:
        rectangleMaximaux3D.addObject(row)

    endTime = time()

    rectangleMaximaux3D.print()
    print(endTime - startTime)