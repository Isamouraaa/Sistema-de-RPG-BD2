import sqlite3
from dataclasses import dataclass
from entidades.Personagem import Personagem
from serializadores.SerializadorPersonagem import PersonagemSerializadora


@dataclass
class EstatisticaPersonagemHabilidade:
    id_personagem: int
    nome_personagem: str
    classe: str
    nome_jogador: str
    total_habilidades: int
    soma_pontos_habilidades: int
    media_pontos_habilidade: float
    lista_habilidades: str
    poder_total: int


@dataclass
class EstatisticaHabilidadeClasse:
    id_habilidade: int
    nome_habilidade: str
    pontos_habilidade: int
    efeito: str
    total_personagens: int
    classe_mais_comum: str | None
    forca_media: float
    inteligencia_media: float


class CrudPersonagem:
    # aqui tem a conexao crud -> banco
    # aqui tem a conexao crud -> serializadora

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao
        self._conexao.execute("PRAGMA foreign_keys = ON;")
        self._serializador = PersonagemSerializadora()

    def bd_criar_personagem(self, personagem: Personagem) -> None:
        dados = self._serializador.personagem_para_dict(personagem)
        sql = """
            INSERT INTO PERSONAGEM (
                IDJogador, nomePersonagem, descricao, tipo, raca, classe,
                forca, inteligencia, vigor, destreza, sabedoria, iniciativa
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor = self._conexao.execute(sql, (
            dados["id_jogador"],
            dados["nome_personagem"],
            dados["descricao"],
            dados["tipo"],
            dados["raca"],
            dados["classe"],
            dados["forca"],
            dados["inteligencia"],
            dados["vigor"],
            dados["destreza"],
            dados["sabedoria"],
            dados["iniciativa"],
        ))
        self._conexao.commit()
        personagem.setIdPersonagem(cursor.lastrowid)

        for nome_hab in (personagem.getHabilidades() or []):
            self.bd_vincular_habilidade(personagem.getIdPersonagem(), nome_hab)

    def bd_editar_personagem(self, id_personagem: int, personagem: Personagem) -> None:
        dados = self._serializador.personagem_para_dict(personagem)
        sql = """
            UPDATE PERSONAGEM SET
                IDJogador = ?,
                nomePersonagem = ?,
                descricao = ?,
                tipo = ?,
                raca = ?,
                classe = ?,
                forca = ?,
                inteligencia = ?,
                vigor = ?,
                destreza = ?,
                sabedoria = ?,
                iniciativa = ?
            WHERE IDPersonagem = ?
        """
        self._conexao.execute(sql, (
            dados["id_jogador"],
            dados["nome_personagem"],
            dados["descricao"],
            dados["tipo"],
            dados["raca"],
            dados["classe"],
            dados["forca"],
            dados["inteligencia"],
            dados["vigor"],
            dados["destreza"],
            dados["sabedoria"],
            dados["iniciativa"],
            id_personagem,
        ))
        self._conexao.commit()

    def bd_excluir_personagem(self, id_personagem: int) -> None:
        sql = "DELETE FROM PERSONAGEM WHERE IDPersonagem = ?"
        self._conexao.execute(sql, (id_personagem,))
        self._conexao.commit()

    def bd_listar_personagens(self) -> list[Personagem]:
        sql = """
            SELECT IDPersonagem, IDJogador, nomePersonagem, descricao, tipo,
                   raca, classe, forca, inteligencia, vigor, destreza, sabedoria, iniciativa
            FROM PERSONAGEM ORDER BY IDPersonagem
        """
        cursor = self._conexao.execute(sql)
        return [self._linha_para_personagem(row) for row in cursor.fetchall()]

    def bd_listar_personagem(self, id_personagem: int) -> Personagem | None:
        sql = """
            SELECT IDPersonagem, IDJogador, nomePersonagem, descricao, tipo,
                   raca, classe, forca, inteligencia, vigor, destreza, sabedoria, iniciativa
            FROM PERSONAGEM WHERE IDPersonagem = ?
        """
        row = self._conexao.execute(sql, (id_personagem,)).fetchone()
        if row is None:
            return None
        return self._linha_para_personagem(row)

    def bd_obter_personagem(self, id_personagem: int) -> Personagem | None:
        return self.bd_listar_personagem(id_personagem)

    def bd_listar_personagens_por_jogador(self, id_jogador: int) -> list[Personagem]:
        sql = """
            SELECT IDPersonagem, IDJogador, nomePersonagem, descricao, tipo,
                   raca, classe, forca, inteligencia, vigor, destreza, sabedoria, iniciativa
            FROM PERSONAGEM WHERE IDJogador = ? ORDER BY nomePersonagem
        """
        cursor = self._conexao.execute(sql, (id_jogador,))
        return [self._linha_para_personagem(row) for row in cursor.fetchall()]

    def bd_listar_todas_habilidades(self) -> list[tuple]:
        sql = "SELECT IDhabilidade, nomeHabilidade, efeitoHabilidade, Pontos FROM HABILIDADE ORDER BY IDhabilidade"
        return self._conexao.execute(sql).fetchall()

    def bd_obter_habilidade(self, id_habilidade: int) -> tuple | None:
        sql = "SELECT IDhabilidade, nomeHabilidade, efeitoHabilidade, Pontos FROM HABILIDADE WHERE IDhabilidade = ?"
        return self._conexao.execute(sql, (id_habilidade,)).fetchone()

    def bd_listar_habilidades_detalhadas_personagem(self, id_personagem: int) -> list[tuple]:
        sql = """
            SELECT h.IDhabilidade, h.nomeHabilidade, h.efeitoHabilidade, h.Pontos
            FROM HABILIDADE h
            JOIN personagensHabilidades ph ON ph._idHabilidade = h.IDhabilidade
            WHERE ph._idPersonagem = ?
            ORDER BY h.IDhabilidade
        """
        return self._conexao.execute(sql, (id_personagem,)).fetchall()

    def bd_vincular_habilidade_por_id(self, id_personagem: int, id_habilidade: int) -> None:
        self._conexao.execute(
            "INSERT OR IGNORE INTO personagensHabilidades (_idPersonagem, _idHabilidade) VALUES (?, ?)",
            (id_personagem, id_habilidade),
        )
        self._conexao.commit()

    def bd_desvincular_habilidade_por_id(self, id_personagem: int, id_habilidade: int) -> None:
        self._conexao.execute(
            "DELETE FROM personagensHabilidades WHERE _idPersonagem = ? AND _idHabilidade = ?",
            (id_personagem, id_habilidade),
        )
        self._conexao.commit()

    def bd_criar_habilidade(self, nome_habilidade: str) -> int:
        self._conexao.execute(
            "INSERT OR IGNORE INTO HABILIDADE (nomeHabilidade) VALUES (?)",
            (nome_habilidade,)
        )
        self._conexao.commit()
        row = self._conexao.execute(
            "SELECT IDhabilidade FROM HABILIDADE WHERE nomeHabilidade = ?",
            (nome_habilidade,)
        ).fetchone()
        return row[0]

    def bd_vincular_habilidade(self, id_personagem: int, nome_habilidade: str) -> None:
        id_habilidade = self.bd_criar_habilidade(nome_habilidade)
        self._conexao.execute(
            "INSERT OR IGNORE INTO personagensHabilidades (_idPersonagem, _idHabilidade) VALUES (?, ?)",
            (id_personagem, id_habilidade),
        )
        self._conexao.commit()

    def bd_alterar_habilidade(self, id_personagem: int, hab_antiga: str, hab_nova: str) -> None:
        linha = self._conexao.execute(
            "SELECT IDhabilidade FROM HABILIDADE WHERE nomeHabilidade = ?", (hab_antiga,)
        ).fetchone()
        if linha is None:
            return
        id_antigo = linha[0]
        self._conexao.execute(
            "DELETE FROM personagensHabilidades WHERE _idPersonagem = ? AND _idHabilidade = ?",
            (id_personagem, id_antigo),
        )
        id_novo = self.bd_criar_habilidade(hab_nova)
        self._conexao.execute(
            "INSERT OR IGNORE INTO personagensHabilidades (_idPersonagem, _idHabilidade) VALUES (?, ?)",
            (id_personagem, id_novo),
        )
        self._conexao.commit()

    def bd_deletar_habilidade(self, id_personagem: int, nome_habilidade: str) -> None:
        self._conexao.execute(
            """
            DELETE FROM personagensHabilidades
            WHERE _idPersonagem = ?
              AND _idHabilidade = (SELECT IDhabilidade FROM HABILIDADE WHERE nomeHabilidade = ?)
            """,
            (id_personagem, nome_habilidade),
        )
        self._conexao.commit()

    def bd_listar_habilidades_personagem(self, id_personagem: int) -> list[str]:
        sql = """
            SELECT h.nomeHabilidade
            FROM HABILIDADE h
            JOIN personagensHabilidades ph ON ph._idHabilidade = h.IDhabilidade
            WHERE ph._idPersonagem = ?
            ORDER BY h.nomeHabilidade
        """
        rows = self._conexao.execute(sql, (id_personagem,)).fetchall()
        return [row[0] for row in rows]

    def bd_listar_personagens_por_habilidade(self, nome_habilidade: str) -> list[Personagem]:
        sql = """
            SELECT p.IDPersonagem, p.IDJogador, p.nomePersonagem, p.descricao, p.tipo,
                   p.raca, p.classe, p.forca, p.inteligencia, p.vigor, p.destreza,
                   p.sabedoria, p.iniciativa
            FROM PERSONAGEM p
            INNER JOIN personagensHabilidades ph ON ph._idPersonagem = p.IDPersonagem
            INNER JOIN HABILIDADE h ON h.IDhabilidade = ph._idHabilidade
            WHERE h.nomeHabilidade = ?
            ORDER BY p.nomePersonagem
        """
        cursor = self._conexao.execute(sql, (nome_habilidade,))
        return [self._linha_para_personagem(row) for row in cursor.fetchall()]

    def bd_listar_personagens_por_jogo(self, id_jogo: int) -> list[Personagem]:
        sql = """
            SELECT p.IDPersonagem, p.IDJogador, p.nomePersonagem, p.descricao, p.tipo,
                   p.raca, p.classe, p.forca, p.inteligencia, p.vigor, p.destreza,
                   p.sabedoria, p.iniciativa
            FROM PERSONAGEM p
            INNER JOIN JOGADOR j ON j.IDJogador = p.IDJogador
            INNER JOIN JOGOSJOGADOR jj ON jj.IDJogador = j.IDJogador
            WHERE jj.IDjogo = ?
            ORDER BY p.nomePersonagem
        """
        cursor = self._conexao.execute(sql, (id_jogo,))
        return [self._linha_para_personagem(row) for row in cursor.fetchall()]

    def bd_estatisticas_personagens_habilidades(self) -> list[EstatisticaPersonagemHabilidade]:
        sql = """
            SELECT
                p.IDPersonagem,
                p.nomePersonagem,
                p.classe,
                COALESCE(j.nomejogador, 'Sem jogador') AS nome_jogador,
                COUNT(h.IDhabilidade)                  AS total_habilidades,
                COALESCE(SUM(h.Pontos), 0)             AS soma_pontos_habilidades,
                ROUND(COALESCE(AVG(h.Pontos), 0.0), 2) AS media_pontos_habilidade,
                COALESCE(GROUP_CONCAT(h.nomeHabilidade, ', '), 'Nenhuma') AS lista_habilidades,
                ((p.forca + p.inteligencia + p.vigor) + COALESCE(SUM(h.Pontos), 0) * 2) AS poder_total
            FROM PERSONAGEM p
            LEFT JOIN JOGADOR j ON j.IDJogador = p.IDJogador
            LEFT JOIN personagensHabilidades ph ON ph._idPersonagem = p.IDPersonagem
            LEFT JOIN HABILIDADE h ON h.IDhabilidade = ph._idHabilidade
            GROUP BY p.IDPersonagem, p.nomePersonagem, p.classe, j.nomejogador, p.forca, p.inteligencia, p.vigor
            ORDER BY poder_total DESC, p.nomePersonagem ASC
        """
        cursor = self._conexao.execute(sql)
        return [
            EstatisticaPersonagemHabilidade(
                id_personagem=row[0],
                nome_personagem=row[1],
                classe=row[2],
                nome_jogador=row[3],
                total_habilidades=row[4],
                soma_pontos_habilidades=row[5],
                media_pontos_habilidade=float(row[6]),
                lista_habilidades=row[7],
                poder_total=row[8],
            )
            for row in cursor.fetchall()
        ]

    def bd_estatisticas_habilidades_classes(self) -> list[EstatisticaHabilidadeClasse]:
        sql = """
            SELECT
                h.IDhabilidade,
                h.nomeHabilidade,
                COALESCE(h.Pontos, 0)                  AS pontos_habilidade,
                COALESCE(h.efeitoHabilidade, '')       AS efeito,
                COUNT(DISTINCT p.IDPersonagem)         AS total_personagens,
                (
                    SELECT p2.classe
                    FROM PERSONAGEM p2
                    INNER JOIN personagensHabilidades ph2 ON ph2._idPersonagem = p2.IDPersonagem
                    WHERE ph2._idHabilidade = h.IDhabilidade
                      AND p2.classe IS NOT NULL
                      AND p2.classe != ''
                    GROUP BY p2.classe
                    ORDER BY COUNT(*) DESC
                    LIMIT 1
                )                                      AS classe_mais_comum,
                ROUND(COALESCE(AVG(p.forca), 0.0), 2)        AS forca_media,
                ROUND(COALESCE(AVG(p.inteligencia), 0.0), 2) AS inteligencia_media
            FROM HABILIDADE h
            LEFT JOIN personagensHabilidades ph ON ph._idHabilidade = h.IDhabilidade
            LEFT JOIN PERSONAGEM p ON p.IDPersonagem = ph._idPersonagem
            GROUP BY h.IDhabilidade, h.nomeHabilidade, h.Pontos, h.efeitoHabilidade
            ORDER BY total_personagens DESC, h.nomeHabilidade ASC
        """
        cursor = self._conexao.execute(sql)
        return [
            EstatisticaHabilidadeClasse(
                id_habilidade=row[0],
                nome_habilidade=row[1],
                pontos_habilidade=row[2],
                efeito=row[3],
                total_personagens=row[4],
                classe_mais_comum=row[5],
                forca_media=float(row[6]),
                inteligencia_media=float(row[7]),
            )
            for row in cursor.fetchall()
        ]

    def serializar(self) -> str:
        return self._serializador.serializar_infos_personagens(self.bd_listar_personagens())

    def desserializar(self, dados: str) -> list[Personagem]:
        return self._serializador.desserializar_infos_personagem(dados)

    def _linha_para_personagem(self, linha) -> Personagem:
        id_personagem = linha[0]
        habilidades = self.bd_listar_habilidades_personagem(id_personagem)
        return self._serializador.linha_para_personagem(linha, habilidades)


PersonagemCrud = CrudPersonagem
