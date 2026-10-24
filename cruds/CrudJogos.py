import sqlite3
from entidades.jogo import Jogo


class CrudJogos:

    def __init__(self, conexao):
        self._conexao = conexao
        self._criarTabela()

    def _criarTabela(self):
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

    def bdCriarJogo(self, jogo):
        sql = "INSERT INTO jogos (nome, descricao, id_mestre) VALUES (?, ?, ?)"
        cursor = self._conexao.execute(
            sql, 
            (jogo.getNome(), jogo.getDescricao(), jogo.getIdMestre())
        )
        self._conexao.commit()
        jogo.setIdJogo(cursor.lastrowid)

    def bdEditarJogo(self, idJogo, jogo):
        sql = "UPDATE jogos SET nome = ?, descricao = ?, id_mestre = ? WHERE id_jogo = ?"
        self._conexao.execute(
            sql, 
            (jogo.getNome(), jogo.getDescricao(), jogo.getIdMestre(), idJogo)
        )
        self._conexao.commit()

    def bdExcluirJogo(self, idJogo):
        sql = "DELETE FROM jogos WHERE id_jogo = ?"
        self._conexao.execute(sql, (idJogo,))
        self._conexao.commit()

    def bdListarJogos(self):
        sql = "SELECT id_jogo, nome, descricao, id_mestre FROM jogos ORDER BY id_jogo"
        cursor = self._conexao.execute(sql)
        return [
            Jogo(idJogo=row[0], nome=row[1], descricao=row[2], idMestre=row[3])
            for row in cursor.fetchall()
        ]

    def bdListarJogo(self, idJogo):
        sql = "SELECT id_jogo, nome, descricao, id_mestre FROM jogos WHERE id_jogo = ?"
        cursor = self._conexao.execute(sql, (idJogo,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Jogo(idJogo=row[0], nome=row[1], descricao=row[2], idMestre=row[3])

    def bdEstatisticasJogos(self, minPersonagens=0):
        sql = """
            SELECT
                j.id_jogo,
                j.nome                                                          AS nome_jogo,
                j.descricao,
                m.nome                                                          AS nome_mestre,
                COUNT(DISTINCT p._idJogador)                                    AS total_jogadores,
                COUNT(DISTINCT p._idPersonagem)                                 AS total_personagens,
                (
                    SELECT p2._classe
                    FROM   personagens p2
                    WHERE  p2._idJogo = j.id_jogo
                      AND  p2._classe IS NOT NULL
                    GROUP BY p2._classe
                    ORDER BY COUNT(*) DESC
                    LIMIT 1
                )                                                               AS classe_mais_comum,
                COALESCE(AVG(p._forca), 0.0)                                    AS forca_media
            FROM  jogos j
            LEFT JOIN mestres     m   ON m.id_mestre   = j.id_mestre
            LEFT JOIN personagens p   ON p._idJogo     = j.id_jogo
            LEFT JOIN jogadores   jog ON jog._idJogador = p._idJogador
            GROUP BY j.id_jogo, j.nome, j.descricao, m.nome
            HAVING COUNT(DISTINCT p._idPersonagem) >= ?
            ORDER BY total_personagens DESC, j.nome ASC
        """
        cursor = self._conexao.execute(sql, (minPersonagens,))
        return [
            Jogo(
                idJogo=row[0],
                nome=row[1],
                descricao=row[2],
                nomeMestre=row[3],
                totalJogadores=row[4],
                totalPersonagens=row[5],
                classeMaisComum=row[6],
                forcaMedia=round(row[7], 2),
            )
            for row in cursor.fetchall()
        ]