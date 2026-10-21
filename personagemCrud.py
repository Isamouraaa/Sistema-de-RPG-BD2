from __future__ import annotations
from personagem import Personagem
from jogador import Jogador
import sqlite3

class PersonagemCrud:

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao
        self._criar_tabela()

        '''    def __init__(self,idPersonagem,nomePersonagem,descricao,tipo,raca,
                 classe,forca,inteligencia,vigor,destreza,sabedoria,
                 iniciativa,habilidades,idJogador):
        '''

    def _criar_tabela(self) -> None:
        sql = """
            CREATE TABLE IF NOT EXISTS personagens (
                _idPersonagem   INTEGER PRIMARY KEY AUTOINCREMENT,
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
                _habilidades            TEXT NOT NULL,
                _idJogador              INT,
                CONSTRAINT FK_Jogadores FOREIGN KEY (_idJogador)
                REFERENCES jogadores(_idJogador)
            );
        """
        self._conexao.execute(sql)
        self._conexao.commit()

    def bd_criar_personagem(self, personagem: Personagem) -> None:
        sql = """ INSERT INTO jogadores (_nomePersonagem, _descricao, _tipo, _raca, _classe, _forca,
                                         _inteligencia, _vigor, _destreza, _sabedoria, _iniciativa,
                                         _habilidades, _idJogador)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        cursor = self._conexao.execute(sql, (personagem._nomePersonagem, personagem._descricao,
                                       personagem._tipo, personagem._raca, personagem._classe,
                                       personagem._forca, personagem._inteligencia, personagem._vigor,
                                       personagem._destreza, personagem._sabedoria, personagem._iniciatica,
                                       personagem._habilidades, personagem._idJogador))
        ##### ARRUMAR LISTA HABILIDADES, TABELA???
        self._conexao.commit()
        personagem._idPersonagem = cursor.lastrowid

    def bd_editar_personagem(self, _idPersonagem: int, personagem: Personagem) -> None:
        sql = """UPDATE personagens SET _nomePersonagem = ?,
                                    SET _descricao = ?,
                                    SET _tipo = ?,
                                    SET _raca = ?,
                                    SET _classe = ?,
                                    SET _forca = ?,
                                    SET _inteligencia = ?,
                                    SET _vigor = ?,
                                    SET _destreza = ?,
                                    SET _sabedoria = ?,
                                    SET _iniciativa = ?,
                                    SET _habilidades = ?,
        WHERE _idPersonagem = ?"""
        cursor = self._conexao.execute(sql, (personagem._nomePersonagem, personagem._descricao,
                                       personagem._tipo, personagem._raca, personagem._classe,
                                       personagem._forca, personagem._inteligencia, personagem._vigor,
                                       personagem._destreza, personagem._sabedoria, personagem._iniciatica,
                                       personagem._habilidades, personagem._idJogador))
        ##### ARRUMAR LISTA HABILIDADES, TABELA???
        self._conexao.commit()

    def bd_excluir_personagem(self, _idPersonagem: int) -> None:
        sql = "DELETE FROM personagens WHERE _idPersonagem = ?"
        cursor = self._conexao.execute(sql, (_idPersonagem))
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
                 FROM jogos WHERE _idJogador = ?"""
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