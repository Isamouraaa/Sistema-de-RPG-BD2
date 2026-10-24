import sqlite3

from entidades.mestre import Mestre

class CrudMestre:

    def __init__(self, conexao):
        self._conexao = conexao
        self._criarTabela()

    def _criarTabela(self):
        sql = """
            CREATE TABLE IF NOT EXISTS mestres (
                id_mestre INTEGER PRIMARY KEY AUTOINCREMENT,
                nome      VARCHAR(255) NOT NULL
            )
        """
        self._conexao.execute(sql)
        self._conexao.commit()

    def bdCriarMestre(self, mestre):
        sql = "INSERT INTO mestres (nome) VALUES (?)"
        cursor = self._conexao.execute(sql, (mestre.getNome(),))
        self._conexao.commit()
        mestre.setIdMestre(cursor.lastrowid)

    def bdEditarMestre(self, idMestre, mestre):
        sql = "UPDATE mestres SET nome = ? WHERE id_mestre = ?"
        self._conexao.execute(sql, (mestre.getNome(), idMestre))
        self._conexao.commit()

    def bdExcluirMestre(self, idMestre):
        sql = "DELETE FROM mestres WHERE id_mestre = ?"
        self._conexao.execute(sql, (idMestre,))
        self._conexao.commit()

    def bdListarMestres(self):
        sql = "SELECT id_mestre, nome FROM mestres ORDER BY id_mestre"
        cursor = self._conexao.execute(sql)
        return [
            Mestre(idMestre=row[0], nome=row[1])
            for row in cursor.fetchall()
        ]

    def bdListarMestre(self, idMestre):
        sql = "SELECT id_mestre, nome FROM mestres WHERE id_mestre = ?"
        cursor = self._conexao.execute(sql, (idMestre,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Mestre(idMestre=row[0], nome=row[1])