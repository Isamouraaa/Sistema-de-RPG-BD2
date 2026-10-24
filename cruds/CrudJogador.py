import sqlite3

from entidades.jogador import Jogador

class JogadorCrud:

    def __init__(self, conexao):
        self._conexao = conexao
        self._criarTabela()

    def _criarTabela(self):
        sql = """
            CREATE TABLE IF NOT EXISTS jogadores (
                _idJogador   INTEGER PRIMARY KEY AUTOINCREMENT,
                _nomeJogador VARCHAR(255) NOT NULL
            )
        """
        self._conexao.execute(sql)
        self._conexao.commit()

    def bdCriarJogador(self, jogador):
        sql = "INSERT INTO jogadores (_nomeJogador) VALUES (?)"
        cursor = self._conexao.execute(sql, (jogador.getNomeJogador(),))
        self._conexao.commit()
        jogador.setIdJogador(cursor.lastrowid)

    def bdEditarJogador(self, idJogador, jogador):
        sql = "UPDATE jogadores SET _nomeJogador = ? WHERE _idJogador = ?"
        self._conexao.execute(sql, (jogador.getNomeJogador(), idJogador))
        self._conexao.commit()

    def bdExcluirJogador(self, idJogador):
        sql = "DELETE FROM jogadores WHERE _idJogador = ?"
        self._conexao.execute(sql, (idJogador,))
        self._conexao.commit()

    def bdListarJogadores(self):
        sql = "SELECT _idJogador, _nomeJogador FROM jogadores ORDER BY _idJogador"
        cursor = self._conexao.execute(sql)
        return [
            Jogador(idJogador=row[0], nomeJogador=row[1])
            for row in cursor.fetchall()
        ]

    def bdObterJogador(self, idJogador):
        sql = "SELECT _idJogador, _nomeJogador FROM jogadores WHERE _idJogador = ?"
        cursor = self._conexao.execute(sql, (idJogador,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Jogador(idJogador=row[0], nomeJogador=row[1])