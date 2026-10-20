from __future__ import annotations

from jogador import Jogador
from personagem import Personagem


class Jogo:

    def __init__(
        self,
        id_jogo: int | None,
        nome: str,
        descricao: str,
        id_mestre: int | None = None,
        jogadores: list[Jogador] | None = None,
        npcs: list[Personagem] | None = None,
        criaturas: list[Personagem] | None = None,
    ) -> None:
        self._id_jogo = id_jogo
        self._nome = nome
        self._descricao = descricao
        self._id_mestre = id_mestre
        self._jogadores: list[Jogador] = jogadores or []
        self._npcs: list[Personagem] = npcs or []
        self._criaturas: list[Personagem] = criaturas or []

    @property
    def id_jogo(self) -> int | None:
        return self._id_jogo

    @id_jogo.setter
    def id_jogo(self, valor: int) -> None:
        self._id_jogo = valor

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        self._nome = valor

    @property
    def descricao(self) -> str:
        return self._descricao

    @descricao.setter
    def descricao(self, valor: str) -> None:
        self._descricao = valor

    @property
    def id_mestre(self) -> int | None:
        return self._id_mestre

    @id_mestre.setter
    def id_mestre(self, valor: int | None) -> None:
        self._id_mestre = valor

    @property
    def jogadores(self) -> list[Jogador]:
        return self._jogadores

    @property
    def npcs(self) -> list[Personagem]:
        return self._npcs

    @property
    def criaturas(self) -> list[Personagem]:
        return self._criaturas

    #isso aqui e so pra facilita minha vida dps eu tiro
    def __repr__(self) -> str:
        return (
            f"Jogo(id={self._id_jogo!r}, nome={self._nome!r}, "
            f"descricao={self._descricao!r}, id_mestre={self._id_mestre!r})"
        )
