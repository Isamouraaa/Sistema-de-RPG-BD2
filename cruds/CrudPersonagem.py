import sqlite3
from entidades.Personagem import Personagem
from serializadores.SerializadorPersonagem import PersonagemSerializadora


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

    def bd_listar_personagens_por_tipo(self, tipo: str) -> list[Personagem]:
        sql = """
            SELECT p.IDPersonagem, p.IDJogador, p.nomePersonagem, p.descricao, p.tipo,
                   p.raca, p.classe, p.forca, p.inteligencia, p.vigor, p.destreza,
                   p.sabedoria, p.iniciativa
            FROM PERSONAGEM p
            WHERE LOWER(p.tipo) LIKE LOWER(?)
            ORDER BY p.IDPersonagem
        """
        cursor = self._conexao.execute(sql, (f"%{tipo}%",))
        return [self._linha_para_personagem(row) for row in cursor.fetchall()]

    def bd_estatisticas_personagens_habilidades(self) -> list[dict]:
        sql = """
            SELECT
                p.IDPersonagem,
                p.nomePersonagem,
                p.classe,
                j.nomejogador AS nome_jogador,
                COUNT(h.IDhabilidade) AS total_habilidades,
                SUM(h.Pontos) AS soma_pontos_habilidades,
                AVG(h.Pontos) AS media_pontos_habilidade,
                GROUP_CONCAT(h.nomeHabilidade, ', ') AS lista_habilidades,
                (p.forca + p.inteligencia + p.vigor) AS atributos_base
            FROM PERSONAGEM p
            LEFT JOIN JOGADOR j ON j.IDJogador = p.IDJogador
            LEFT JOIN personagensHabilidades ph ON ph._idPersonagem = p.IDPersonagem
            LEFT JOIN HABILIDADE h ON h.IDhabilidade = ph._idHabilidade
            GROUP BY p.IDPersonagem, p.nomePersonagem, p.classe, j.nomejogador, p.forca, p.inteligencia, p.vigor
            ORDER BY atributos_base DESC, p.nomePersonagem ASC
        """
        cursor = self._conexao.execute(sql)
        resultado = []
        for row in cursor.fetchall():
            soma_pontos = row[5] or 0
            media_pontos = round(row[6], 2) if row[6] is not None else 0.0
            poder_total = (row[8] or 0) + (soma_pontos * 2)
            resultado.append({
                "id_personagem": row[0],
                "nome_personagem": row[1],
                "classe": row[2],
                "nome_jogador": row[3] or "Sem jogador",
                "total_habilidades": row[4] or 0,
                "soma_pontos_habilidades": soma_pontos,
                "media_pontos_habilidade": media_pontos,
                "lista_habilidades": row[7] or "Nenhuma",
                "poder_total": poder_total,
            })
        return resultado

    def bd_estatisticas_habilidades_classes(self) -> list[dict]:
        sql = """
            SELECT
                h.IDhabilidade,
                h.nomeHabilidade,
                h.Pontos AS pontos_habilidade,
                h.efeitoHabilidade AS efeito,
                COUNT(p.IDPersonagem) AS total_personagens,
                AVG(p.forca) AS forca_media,
                AVG(p.inteligencia) AS inteligencia_media
            FROM HABILIDADE h
            LEFT JOIN personagensHabilidades ph ON ph._idHabilidade = h.IDhabilidade
            LEFT JOIN PERSONAGEM p ON p.IDPersonagem = ph._idPersonagem
            GROUP BY h.IDhabilidade, h.nomeHabilidade, h.Pontos, h.efeitoHabilidade
            ORDER BY total_personagens DESC, h.nomeHabilidade ASC
        """
        cursor = self._conexao.execute(sql)
        resultado = []
        for row in cursor.fetchall():
            resultado.append({
                "id_habilidade": row[0],
                "nome_habilidade": row[1],
                "pontos_habilidade": row[2] or 0,
                "efeito": row[3] or "",
                "total_personagens": row[4] or 0,
                "classe_mais_comum": "-",
                "forca_media": round(row[5], 2) if row[5] is not None else 0.0,
                "inteligencia_media": round(row[6], 2) if row[6] is not None else 0.0,
            })
        return resultado

    def bd_estatisticas_por_tipo(self) -> list[dict]:
        sql = """
            SELECT
                p.tipo,
                COUNT(p.IDPersonagem) AS total_personagens,
                AVG(p.forca)          AS forca_media,
                AVG(p.vigor)          AS vigor_medio,
                AVG(p.inteligencia)   AS inteligencia_media,
                AVG(p.iniciativa)     AS iniciativa_media
            FROM PERSONAGEM p
            GROUP BY p.tipo
            ORDER BY total_personagens DESC
        """
        cursor = self._conexao.execute(sql)
        resultado = []
        for row in cursor.fetchall():
            resultado.append({
                "tipo": row[0] or "Não Definido",
                "total_personagens": row[1] or 0,
                "forca_media": round(row[2], 1) if row[2] is not None else 0.0,
                "vigor_medio": round(row[3], 1) if row[3] is not None else 0.0,
                "inteligencia_media": round(row[4], 1) if row[4] is not None else 0.0,
                "iniciativa_media": round(row[5], 1) if row[5] is not None else 0.0,
            })
        return resultado

    def bd_estatisticas_tipos_por_jogo(self) -> list[dict]:
        sql = """
            SELECT
                j.IDjogo,
                j.nome AS nome_jogo,
                m.nome AS nome_mestre,
                COUNT(p.IDPersonagem) AS total_geral_personagens
            FROM JOGO j
            LEFT JOIN MESTRE m ON m.IDmestre = j.IDmestre
            LEFT JOIN JOGOSJOGADOR jj ON jj.IDjogo = j.IDjogo
            LEFT JOIN PERSONAGEM p ON p.IDJogador = jj.IDJogador
            GROUP BY j.IDjogo, j.nome, m.nome
            ORDER BY total_geral_personagens DESC, j.nome ASC
        """
        cursor = self._conexao.execute(sql)
        resultado = []
        for row in cursor.fetchall():
            resultado.append({
                "id_jogo": row[0],
                "nome_jogo": row[1],
                "nome_mestre": row[2] or "Sem mestre",
                "total_geral_personagens": row[3] or 0,
            })
        return resultado

    def bd_consultar_tipo_e_caracteristica(
        self, tipo: str = "", classe: str = "", forca_minima: int = 0
    ) -> list[dict]:
        sql = """
            SELECT
                p.IDPersonagem,
                p.nomePersonagem,
                p.tipo,
                p.classe,
                p.raca,
                p.forca,
                p.inteligencia,
                p.vigor,
                p.iniciativa,
                j.nomejogador
            FROM PERSONAGEM p
            LEFT JOIN JOGADOR j ON j.IDJogador = p.IDJogador
            WHERE p.tipo LIKE ?
              AND p.classe LIKE ?
              AND p.forca >= ?
            ORDER BY p.forca DESC, p.nomePersonagem ASC
        """
        cursor = self._conexao.execute(sql, (f"%{tipo}%", f"%{classe}%", forca_minima))
        resultado = []
        for row in cursor.fetchall():
            id_p = row[0]
            habs = self.bd_listar_habilidades_personagem(id_p)
            resultado.append({
                "id_personagem": id_p,
                "nome_personagem": row[1],
                "tipo": row[2] or "-",
                "classe": row[3] or "-",
                "raca": row[4] or "-",
                "forca": row[5],
                "inteligencia": row[6],
                "vigor": row[7],
                "iniciativa": row[8],
                "nome_jogador": row[9] or "Sem jogador",
                "total_habilidades": len(habs),
                "lista_habilidades": ", ".join(habs) if habs else "Nenhuma",
            })
        return resultado

    def serializar(self) -> str:
        return self._serializador.serializar_infos_personagens(self.bd_listar_personagens())

    def desserializar(self, dados: str) -> list[Personagem]:
        return self._serializador.desserializar_infos_personagem(dados)

    def _linha_para_personagem(self, linha) -> Personagem:
        id_personagem = linha[0]
        habilidades = self.bd_listar_habilidades_personagem(id_personagem)
        return self._serializador.linha_para_personagem(linha, habilidades)


PersonagemCrud = CrudPersonagem
