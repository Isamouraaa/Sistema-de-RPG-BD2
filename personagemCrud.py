from __future__ import annotations
from personagem import Personagem
from jogador import Jogador
import sqlite3

class PersonagemCrud:

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao
        self._criar_tabelas()

        '''    def __init__(self,idPersonagem,nomePersonagem,descricao,tipo,raca,
                 classe,forca,inteligencia,vigor,destreza,sabedoria,
                 iniciativa,habilidades,idJogador):
        '''

    def _criar_tabelas(self) -> None:
        sql1 = """
            CREATE TABLE IF NOT EXISTS personagens (
                _idPersonagem           INTEGER PRIMARY KEY AUTOINCREMENT,
                _nomePersonagem         VARCHAR(255) NOT NULL,
                _descricao              VARCHAR(255) NOT NULL,
                _tipo                   VARCHAR(255) NOT NULL,
                _raca                   VARCHAR(255) NOT NULL,
                _classe                 VARCHAR(255) NOT NULL,
                _forca                  INT NOT NULL,
                _inteligencia           INT NOT NULL,
                _vigor                  INT NOT NULL,
                _destreza               INT NOT NULL,
                _sabedoria              INT NOT NULL,
                _iniciativa             INT NOT NULL,
                _idJogador              INT,
                CONSTRAINT FK_Jogadores FOREIGN KEY (_idJogador)
                REFERENCES jogadores(_idJogador)
            );
        """

        sql2 = """
            CREATE TABLE IF NOT EXISTS habilidades (
                _idHabilidade           INTEGER PRIMARY KEY AUTOINCREMENT,
                _nomeHabilidade         VARCHAR(255) NOT NULL
            );
        """

        sql3 = """
            CREATE TABLE IF NOT EXISTS personagensHabilidades (
                _idPersonagem           INT NOT NULL,
                _idHabilidade           INT NOT NULL,
                PRIMARY KEY (_idPersonagem, _idHabilidade),
                CONSTRAINT fk_ph_personagem
                    FOREIGN KEY (_idPersonagem)
                    REFERENCES personagens(_idPersonagem)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                CONSTRAINT fk_ph_habilidade
                    FOREIGN KEY (_idHabilidade)
                    REFERENCES habilidades(_idHabilidade)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            );
        """
        self._conexao.execute(sql1)
        self._conexao.execute(sql2)
        self._conexao.execute(sql3)

        self._conexao.execute("PRAGMA foreign_keys = ON;") #Ativa FKs no sqlite

        self._conexao.commit()

    def bd_criar_personagem(self, personagem: Personagem) -> None:
        sql = """
        INSERT INTO personagens (_nomePersonagem, _descricao, _tipo, _raca, _classe, _forca,
            _inteligencia, _vigor, _destreza, _sabedoria, _iniciativa,
            _idJogador)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        cursor = self._conexao.execute(sql, (personagem._nomePersonagem, personagem._descricao,
                                       personagem._tipo, personagem._raca, personagem._classe,
                                       personagem._forca, personagem._inteligencia, personagem._vigor,
                                       personagem._destreza, personagem._sabedoria, personagem._iniciatica,
                                       personagem._idJogador))
        self._conexao.commit()

        for nome_hab in (personagem.getHabilidades() or []):
            self.vincular_habilidade(personagem.getIdPersonagem(), nome_hab)
        
        personagem._idPersonagem = cursor.lastrowid

    def bd_criar_habilidade(self, _nomeHabilidade: str) -> int:
        sql = """
        INSERT OR IGNORE INTO habilidades (_nomeHabilidade) VALUES (?);
        """

        self._conexao.execute(sql, (_nomeHabilidade,))
        self._conexao.commit()

    def bd_vincular_habilidade(self, _idPersonagem: int, _nomeHabilidade: str) -> None:
        _idHabilidade = self.bd_criar_habilidade(_nomeHabilidade,)
        sql = """
            INSERT OR IGNORE INTO personagensHabilidades (_idPersonagem, _idHabilidade)
            VALUES (?, ?)     
        """
        self._conexao.execute(sql, (_idPersonagem, _idHabilidade,))
        self._conexao.commit()

    def bd_alterar_habilidade(self, _idPersonagem, hab_antiga, hab_nova) -> None:
        linha = self._conexao.execute(
            "SELECT _idHabilidade FROM habilidades WHERE _nomeHabilidade = ?",
            (hab_antiga,)
            ).fetchone()

        idAntigo = linha[0]
        self._conexao.execute(
            """DELETE FROM personagensHabilidades WHERE _idPersonagem =?" \
            AND _idHabilidade = ?
            """, (_idPersonagem, idAntigo),
            )

        idNovo = self.bd_criar_habilidade(hab_nova)
        self._conexao.execute("""
            INSERT OR IGNORE INTO personagensHabilidades (_idPersonagem, _idHabilidade)
            VALUES (?, ?)
        """, (_idPersonagem, idNovo),
        )
        self._conexao.commit()

    def bd_deletar_habilidade(self, _idPersonagem, nomeHab) -> None:
        self._conexao.execute("""
            DELETE FROM personagensHabilidades
            WHERE _idPersonagem = ?
            AND _idHabilidade = (SELECT _idHabilidade
                                 FROM habilidades
                                 WHERE _nomeHabilidade = ?)

        """, (_idPersonagem, nomeHab),
        )

        self._conexao.commit()

    def bd_listar_habilidades_personagem(self, _idPersonagem) -> list[str]:
        sql = """
            SELECT habilidades._nomeHabilidade
            FROM habilidades
            JOIN personagensHabilidades ON personagensHabilidades._idHabilidade = habilidades._idHabilidade
            WHERE personagensHabilidades._idPersonagem = ?
            ORDER BY habilidades._nomeHabilidade
        """
        return [habs[0] for habs in self._conexao.execute(sql, (_idPersonagem,)).fetchall()]

    def bd_editar_personagem(self, _idPersonagem: int, personagem: Personagem) -> None:
        sql = """
        UPDATE personagens SET _nomePersonagem = ?,
                               _descricao = ?,
                               _tipo = ?,
                               _raca = ?,
                               _classe = ?,
                               _forca = ?,
                               _inteligencia = ?,
                               _vigor = ?,
                               _destreza = ?,
                               _sabedoria = ?,
                               _iniciativa = ?,
            WHERE _idPersonagem = ?"""
        self._conexao.execute(sql, (personagem.getNomePersonagem, personagem.getDescricao,
                                       personagem.getTipo, personagem.getRaca, personagem.getClasse,
                                       personagem.getForca, personagem.getInteligencia, personagem.getVigor,
                                       personagem.getDestreza, personagem.getSabedoria, personagem.getIniciativa,
                                       personagem.getIdJogador, _idPersonagem))
        self._conexao.commit()

    def bd_excluir_personagem(self, _idPersonagem: int) -> None:
        sql = "DELETE FROM personagens WHERE _idPersonagem = ?"
        cursor = self._conexao.execute(sql, (_idPersonagem,))
        self._conexao.commit()

    def bd_listar_personagens(self) -> list[Personagem]:
        sql = """SELECT _idPersonagem, _nomePersonagem
                 FROM personagens ORDER BY _idPersonagem"""
        cursor = self._conexao.execute(sql)
        return [
            Personagem(_idPersonagem=row[0],
                       _nomePersonagem=row[1])
        ##### ARRUMAR LISTA HABILIDADES, TABELA???
            for row in cursor.fetchall()
        ]

    def bd_listar_personagem(self, _idPersonagem: int, personagem: Personagem) -> None:
        sql = """SELECT _idPersonagem, _nomePersonagem, _descricao, _tipo, _raca, _classe, _forca,
                                       _inteligencia, _vigor, _destreza, _sabedoria, _iniciativa,
                                       _habilidades
                 FROM personagens WHERE _idPersonagem = ?"""
        cursor = self._conexao.execute(sql, (personagem._nomePersonagem, personagem._descricao,
                                       personagem._tipo, personagem._raca, personagem._classe,
                                       personagem._forca, personagem._inteligencia, personagem._vigor,
                                       personagem._destreza, personagem._sabedoria, personagem._iniciatica,
                                       personagem._habilidades, personagem._idJogador))
        row = cursor.fetchone()
        if row is None:
            return None
        return personagem(_idPersonagem=row[0],
                       _nomePersonagem=row[1],
                       _descricao=row[2],
                       _tipo=row[3],
                       _raca=row[4],
                       _classe=row[5],
                       _forca=row[6],
                       _inteligencia=row[7],
                       _vigor=row[8],
                       _destreza=row[9],
                       _sabedoria=row[10],
                       _iniciativa=row[11],
                       _habilidades=row[12])

    def bd_listar_personagens_por_jogador(self, _idJogador: int, jogador: Jogador) -> None:
        sql = ""

        cursor = self._conexao.execute()

        return ()