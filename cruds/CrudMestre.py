import sqlite3
from entidades.Mestre import Mestre
from serializadores.SerializadorMestre import SerializadorMestre


class CrudMestre:
    # aqui tem a conexao crud -> banco
    # aqui tem a conexao crud -> serializadora

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao
        self._serializador = SerializadorMestre()

    def bd_criar_mestre(self, mestre: Mestre) -> None:
        dados = self._serializador.mestre_para_dict(mestre)
        sql = "INSERT INTO MESTRE (nome) VALUES (?)"
        cursor = self._conexao.execute(sql, (dados["nome"],))
        self._conexao.commit()
        mestre.id_mestre = cursor.lastrowid

    def bd_editar_mestre(self, id_mestre: int, mestre: Mestre) -> None:
        dados = self._serializador.mestre_para_dict(mestre)
        sql = "UPDATE MESTRE SET nome = ? WHERE IDmestre = ?"
        self._conexao.execute(sql, (dados["nome"], id_mestre))
        self._conexao.commit()

    def bd_excluir_mestre(self, id_mestre: int) -> None:
        sql = "DELETE FROM MESTRE WHERE IDmestre = ?"
        self._conexao.execute(sql, (id_mestre,))
        self._conexao.commit()

    def bd_obter_mestre_unico(self) -> Mestre | None:
        mestres = self.bd_listar_mestres()
        return mestres[0] if mestres else None

    def bd_listar_mestres(self) -> list[Mestre]:
        sql = "SELECT IDmestre, nome FROM MESTRE ORDER BY IDmestre"
        cursor = self._conexao.execute(sql)
        return [self._serializador.linha_para_mestre(row) for row in cursor.fetchall()]

    def bd_listar_mestre(self, id_mestre: int) -> Mestre | None:
        sql = "SELECT IDmestre, nome FROM MESTRE WHERE IDmestre = ?"
        cursor = self._conexao.execute(sql, (id_mestre,))
        row = cursor.fetchone()
        if row is None:
            return None
        return self._serializador.linha_para_mestre(row)

    def bd_listar_jogos_do_mestre(self, id_mestre: int) -> list[tuple[int, str, str]]:
        sql = "SELECT IDjogo, nome, COALESCE(descricao, '') FROM JOGO WHERE IDmestre = ? ORDER BY IDjogo"
        cursor = self._conexao.execute(sql, (id_mestre,))
        return cursor.fetchall()

    def serializar(self) -> str:
        return self._serializador.serializar_infos_mestres(self.bd_listar_mestres())

    def desserializar(self, dados: str) -> list[Mestre]:
        return self._serializador.desserializar_infos_mestres(dados)
