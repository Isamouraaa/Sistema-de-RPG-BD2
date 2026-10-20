from __future__ import annotations

import sqlite3

from jogo import Jogo


class CrudJogos:

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao
        self._criar_tabela()

    def _criar_tabela(self) -> None:
        sql = """
            CREATE TABLE IF NOT EXISTS jogos (
                id_jogo   INTEGER PRIMARY KEY AUTOINCREMENT,
                nome      VARCHAR(255) NOT NULL,
                descricao VARCHAR(1000) NOT NULL
            )
        """
        self._conexao.execute(sql)
        self._conexao.commit()

    def bd_criar_jogo(self, jogo: Jogo) -> None:
        sql = "INSERT INTO jogos (nome, descricao) VALUES (?, ?)"
        cursor = self._conexao.execute(sql, (jogo.nome, jogo.descricao))
        self._conexao.commit()
        jogo.id_jogo = cursor.lastrowid

    def bd_editar_jogo(self, id_jogo: int, jogo: Jogo) -> None:
        sql = "UPDATE jogos SET nome = ?, descricao = ? WHERE id_jogo = ?"
        self._conexao.execute(sql, (jogo.nome, jogo.descricao, id_jogo))
        self._conexao.commit()

    def bd_excluir_jogo(self, id_jogo: int) -> None:
        sql = "DELETE FROM jogos WHERE id_jogo = ?"
        self._conexao.execute(sql, (id_jogo,))
        self._conexao.commit()

    def bd_listar_jogos(self) -> list[Jogo]:
        sql = "SELECT id_jogo, nome, descricao FROM jogos ORDER BY id_jogo"
        cursor = self._conexao.execute(sql)
        return [
            Jogo(id_jogo=row[0], nome=row[1], descricao=row[2])
            for row in cursor.fetchall()
        ]

    def bd_listar_jogo(self, id_jogo: int) -> Jogo | None:
        sql = "SELECT id_jogo, nome, descricao FROM jogos WHERE id_jogo = ?"
        cursor = self._conexao.execute(sql, (id_jogo,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Jogo(id_jogo=row[0], nome=row[1], descricao=row[2])
