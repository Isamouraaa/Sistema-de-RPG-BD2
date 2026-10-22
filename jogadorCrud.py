from __future__ import annotations
from jogador import Jogador
import sqlite3

class JogadorCrud:

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao
        self._criar_tabela()

    def _criar_tabela(self) -> None:
        sql = """
            CREATE TABLE IF NOT EXISTS jogadores (
                _idJogador    INTEGER PRIMARY KEY AUTOINCREMENT,
                _nomeJogador         VARCHAR(255) NOT NULL,
            )
        """
        self._conexao.execute(sql)
        self._conexao.commit()

    def bd_criar_jogador(self, jogador: Jogador) -> None:
        sql = "INSERT INTO jogadores (_nomeJogador) VALUES (?)"
        cursor = self._conexao.execute(sql, (jogador._nomeJogador))
        self._conexao.commit()
        jogador._idJogador = cursor.lastrowid

    def bd_editar_jogador(self, _idJogador: int, jogador: Jogador) -> None:
        sql = "UPDATE jogos SET _nomeJogador = ?, WHERE _idJogador = ?"
        self._conexao.execute(sql, (jogador._nomeJogador, _idJogador))
        self._conexao.commit()

    def bd_excluir_jogador(self, _idJogador: int) -> None:
        sql = "DELETE FROM jogadores WHERE _idJogador = ?"
        self._conexao.execute(sql, (_idJogador,))
        self._conexao.commit()

    def bd_listar_jogadores(self) -> list[Jogador]:
        sql = "SELECT _idJogador, _nomeJogador, FROM jogadores ORDER BY _idJogador"
        cursor = self._conexao.execute(sql)
        return [
            Jogador(_idJogador=row[0], _nomeJogador=row[1])
            for row in cursor.fetchall()
        ]

    def bd_obter_jogador(self, _idJogador: int) -> Jogador | None:
        sql = "SELECT _idJogador, _nomeJogador, FROM jogos WHERE _idJogador = ?"
        cursor = self._conexao.execute(sql, (_idJogador))
        row = cursor.fetchone()
        if row is None:
            return None
        return Jogador(_idJogador=row[0], _nomeJogador=row[1])