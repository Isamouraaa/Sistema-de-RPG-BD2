from __future__ import annotations

import sqlite3

from crud_jogos import CrudJogos, EstatisticaJogo
from crud_mestre import CrudMestre
from jogo import Jogo
from mestre import Mestre


class ControladoraGeral:

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao
        self._crud_jogos = CrudJogos(conexao)
        self._crud_mestre = CrudMestre(conexao)

    def CriarMestre(self, mestre: Mestre) -> None:
        self._crud_mestre.bd_criar_mestre(mestre)

    def ExcluirMestre(self, idMestre: int) -> None:
        self._crud_mestre.bd_excluir_mestre(idMestre)

    def EditarMestre(self, idMestre: int, mestre: Mestre) -> None:
        self._crud_mestre.bd_editar_mestre(idMestre, mestre)

    def VisualizarMestre(self, idMestre: int) -> Mestre | None:
        return self._crud_mestre.bd_listar_mestre(idMestre)

    def CriarJogo(self, jogo: Jogo) -> None:
        self._crud_jogos.bd_criar_jogo(jogo)

    def EditarJogo(self, idJogo: int, jogo: Jogo) -> None:
        self._crud_jogos.bd_editar_jogo(idJogo, jogo)

    def ExcluirJogo(self, idJogo: int) -> None:
        self._crud_jogos.bd_excluir_jogo(idJogo)

    def ListarJogos(self) -> list[Jogo]:
        return self._crud_jogos.bd_listar_jogos()

    def ObterJogo(self, idJogo: int) -> Jogo | None:
        return self._crud_jogos.bd_listar_jogo(idJogo)

    def EstatisticasJogos(self, min_personagens: int = 0) -> list[EstatisticaJogo]:
        return self._crud_jogos.bd_estatisticas_jogos(min_personagens)
