# cyriac/IA
from modules.train.objects.d2.Colis import Colis
from modules.train.objects.d2.EspaceVide import EspaceVide

class Container:
    id = 0

    def __init__(self, max_longuer: float = 0, max_largeur: float = 0):
        self.id = Container.id
        Container.id += 1

        self.max_longueur: float = max_longuer
        self.max_largeur: float = max_largeur

        self.colis: list[Colis] = []
        self.espaces_vides: list[EspaceVide] = [EspaceVide(0.0, 0.0, self.max_longueur, self.max_largeur)]

    def __eclatement(self, colis: Colis, espaceVide: EspaceVide) -> list[EspaceVide]:
        x_vide_min = espaceVide.x
        x_vide_max = espaceVide.x + espaceVide.longueur
        y_vide_min = espaceVide.y
        y_vide_max = espaceVide.y + espaceVide.largeur

        x_colis_min = colis.x
        x_colis_max = colis.x + colis.longueur
        y_colis_min = colis.y
        y_colis_max = colis.y + colis.largeur

        if x_colis_min >= x_vide_max or x_colis_max <= x_vide_min or y_colis_min >= y_vide_max or y_colis_max <= y_vide_min:
            return [espaceVide]

        nouveaux_vides = []

        if x_vide_min < x_colis_min:
            nouveaux_vides.append(EspaceVide(
                x_vide_min,
                y_vide_min,
                x_colis_min - x_vide_min,
                espaceVide.largeur
            ))

        if y_vide_min < y_colis_min:
            nouveaux_vides.append(EspaceVide(
                x_vide_min,
                y_vide_min,
                espaceVide.longueur,
                y_colis_min - y_vide_min
            ))

        if x_colis_max < x_vide_max:
            nouveaux_vides.append(EspaceVide(
                x_colis_max,
                y_vide_min,
                x_vide_max - x_colis_max,
                espaceVide.largeur
            ))

        if y_colis_max < y_vide_max:
            nouveaux_vides.append(EspaceVide(
                x_vide_min,
                y_colis_max,
                espaceVide.longueur,
                y_vide_max - y_colis_max
            ))

        return nouveaux_vides

    def __nettoyage(self) -> None:
        vides_valides = []
        for i, vide1 in enumerate(self.espaces_vides):
            est_inclus = False
            for j, vide2 in enumerate(self.espaces_vides):
                if i != j:
                    if (vide1.x >= vide2.x and vide1.y >= vide2.y and vide1.x + vide1.longueur <= vide2.x + vide2.longueur and vide1.y + vide1.largeur <= vide2.y + vide2.largeur):
                        est_inclus = True
                        break
            if not est_inclus:
                vides_valides.append(vide1)

        self.espaces_vides = vides_valides

    def try_add(self, colis: Colis) -> tuple[bool, float, tuple[float, float], bool]:
        meilleur: dict[str, float | bool] = {
            "x": -1,
            "y": -1,
            "score": -float("inf"),
            "tourne": False
        }
        peut_rentrer = False

        for espace in self.espaces_vides:
            if espace.longueur >= colis.longueur and espace.largeur >= colis.largeur:
                peut_rentrer = True
                x = espace.x
                y = espace.y

                score_normal = -espace.surface - (espace.y * 0.001) - (espace.x * 0.0001)

                if score_normal > meilleur["score"]:
                    meilleur["score"] = float(score_normal)
                    meilleur["x"] = x
                    meilleur["y"] = y
                    meilleur["tourne"] = False

            if espace.longueur >= colis.largeur and espace.largeur >= colis.longueur:
                peut_rentrer = True

                score_tourne = -espace.surface - (espace.y * 0.001) - (espace.x * 0.0001)

                if score_tourne > meilleur["score"]:
                    meilleur["score"] = float(score_tourne)
                    meilleur["x"] = espace.x
                    meilleur["y"] = espace.y
                    meilleur["tourne"] = True

        if peut_rentrer:
            return True, meilleur["score"], (meilleur["x"], meilleur["y"]), meilleur["tourne"]

        return False, 0, (0, 0), False

    def get_surface_libre(self) -> float:
        surface_totale = self.max_longueur * self.max_largeur
        surface_occupee = sum(colis.longueur * colis.largeur for colis in self.colis)
        return round(surface_totale - surface_occupee, 5)

    def place_object(self, colis: Colis, x: float, y: float) -> None:
        colis.x = x
        colis.y = y
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