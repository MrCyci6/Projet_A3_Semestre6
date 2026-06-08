# cyriac
from modules.train.objects.d2.Colis import Colis
from modules.train.objects.d2.Container import Container


class RectangleMaximaux:
    def __init__(self, container: dict[str, float]):
        self.max_container_longueur = container["longueur"]
        self.max_container_largeur = container["largeur"]

        self.containers: list[Container] = []

    def addObject(self, colis: Colis):
        meilleur: dict[str, tuple[float, float] | Container | float | bool | None] = {
            "score": -float('inf'),
            "container": None,
            "coords": (0, 0),
            "tourne": False
        }

        for container in self.containers:
            peut_rentrer, score, coords, tourne = container.try_add(colis)

            if peut_rentrer and score > meilleur["score"]:
                meilleur["score"] = score
                meilleur["container"] = container
                meilleur["coords"] = coords
                meilleur["tourne"] = tourne

        if meilleur["container"] is not None:
            if meilleur["tourne"]:
                colis.longueur, colis.largeur = colis.largeur, colis.longueur

            meilleur["container"].place_object(colis, meilleur["coords"][0], meilleur["coords"][1])

        else:
            container = Container(self.max_container_longueur, self.max_container_largeur)

            if colis.longueur > self.max_container_longueur or colis.largeur > self.max_container_largeur:
                colis.longueur, colis.largeur = colis.largeur, colis.longueur

            container.place_object(colis, 0.0, 0.0)
            self.containers.append(container)

    def print(self):
        for container in self.containers:
            print("\n", container)
            for colis in container.colis:
                print(colis)

        print(f"Surface restante {round(sum(c.get_surface_libre() for c in self.containers), 5)}")
