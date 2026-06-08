# cyriac
from pandas import Series

class Colis:
    def __init__(self, row: Series, x: float = 0, y: float = 0):
        self.data: Series = row

        self.x: float = x
        self.y: float = y

        self.numero: int = int(row[1]["numero"])
        self.designation: str = row[1]["designation"]

        self.longueur: float = float(row[1]["longueur"].replace(",", "."))
        self.largeur: float = float(row[1]["largeur"].replace(",", "."))

    @property
    def surface(self) -> float:
        return self.longueur * self.largeur

    def __repr__(self):
        return f"N°{self.numero} - \"{self.designation}\" - ({self.x}, {self.y}) - [L:{self.longueur}, l:{self.largeur}]"