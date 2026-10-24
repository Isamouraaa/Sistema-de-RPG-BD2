class Jogador:
    def __init__(self, idJogador=None, nomeJogador=None):
        self._idJogador = idJogador
        self._nomeJogador = nomeJogador

    def getId(self):
        return self._idJogador

    def getNome(self):
        return self._nomeJogador

    def setId(self, novoId):
        self._idJogador = novoId

    def setNome(self, novoNome):
        self._nomeJogador = novoNome

    def getIdJogador(self):
        return self._idJogador

    def getNomeJogador(self):
        return self._nomeJogador

    def setIdJogador(self, novoId):
        self._idJogador = novoId

    def setNomeJogador(self, novoNome):
        self._nomeJogador = novoNome
