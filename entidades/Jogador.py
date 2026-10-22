class Jogador:
    def __init__(self, idJogador: int | None = None, nomeJogador: str = "") -> None:
        self._idJogador = idJogador
        self._nomeJogador = nomeJogador

    def getId(self) -> int | None:
        return self._idJogador

    def getIdJogador(self) -> int | None:
        return self._idJogador

    def setId(self, novoId: int | None) -> None:
        self._idJogador = novoId

    def getNome(self) -> str:
        return self._nomeJogador

    def setNome(self, novoNome: str) -> None:
        self._nomeJogador = novoNome

    def __repr__(self) -> str:
        return f"Jogador(id={self._idJogador!r}, nome={self._nomeJogador!r})"
