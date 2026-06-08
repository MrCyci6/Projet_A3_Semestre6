# cyriac/IA
from modules.train.objects.d3.Colis import Colis
from modules.train.objects.d3.Container import Container
from modules.train.objects.d3.Point import Point


class PointsExtremes:
    def __init__(self, container: dict[str, float]):
        self.max_container_longueur = container["longueur"]
        self.max_container_largeur = container["largeur"]
        self.max_container_hauteur = container["hauteur"]

        self.containers: list[Container] = []

    def addObject(self, colis: Colis):
        meilleur: dict[str, tuple[float, float] | Container | Point | float | bool | None] = {
            "score": -float('inf'),
            "container": None,
            "point": None,
            "tourne": False
        }

        for container in self.containers:
            peut_rentrer, score, point, tourne = container.try_add(colis)

            if peut_rentrer and score > meilleur["score"]:
                meilleur["score"] = score
                meilleur["container"] = container
                meilleur["point"] = point
                meilleur["tourne"] = tourne

        if meilleur["container"] is not None:
            if meilleur["tourne"]:
                colis.tourner()

            meilleur["container"].place_object(colis, meilleur["point"])

        else:
            container = Container(self.max_container_longueur, self.max_container_largeur, self.max_container_hauteur)

            if colis.longueur > self.max_container_longueur or colis.largeur > self.max_container_largeur:
                colis.tourner()

            container.place_object(colis, Point(0, 0, 0))
            self.containers.append(container)

    def print(self):
        for container in self.containers:
            print("\n", container)
            for colis in container.colis:
                print(colis)
