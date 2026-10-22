class Personagem:
    def __init__(
        self,
        idPersonagem: int | None = None,
        nomePersonagem: str = "",
        descricao: str = "",
        tipo: str = "",
        raca: str = "",
        classe: str = "",
        forca: int = 10,
        inteligencia: int = 10,
        vigor: int = 10,
        destreza: int = 10,
        sabedoria: int = 10,
        iniciativa: int = 10,
        habilidades: list[str] | None = None,
        idJogador: int | None = None,
    ) -> None:
        self._idPersonagem = idPersonagem
        self._nomePersonagem = nomePersonagem
        self._descricao = descricao
        self._tipo = tipo
        self._raca = raca
        self._classe = classe
        self._forca = forca
        self._inteligencia = inteligencia
        self._vigor = vigor
        self._destreza = destreza
        self._sabedoria = sabedoria
        self._iniciativa = iniciativa
        self._habilidades = habilidades if habilidades is not None else []
        self._idJogador = idJogador

    def getIdPersonagem(self) -> int | None:
        return self._idPersonagem

    def getNomePersonagem(self) -> str:
        return self._nomePersonagem

    def getDescricao(self) -> str:
        return self._descricao

    def getTipo(self) -> str:
        return self._tipo

    def getRaca(self) -> str:
        return self._raca

    def getClasse(self) -> str:
        return self._classe

    def getForca(self) -> int:
        return self._forca

    def getInteligencia(self) -> int:
        return self._inteligencia

    def getVigor(self) -> int:
        return self._vigor

    def getDestreza(self) -> int:
        return self._destreza

    def getSabedoria(self) -> int:
        return self._sabedoria

    def getIniciativa(self) -> int:
        return self._iniciativa

    def getHabilidades(self) -> list[str]:
        return list(self._habilidades)

    def getIdJogador(self) -> int | None:
        return self._idJogador

    def setIdPersonagem(self, id_val: int | None) -> None:
        self._idPersonagem = id_val

    def setNomePersonagem(self, nome: str) -> None:
        self._nomePersonagem = nome

    def setDescricao(self, novaDescricao: str) -> None:
        self._descricao = novaDescricao

    def setTipo(self, novoTipo: str) -> None:
        self._tipo = novoTipo

    def setRaca(self, novaRaca: str) -> None:
        self._raca = novaRaca

    def setClasse(self, novaClasse: str) -> None:
        self._classe = novaClasse

    def setForca(self, novaForca: int) -> None:
        self._forca = novaForca

    def setInteligencia(self, novaInt: int) -> None:
        self._inteligencia = novaInt

    def setVigor(self, novoVigor: int) -> None:
        self._vigor = novoVigor

    def setDestreza(self, novaDex: int) -> None:
        self._destreza = novaDex

    def setSabedoria(self, novaSab: int) -> None:
        self._sabedoria = novaSab

    def setIniciativa(self, novaInic: int) -> None:
        self._iniciativa = novaInic

    def setHabilidades(self, novasHab: list[str]) -> None:
        self._habilidades = list(novasHab)

    def setIdJogador(self, idJoga: int | None) -> None:
        self._idJogador = idJoga

    def __repr__(self) -> str:
        return f"Personagem(id={self._idPersonagem!r}, nome={self._nomePersonagem!r}, classe={self._classe!r})"
