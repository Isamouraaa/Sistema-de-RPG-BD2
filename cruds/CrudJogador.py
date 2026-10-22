import sqlite3
from entidades.Jogador import Jogador
from serializadores.SerializadorJogador import SerializadorJogador


class CrudJogador:
    # aqui tem a conexao crud -> banco
    # aqui tem a conexao crud -> serializadora

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao
        self._serializador = SerializadorJogador()

    def bd_criar_jogador(self, jogador: Jogador) -> None:
        dados = self._serializador.jogador_para_dict(jogador)
        sql = "INSERT INTO JOGADOR (nomejogador) VALUES (?)"
        cursor = self._conexao.execute(sql, (dados["_nomeJogador"],))
        self._conexao.commit()
        jogador.setId(cursor.lastrowid)

    def bd_editar_jogador(self, id_jogador: int, jogador: Jogador) -> None:
        dados = self._serializador.jogador_para_dict(jogador)
        sql = "UPDATE JOGADOR SET nomejogador = ? WHERE IDJogador = ?"
        self._conexao.execute(sql, (dados["_nomeJogador"], id_jogador))
        self._conexao.commit()

    def bd_excluir_jogador(self, id_jogador: int) -> None:
        sql = "DELETE FROM JOGADOR WHERE IDJogador = ?"
        self._conexao.execute(sql, (id_jogador,))
        self._conexao.commit()

    def bd_listar_jogadores(self) -> list[Jogador]:
        sql = "SELECT IDJogador, nomejogador FROM JOGADOR ORDER BY IDJogador"
        cursor = self._conexao.execute(sql)
        return [self._serializador.linha_para_jogador(row) for row in cursor.fetchall()]

    def bd_listar_jogador(self, id_jogador: int) -> Jogador | None:
        sql = "SELECT IDJogador, nomejogador FROM JOGADOR WHERE IDJogador = ?"
        cursor = self._conexao.execute(sql, (id_jogador,))
        row = cursor.fetchone()
        if row is None:
            return None
        return self._serializador.linha_para_jogador(row)

    def bd_obter_jogador(self, id_jogador: int) -> Jogador | None:
        return self.bd_listar_jogador(id_jogador)

    def serializar(self) -> str:
        return self._serializador.serializar_infos_jogadores(self.bd_listar_jogadores())

    def desserializar(self, dados: str) -> list[Jogador]:
        return self._serializador.desserializar_infos_jogadores(dados)


JogadorCrud = CrudJogador
