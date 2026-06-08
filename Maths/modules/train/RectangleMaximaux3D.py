# cyriac
from modules.train.objects.d3.Colis import Colis
from modules.train.objects.d3.v2.Container import Container


class RectangleMaximaux3D:
    def __init__(self, container: dict[str, float]):
        self.max_container_longueur = container["longueur"]
        self.max_container_largeur = container["largeur"]
        self.max_container_hauteur = container["hauteur"]

        self.containers: list[Container] = []

    def addObject(self, colis: Colis):
        meilleur: dict[str, tuple[float, float, float] | Container | float | bool | None] = {
            "score": -float('inf'),
            "container": None,
            "coords": (0, 0, 0),
            "dims": None
        }

        for container in self.containers:
            peut_rentrer, score, coords, dims = container.try_add(colis)

            if peut_rentrer and score > meilleur["score"]:
                meilleur["score"] = score
                meilleur["container"] = container
                meilleur["coords"] = coords
                meilleur["dims"] = dims

        if meilleur["container"] is not None:
            colis.longueur, colis.largeur, colis.hauteur = meilleur["dims"]
            meilleur["container"].place_object(colis, meilleur["coords"][0], meilleur["coords"][1], meilleur["coords"][2])

        else:
            container = Container(
                self.max_container_longueur,
                self.max_container_largeur,
                self.max_container_hauteur
            )

            if colis.longueur > self.max_container_longueur or colis.largeur > self.max_container_largeur:
                colis.longueur, colis.largeur = colis.largeur, colis.longueur

            container.place_object(colis, 0, 0, 0)
            self.containers.append(container)

    def print(self):
        for container in self.containers:
            print("\n", container)
            for colis in container.colis:
                print(colis)

        print(f"Volume libre: {round(sum(c.get_volume_libre() for c in self.containers), 5)}")
