class Jogador:
    def __init__(self, idJogador=None, nomeJogador=None):
        self._idJogador = idJogador
        self._nomeJogador = nomeJogador

    def getId(self):
        return self._idJogador

    def setId(self, novoId):
        self._idJogador = novoId

    def getNome(self):
        return self._nomeJogador

    def setNome(self, novoNome):
        self._nomeJogador = novoNome
