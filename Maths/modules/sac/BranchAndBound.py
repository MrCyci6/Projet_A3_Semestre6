# cyriac/IA
from modules.sac.bab.Node import Node
from time import time

class BranchAndBound:
    def __init__(self, objets: dict[str, dict[str, float]], C: float):
        self.__C = C
        self.__objets = objets
        self.__objets_sorted: list[tuple[str, dict[str, float]]] = []

        self.__calcRatio()
        self.__sort()

    def getC(self) -> float:
        return self.__C

    def setC(self, C: float) -> None:
        self.__C = C

    def getObjets(self) -> dict[str, dict[str, float]]:
        return self.__objets

    def setObjets(self, objets: dict[str, dict[str, float]]) -> None:
        self.__objets = objets

    def getObjetsSorted(self) -> list[tuple[str, dict[str, float]]]:
        return self.__objets_sorted

    def __calcRatio(self) -> None:
        for objet in self.__objets:
            self.__objets[objet]["ratio"] = self.__objets[objet]["utilite"] / self.__objets[objet]["poids"]

    def __sort(self) -> None:
        self.__objets_sorted = sorted(self.__objets.items(), key=lambda item: item[1]["ratio"], reverse=True)

    def borne(self, node: Node):
        if round(node.getPoidsTotal(), 5) > self.__C:
            return 0

        profit_estime = node.getUtiliteTotal()
        poids_actuel = node.getPoidsTotal()
        niveau_suivant = node.getNiveau() + 1

        while (niveau_suivant < len(self.__objets_sorted)) and (round(poids_actuel + self.__objets_sorted[niveau_suivant][1]["poids"], 5) <= self.__C):
            poids_actuel += self.__objets_sorted[niveau_suivant][1]["poids"]
            profit_estime += self.__objets_sorted[niveau_suivant][1]["utilite"]
            niveau_suivant += 1

        if niveau_suivant < len(self.__objets_sorted):
            espace_restant = self.__C - poids_actuel
            ratio = self.__objets_sorted[niveau_suivant][1]["ratio"]
            profit_estime = profit_estime + (espace_restant * ratio)

        return profit_estime

    def run(self):
        meilleur_utilite = 0
        meilleur_poids = 0
        meilleur_sac = []
        file = []

        startTime = time()

        node_racine = Node(-1, 0, 0)
        node_racine.setBorne(self.borne(node_racine))
        file.append(node_racine)

        while len(file) > 0:
            index_meilleur_node = max(range(len(file)), key=lambda i: file[i].getBorne())
            node = file.pop(index_meilleur_node)

            if node.getBorne() <= meilleur_utilite:
                break;

            if node.getNiveau() == len(self.__objets_sorted) - 1:
                continue

            prochain_niveau = node.getNiveau() + 1
            objet_suivant_tuple = self.__objets_sorted[prochain_niveau]
            objet_suivant_dict = objet_suivant_tuple[1]

            nouveau_sac_avec = node.getSac().copy()
            nouveau_sac_avec.append(objet_suivant_tuple)

            node_avec = Node(
                prochain_niveau,
                node.getUtiliteTotal() + objet_suivant_dict["utilite"],
                node.getPoidsTotal() + objet_suivant_dict["poids"],
                sac=nouveau_sac_avec
            )

            if round(node_avec.getPoidsTotal(), 5) <= self.__C and node_avec.getUtiliteTotal() > meilleur_utilite:
                meilleur_utilite = node_avec.getUtiliteTotal()
                meilleur_poids = node_avec.getPoidsTotal()
                meilleur_sac = node_avec.getSac()

            node_avec.setBorne(self.borne(node_avec))

            if node_avec.getBorne() > meilleur_utilite:
                file.append(node_avec)

            node_sans = Node(
                prochain_niveau,
                node.getUtiliteTotal(),
                node.getPoidsTotal(),
                sac=node.getSac().copy()
            )

            if round(node_sans.getPoidsTotal(), 5) <= self.__C and node_sans.getUtiliteTotal() > meilleur_utilite:
                meilleur_utilite = node_sans.getUtiliteTotal()
                meilleur_poids = node_sans.getPoidsTotal()
                meilleur_sac = node_sans.getSac()

            node_sans.setBorne(self.borne(node_sans))

            if node_sans.getBorne() > meilleur_utilite:
                file.append(node_sans)

        endTime = time()
        total_time = endTime - startTime

        stats = (meilleur_poids, meilleur_utilite, total_time)

        return meilleur_sac, stats