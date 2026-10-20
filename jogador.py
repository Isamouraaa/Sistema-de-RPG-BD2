class Jogador:
    def __init__(self,idJogador,nomeJogador):
        self._idJogador = idJogador
        self._nomeJogador = nomeJogador

    def getId(self):
        return self._idJogador

    def getNome(self):
        return self._nomeJogador

    def setNome(self, novoNome):
        self._nomeJogador = novoNome
