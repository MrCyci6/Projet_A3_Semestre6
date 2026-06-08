# cyriac
from time import time

class Glouton:
    def __init__(self, objets: dict[str, dict[str, float]]):
        self.__objets: dict[str, dict[str, float]] = objets
        self.__objets_sorted: list[tuple[str, dict[str, float]]] = []

        self.__calcRatio()
        self.__sort()

    def getObjets(self) -> dict[str, dict[str, float]]:
        return self.__objets

    def setObjets(self, objets: dict[str, dict[str, float]]) -> None:
        self.__objets = objets

    def getObjetsSorted(self) -> dict[str, dict[str, float]]:
        return self.__objets_sorted

    def __calcRatio(self) -> None:
        for objet in self.__objets:
            self.__objets[objet]["ratio"] = self.__objets[objet]["utilite"] / self.__objets[objet]["poids"]

    def __sort(self) -> None:
        self.__objets_sorted = sorted(self.__objets.items(), key=lambda item: item[1]["ratio"], reverse=True)

    def run(self, C: float) -> tuple[list[dict[str, dict[str, float]]], tuple[float, float, float]]:
        sac: list[dict[str, dict[str, float]]] = []
        total_poids: float = 0
        total_utilite: float = 0
        startTime = time()

        for i in range(0, len(self.__objets_sorted)):
            objet: tuple(str, dict[str, float]) = self.__objets_sorted[i]
            poids: float = objet[1]["poids"]
            utilite: float = objet[1]["utilite"]

            if total_poids + poids <= C:
                sac.append(objet)
                total_poids += poids
                total_utilite += utilite
            if total_poids == C:
                break

        endTime = time()
        total_time = endTime - startTime
        stats: tuple(float, float, float) = (total_poids, total_utilite, total_time)

        return sac, stats