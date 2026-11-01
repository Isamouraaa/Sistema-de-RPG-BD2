class Mestre:

    def __init__(self, idMestre=None, nome=""):
        self._idMestre = idMestre
        self._nome = nome

    # idMestre
    def getIdMestre(self):
        return self._idMestre

    def setIdMestre(self, valor):
        self._idMestre = valor

    # nome
    def getNome(self):
        return self._nome

    def setNome(self, valor):
        self._nome = valor

    def __repr__(self):
        return f"Mestre(id={self._idMestre!r}, nome={self._nome!r})"