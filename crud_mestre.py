from __future__ import annotations

import sqlite3

from mestre import Mestre


class CrudMestre:

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao
        self._criar_tabela()

    def _criar_tabela(self) -> None:
        sql = """
            CREATE TABLE IF NOT EXISTS mestres (
                id_mestre INTEGER PRIMARY KEY AUTOINCREMENT,
                nome      VARCHAR(255) NOT NULL
            )
        """
        self._conexao.execute(sql)
        self._conexao.commit()

    def bd_criar_mestre(self, mestre: Mestre) -> None:
        sql = "INSERT INTO mestres (nome) VALUES (?)"
        cursor = self._conexao.execute(sql, (mestre.nome,))
        self._conexao.commit()
        mestre.id_mestre = cursor.lastrowid

    def bd_editar_mestre(self, id_mestre: int, mestre: Mestre) -> None:
        sql = "UPDATE mestres SET nome = ? WHERE id_mestre = ?"
        self._conexao.execute(sql, (mestre.nome, id_mestre))
        self._conexao.commit()

    def bd_excluir_mestre(self, id_mestre: int) -> None:
        sql = "DELETE FROM mestres WHERE id_mestre = ?"
        self._conexao.execute(sql, (id_mestre,))
        self._conexao.commit()

    def bd_listar_mestres(self) -> list[Mestre]:
        sql = "SELECT id_mestre, nome FROM mestres ORDER BY id_mestre"
        cursor = self._conexao.execute(sql)
        return [
            Mestre(id_mestre=row[0], nome=row[1])
            for row in cursor.fetchall()
        ]

    def bd_listar_mestre(self, id_mestre: int) -> Mestre | None:
        sql = "SELECT id_mestre, nome FROM mestres WHERE id_mestre = ?"
        cursor = self._conexao.execute(sql, (id_mestre,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Mestre(id_mestre=row[0], nome=row[1])
