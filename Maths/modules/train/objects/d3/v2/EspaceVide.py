# cyriac
class EspaceVide:
    def __init__(self, x: float, y: float, z: float, longueur: float, largeur: float, hauteur: float):
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.longueur: float = longueur
        self.largeur: float = largeur
        self.hauteur: float = hauteur

    @property
    def surface(self) -> float:
        return self.longueur * self.largeur

    @property
    def volume(self) -> float:
        return self.longueur * self.largeur * self.hauteur