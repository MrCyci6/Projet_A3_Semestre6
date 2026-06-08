# cyriac
class Node:
    __id = 0
    def __init__(self, niveau: int, utilite_total: float, poids_total: float, borne: float = 0, sac: list = None):
        self.__id = Node.__id
        Node.__id += 1

        self.__niveau = niveau
        self.__utilite_total = utilite_total
        self.__poids_total = poids_total
        self.__borne = borne
        self.__sac = sac if sac is not None else []

    def setBorne(self, borne: float):
        self.__borne = borne

    def getNiveau(self):
        return self.__niveau

    def getUtiliteTotal(self):
        return self.__utilite_total

    def getPoidsTotal(self):
        return self.__poids_total

    def getBorne(self):
        return self.__borne

    def getSac(self):
        return self.__sac