from __future__ import annotations

import sqlite3
from dataclasses import dataclass

from jogo import Jogo


@dataclass
class EstatisticaJogo:
    """Resultado da consulta de estatísticas por jogo."""
    id_jogo: int
    nome_jogo: str
    descricao: str
    nome_mestre: str | None
    total_jogadores: int
    total_personagens: int
    classe_mais_comum: str | None
    forca_media: float


class CrudJogos:

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao
        self._criar_tabela()

    def _criar_tabela(self) -> None:
        sql = """
            CREATE TABLE IF NOT EXISTS jogos (
                id_jogo   INTEGER PRIMARY KEY AUTOINCREMENT,
                nome      VARCHAR(255) NOT NULL,
                descricao VARCHAR(1000) NOT NULL,
                id_mestre INTEGER,
                FOREIGN KEY (id_mestre) REFERENCES mestres(id_mestre)
            )
        """
        self._conexao.execute(sql)
        self._conexao.commit()

    def bd_criar_jogo(self, jogo: Jogo) -> None:
        sql = "INSERT INTO jogos (nome, descricao, id_mestre) VALUES (?, ?, ?)"
        cursor = self._conexao.execute(sql, (jogo.nome, jogo.descricao, jogo.id_mestre))
        self._conexao.commit()
        jogo.id_jogo = cursor.lastrowid

    def bd_editar_jogo(self, id_jogo: int, jogo: Jogo) -> None:
        sql = "UPDATE jogos SET nome = ?, descricao = ?, id_mestre = ? WHERE id_jogo = ?"
        self._conexao.execute(sql, (jogo.nome, jogo.descricao, jogo.id_mestre, id_jogo))
        self._conexao.commit()

    def bd_excluir_jogo(self, id_jogo: int) -> None:
        sql = "DELETE FROM jogos WHERE id_jogo = ?"
        self._conexao.execute(sql, (id_jogo,))
        self._conexao.commit()

    def bd_listar_jogos(self) -> list[Jogo]:
        sql = "SELECT id_jogo, nome, descricao, id_mestre FROM jogos ORDER BY id_jogo"
        cursor = self._conexao.execute(sql)
        return [
            Jogo(id_jogo=row[0], nome=row[1], descricao=row[2], id_mestre=row[3])
            for row in cursor.fetchall()
        ]

    def bd_listar_jogo(self, id_jogo: int) -> Jogo | None:
        sql = "SELECT id_jogo, nome, descricao, id_mestre FROM jogos WHERE id_jogo = ?"
        cursor = self._conexao.execute(sql, (id_jogo,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Jogo(id_jogo=row[0], nome=row[1], descricao=row[2], id_mestre=row[3])

    def bd_estatisticas_jogos(
        self,
        min_personagens: int = 0,
    ) -> list[EstatisticaJogo]:
        sql = """
            SELECT
                j.id_jogo,
                j.nome                                          AS nome_jogo,
                j.descricao,
                m.nome                                          AS nome_mestre,
                COUNT(DISTINCT p._idJogador)                    AS total_jogadores,
                COUNT(DISTINCT p._idPersonagem)                 AS total_personagens,
                (
                    -- subconsulta correlacionada: classe com mais personagens neste jogo
                    SELECT p2._classe
                    FROM   personagens p2
                    INNER JOIN jogadores jog2 ON jog2._idJogador = p2._idJogador
                    WHERE  p2._classe IS NOT NULL
                    GROUP BY p2._classe
                    ORDER BY COUNT(*) DESC
                    LIMIT 1
                )                                               AS classe_mais_comum,
                COALESCE(AVG(p._forca), 0.0)                    AS forca_media
            FROM  jogos j
            LEFT JOIN mestres    m   ON m.id_mestre  = j.id_mestre
            LEFT JOIN jogadores  jog ON jog._idJogador IS NOT NULL
            LEFT JOIN personagens p  ON p._idJogador  = jog._idJogador
            GROUP BY j.id_jogo, j.nome, j.descricao, m.nome
            HAVING COUNT(DISTINCT p._idPersonagem) >= ?
            ORDER BY total_personagens DESC, j.nome ASC
        """
        cursor = self._conexao.execute(sql, (min_personagens,))
        return [
            EstatisticaJogo(
                id_jogo=row[0],
                nome_jogo=row[1],
                descricao=row[2],
                nome_mestre=row[3],
                total_jogadores=row[4],
                total_personagens=row[5],
                classe_mais_comum=row[6],
                forca_media=round(row[7], 2),
            )
            for row in cursor.fetchall()
        ]
