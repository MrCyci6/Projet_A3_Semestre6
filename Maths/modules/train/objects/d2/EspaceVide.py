# cyriac
class EspaceVide:
    def __init__(self, x: float, y: float, longueur: float, largeur: float):
        self.x: float = x
        self.y: float = y
        self.longueur: float = longueur
        self.largeur: float = largeur

    @property
    def surface(self) -> float:
        return self.longueur * self.largeur