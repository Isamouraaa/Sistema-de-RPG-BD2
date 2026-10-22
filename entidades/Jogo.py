from entidades.Jogador import Jogador
from entidades.Personagem import Personagem


class Jogo:
    def __init__(
        self,
        id_jogo: int | None = None,
        nome: str = "",
        descricao: str = "",
        id_mestre: int | None = None,
        jogadores: list[Jogador] | None = None,
        npcs: list[Personagem] | None = None,
        criaturas: list[Personagem] | None = None,
    ) -> None:
        self.id_jogo = id_jogo
        self.nome = nome
        self.descricao = descricao
        self.id_mestre = id_mestre
        self.jogadores: list[Jogador] = jogadores or []
        self.npcs: list[Personagem] = npcs or []
        self.criaturas: list[Personagem] = criaturas or []

    def getId(self) -> int | None:
        return self.id_jogo

    def getNome(self) -> str:
        return self.nome

    def getDescricao(self) -> str:
        return self.descricao

    def getIdMestre(self) -> int | None:
        return self.id_mestre

    def __repr__(self) -> str:
        return (
            f"Jogo(id={self.id_jogo!r}, nome={self.nome!r}, "
            f"descricao={self.descricao!r}, id_mestre={self.id_mestre!r})"
        )
