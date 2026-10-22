import sqlite3
from entidades.Jogo import Jogo
from serializadores.SerializadorJogo import SerializadorJogo


class CrudJogos:
    # aqui tem a conexao crud -> banco
    # aqui tem a conexao crud -> serializadora

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao
        self._serializador = SerializadorJogo()

    def bd_criar_jogo(self, jogo: Jogo) -> None:
        dados = self._serializador.jogo_para_dict(jogo)
        sql = "INSERT INTO JOGO (IDmestre, nome, descricao) VALUES (?, ?, ?)"
        cursor = self._conexao.execute(sql, (dados["id_mestre"], dados["nome"], dados["descricao"]))
        self._conexao.commit()
        jogo.id_jogo = cursor.lastrowid

    def bd_editar_jogo(self, id_jogo: int, jogo: Jogo) -> None:
        dados = self._serializador.jogo_para_dict(jogo)
        sql = "UPDATE JOGO SET nome = ?, descricao = ?, IDmestre = ? WHERE IDjogo = ?"
        self._conexao.execute(sql, (dados["nome"], dados["descricao"], dados["id_mestre"], id_jogo))
        self._conexao.commit()

    def bd_excluir_jogo(self, id_jogo: int) -> None:
        sql = "DELETE FROM JOGO WHERE IDjogo = ?"
        self._conexao.execute(sql, (id_jogo,))
        self._conexao.commit()

    def bd_listar_jogos(self) -> list[Jogo]:
        sql = "SELECT IDjogo, IDmestre, nome, descricao FROM JOGO ORDER BY IDjogo"
        cursor = self._conexao.execute(sql)
        return [self._serializador.linha_para_jogo(row) for row in cursor.fetchall()]

    def bd_listar_jogo(self, id_jogo: int) -> Jogo | None:
        sql = "SELECT IDjogo, IDmestre, nome, descricao FROM JOGO WHERE IDjogo = ?"
        cursor = self._conexao.execute(sql, (id_jogo,))
        row = cursor.fetchone()
        if row is None:
            return None
        return self._serializador.linha_para_jogo(row)

    def serializar(self) -> str:
        return self._serializador.serializar_infos_jogos(self.bd_listar_jogos())

    def desserializar(self, dados: str) -> list[Jogo]:
        return self._serializador.desserializar_infos_jogos(dados)

    def bd_estatisticas_jogos(self, min_personagens: int = 0) -> list[dict]:
        sql = """
            SELECT
                j.IDjogo,
                j.nome                                              AS nome_jogo,
                j.descricao                                         AS descricao,
                m.nome                                              AS nome_mestre,
                COUNT(jj.IDJogador)                                 AS total_jogadores,
                COUNT(p.IDPersonagem)                               AS total_personagens,
                (
                    SELECT p2.classe
                    FROM   PERSONAGEM p2
                    INNER JOIN JOGOSJOGADOR jj2 ON jj2.IDJogador = p2.IDJogador
                    WHERE  jj2.IDjogo = j.IDjogo
                      AND  p2.classe IS NOT NULL
                      AND  p2.classe != ''
                    GROUP BY p2.classe
                    ORDER BY COUNT(*) DESC
                    LIMIT 1
                )                                                   AS classe_mais_comum,
                AVG(p.forca)                                        AS forca_media
            FROM  JOGO j
            LEFT JOIN MESTRE        m   ON m.IDmestre    = j.IDmestre
            LEFT JOIN JOGOSJOGADOR  jj  ON jj.IDjogo     = j.IDjogo
            LEFT JOIN PERSONAGEM    p   ON p.IDJogador   = jj.IDJogador
            GROUP BY j.IDjogo, j.nome, j.descricao, m.nome
            HAVING COUNT(p.IDPersonagem) >= ?
            ORDER BY total_personagens DESC, j.nome ASC
        """
        cursor = self._conexao.execute(sql, (min_personagens,))
        return [
            {
                "id_jogo": row[0],
                "nome_jogo": row[1],
                "descricao": row[2] or "",
                "nome_mestre": row[3] or "Sem mestre",
                "total_jogadores": row[4] or 0,
                "total_personagens": row[5] or 0,
                "classe_mais_comum": row[6] or "-",
                "forca_media": round(row[7], 2) if row[7] is not None else 0.0,
            }
            for row in cursor.fetchall()
        ]
