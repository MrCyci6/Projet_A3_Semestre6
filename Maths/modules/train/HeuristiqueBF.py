# cyriac
from pandas import Series

from modules.train.objects.d1.Container import Container


class HeuristiqueBF:
    def __init__(self, longueur_max: float):
        self.__longueur_max: float = longueur_max
        self.__containers: list[Container] = []

    def addObject(self, row: Series) -> None:
        longueur = float(row["longueur"].replace(",", "."))
        added: bool = False

        for container in self.__containers:
            if longueur == self.__longueur_max - container.longueur:
                container.add(row)
                added = True
                break

        if not added:
            for container in self.__containers:
                if container.longueur + longueur <= self.__longueur_max:
                    container.add(row)
                    added = True
                    break

        if not added:
            container = Container()
            if container.longueur + longueur <= self.__longueur_max:
                container.add(row)
                self.__containers.append(container)
            else:
                print("L'objet est trop long il n'a pas pu être ajouté dans un container")

    def print(self) -> None:
        if not self.__containers:
            print("Aucun conteneur n'est actuellement utilisé.")
            return

        longeur_utilisée: float = 0
        for container in self.__containers:
            longeur_utilisée += container.longueur
            print(f"\n{container}")

            if not container.objets:
                print(">>> Vide")
            else:
                for objet in container.objets:
                    details_objet = objet.to_dict()
                    print(f">>> {details_objet}")

        print(f"Nombre container: {len(self.__containers)}, Longueur utilisée: {longeur_utilisée}, Longueur restante: {self.__longueur_max*len(self.__containers) - longeur_utilisée}")