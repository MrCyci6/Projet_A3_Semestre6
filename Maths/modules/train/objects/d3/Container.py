# cyriac/IA
from modules.train.objects.d3.Colis import Colis
from modules.train.objects.d3.Point import Point

class Container:
    id = 0

    def __init__(self, max_longuer: float = 0, max_largeur: float = 0, max_hauteur: float = 0):
        self.id = Container.id
        Container.id += 1

        self.max_longueur: float = max_longuer
        self.max_largeur: float = max_largeur
        self.max_hauteur: float = max_hauteur

        self.colis: list[Colis] = []
        self.points: list[Point] = [Point(0,0,0)]

    def __collision(self, x: float, y: float, z: float, L: float, l: float, H: float) -> bool:
        if x + L > self.max_longueur or y + l > self.max_largeur or z + H > self.max_hauteur:
            return True

        for c in self.colis:
            if not (x + L <= c.x or x >= c.x + c.longueur or y + l <= c.y or y >= c.y + c.largeur or z + H <= c.z or z >= c.z + c.hauteur):
                return True

        return False

    def __score(self, x: float, y: float, z: float, L: float, l: float, H: float) -> float:
        score = 0

        if z == 0:
            score += (L * l)
        if x == 0:
            score += (l * H)
        if y == 0:
            score += (L * H)
        if x + L == self.max_longueur:
            score += (l * H)
        if y + l == self.max_largeur:
            score += (L * H)
        if z + H == self.max_hauteur:
            score += (L * l)

        for c in self.colis:
            if x + L == c.x or x == c.x + c.longueur:
                chevauchement_y = max(0, min(y + l, c.y + c.largeur) - max(y, c.y))
                chevauchement_z = max(0, min(z + H, c.z + c.hauteur) - max(z, c.z))
                score += chevauchement_y * chevauchement_z

            if y + l == c.y or y == c.y + c.largeur:
                chevauchement_x = max(0, min(x + L, c.x + c.longueur) - max(x, c.x))
                chevauchement_z = max(0, min(z + H, c.z + c.hauteur) - max(z, c.z))
                score += chevauchement_x * chevauchement_z

            if z + H == c.z or z == c.z + c.hauteur:
                chevauchement_x = max(0, min(x + L, c.x + c.longueur) - max(x, c.x))
                chevauchement_y = max(0, min(y + l, c.y + c.largeur) - max(y, c.y))
                score += chevauchement_x * chevauchement_y

        return score

    def __nettoyage(self):
        points_valides = []

        for pt in self.points:
            est_valide = True
            for c in self.colis:
                if (c.x <= pt.x < c.x + c.longueur and c.y <= pt.y < c.y + c.largeur and c.z <= pt.z < c.z + c.hauteur):
                    est_valide = False
                    break

            if pt.x == self.max_longueur or pt.y == self.max_largeur or pt.z == self.max_hauteur:
                est_valide = False

            if est_valide:
                points_valides.append(pt)

        self.points = points_valides

    def try_add(self, colis: Colis) -> tuple[bool, float, Colis | None, bool]:
        meilleur: dict[str, float | bool | Point | None] = {
            "score": -float('inf'),
            "point": None,
            "tourne": False
        }
        peut_rentrer = False

        for pt in self.points:
            if not self.__collision(pt.x, pt.y, pt.z, colis.longueur, colis.largeur, colis.hauteur):
                score_normal = self.__score(pt.x, pt.y, pt.z, colis.longueur, colis.largeur, colis.hauteur)
                #score_normal -= (pt.x + pt.y + pt.z) * 0.0001

                if score_normal > meilleur["score"]:
                    meilleur["score"] = score_normal
                    meilleur["point"] = pt
                    meilleur["tourne"] = False
                    peut_rentrer = True

            if not self.__collision(pt.x, pt.y, pt.z, colis.largeur, colis.longueur, colis.hauteur):
                score_tourne = self.__score(pt.x, pt.y, pt.z, colis.largeur, colis.longueur, colis.hauteur)
                #score_tourne -= (pt.x + pt.y + pt.z) * 0.0001

                if score_tourne > meilleur["score"]:
                    meilleur["score"] = score_tourne
                    meilleur["point"] = pt
                    meilleur["tourne"] = True
                    peut_rentrer = True

        return peut_rentrer, meilleur["score"], meilleur["point"], meilleur["tourne"]

    def place_object(self, colis: Colis, point: Point):
        colis.x = point.x
        colis.y = point.y
        colis.z = point.z
        self.colis.append(colis)

        self.points.remove(point)

        nouveau_haut = Point(colis.x, colis.y, colis.z + colis.hauteur)
        nouveau_droite = Point(colis.x + colis.longueur, colis.y, colis.z)
        nouveau_avant = Point(colis.x, colis.y + colis.largeur, colis.z)

        self.points.extend([nouveau_haut, nouveau_droite, nouveau_avant])

        self.__nettoyage()

    def __repr__(self):
        return (f"Container n°{self.id} "
                f"- (L_max:{self.max_longueur}, l_max:{self.max_largeur}) "
                f"- Objets: {len(self.colis)}")