# cyriac/IA
from modules.train.objects.d3.Colis import Colis
from modules.train.objects.d3.v2.EspaceVide import EspaceVide

class Container:
    id = 0

    def __init__(self, max_longuer: float = 0, max_largeur: float = 0, max_hauteur: float = 0):
        self.id = Container.id
        Container.id += 1

        self.max_longueur: float = max_longuer
        self.max_largeur: float = max_largeur
        self.max_hauteur: float = max_hauteur

        self.colis: list[Colis] = []
        self.espaces_vides: list[EspaceVide] = [EspaceVide(0, 0, 0, self.max_longueur, self.max_largeur, self.max_hauteur)]

    def __eclatement(self, colis: Colis, espaceVide: EspaceVide) -> list[EspaceVide]:
        x_vide_min = espaceVide.x
        x_vide_max = espaceVide.x + espaceVide.longueur
        y_vide_min = espaceVide.y
        y_vide_max = espaceVide.y + espaceVide.largeur
        z_vide_min = espaceVide.z
        z_vide_max = espaceVide.z + espaceVide.hauteur

        x_colis_min = colis.x
        x_colis_max = colis.x + colis.longueur
        y_colis_min = colis.y
        y_colis_max = colis.y + colis.largeur
        z_colis_min = colis.z
        z_colis_max = colis.z + colis.hauteur

        if (x_colis_min >= x_vide_max or x_colis_max <= x_vide_min or
                y_colis_min >= y_vide_max or y_colis_max <= y_vide_min or
                z_colis_min >= z_vide_max or z_colis_max <= z_vide_min):
            return [espaceVide]

        nouveaux_vides = []

        if x_vide_min < x_colis_min:
            nouveaux_vides.append(EspaceVide(
                x_vide_min, y_vide_min, z_vide_min,
                x_colis_min - x_vide_min, espaceVide.largeur, espaceVide.hauteur
            ))

        if y_vide_min < y_colis_min:
            nouveaux_vides.append(EspaceVide(
                x_vide_min, y_vide_min, z_vide_min,
                espaceVide.longueur, y_colis_min - y_vide_min, espaceVide.hauteur
            ))

        if x_colis_max < x_vide_max:
            nouveaux_vides.append(EspaceVide(
                x_colis_max, y_vide_min, z_vide_min,
                x_vide_max - x_colis_max, espaceVide.largeur, espaceVide.hauteur
            ))

        if y_colis_max < y_vide_max:
            nouveaux_vides.append(EspaceVide(
                x_vide_min, y_colis_max, z_vide_min,
                espaceVide.longueur, y_vide_max - y_colis_max, espaceVide.hauteur
            ))

        if z_vide_min < z_colis_min:
            nouveaux_vides.append(EspaceVide(
                x_vide_min, y_vide_min, z_vide_min,
                espaceVide.longueur, espaceVide.largeur, z_colis_min - z_vide_min
            ))
        if z_colis_max < z_vide_max:
            nouveaux_vides.append(EspaceVide(
                x_vide_min, y_vide_min, z_colis_max,
                espaceVide.longueur, espaceVide.largeur, z_vide_max - z_colis_max
            ))

        return nouveaux_vides

    def __nettoyage(self) -> None:
        vides_valides = []
        for i, vide1 in enumerate(self.espaces_vides):
            est_inclus = False
            for j, vide2 in enumerate(self.espaces_vides):
                if i != j:
                    if (vide1.x >= vide2.x and vide1.y >= vide2.y and vide1.z >= vide2.z and
                            vide1.x + vide1.longueur <= vide2.x + vide2.longueur and
                            vide1.y + vide1.largeur <= vide2.y + vide2.largeur and
                            vide1.z + vide1.hauteur <= vide2.z + vide2.hauteur):
                        est_inclus = True
                        break
            if not est_inclus:
                vides_valides.append(vide1)

        self.espaces_vides = vides_valides

    def get_volume_libre(self) -> float:
        volume_total = self.max_longueur * self.max_largeur * self.max_hauteur
        volume_occupe = sum(colis.longueur * colis.largeur * colis.hauteur for colis in self.colis)
        return round(volume_total - volume_occupe, 5)

    def try_add(self, colis: Colis):
        if colis.palette == 1:
            permutations = [
                (colis.longueur, colis.largeur, colis.hauteur),
                (colis.largeur, colis.longueur, colis.hauteur)
            ]
        else:
            permutations = [
                (colis.longueur, colis.largeur, colis.hauteur),
                (colis.longueur, colis.hauteur, colis.largeur),
                (colis.largeur, colis.longueur, colis.hauteur),
                (colis.largeur, colis.hauteur, colis.longueur),
                (colis.hauteur, colis.longueur, colis.largeur),
                (colis.hauteur, colis.largeur, colis.longueur)
            ]

        meilleur: dict = {
            "x": -1,
            "y": -1,
            "z": -1,
            "score": -float("inf"),
            "dims": None
        }
        peut_rentrer = False

        for espace in self.espaces_vides:
            for perm in permutations:
                L_test, l_test, H_test = perm

                if espace.longueur >= L_test and espace.largeur >= l_test and espace.hauteur >= H_test:
                    peut_rentrer = True

                    score = -espace.volume - (espace.z * 100) - (espace.y * 0.1) - (espace.x * 0.01)

                    if score > meilleur["score"]:
                        meilleur["score"] = float(score)
                        meilleur["x"] = espace.x
                        meilleur["y"] = espace.y
                        meilleur["z"] = espace.z
                        meilleur["dims"] = perm

        if peut_rentrer:
            return True, meilleur["score"], (meilleur["x"], meilleur["y"], meilleur["z"]), meilleur["dims"]

        return False, 0, (0, 0, 0), None

    def place_object(self, colis: Colis, x: float, y: float, z: float) -> None:
        colis.x = x
        colis.y = y
        colis.z = z
        self.colis.append(colis)

        vides_apres_impact = []
        for espace in self.espaces_vides:
            morceaux = self.__eclatement(colis, espace)
            vides_apres_impact.extend(morceaux)

        self.espaces_vides = vides_apres_impact
        self.__nettoyage()

    def __repr__(self):
        return (f"Container n°{self.id} "
                f"- (L_max:{self.max_longueur}, l_max:{self.max_largeur}) "
                f"- Objets: {len(self.colis)} | Espaces vides: {len(self.espaces_vides)}")