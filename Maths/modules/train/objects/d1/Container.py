# cyriac
from pandas import Series

class Container:
    id = 0

    def __init__(self):
        self.id = Container.id
        Container.id += 1

        self.longueur: float = 0
        self.objets: list[Series] = []

    def add(self, row: Series):
        self.objets.append(row)
        self.longueur += float(row["longueur"].replace(",", "."))

    def __repr__(self):
        return (f"Container n°{self.id} (L:{self.longueur}) - Objets: {len(self.objets)}")