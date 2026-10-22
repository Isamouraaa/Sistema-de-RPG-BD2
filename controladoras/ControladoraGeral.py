import sqlite3
from cruds.CrudJogos import CrudJogos, EstatisticaJogo
from cruds.CrudMestre import CrudMestre
from entidades.Jogo import Jogo
from entidades.Mestre import Mestre


class ControladoraGeral:
    # aqui tem a conexao controladora -> crud

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao
        self._crud_jogos = CrudJogos(conexao)
        self._crud_mestre = CrudMestre(conexao)

    def ObterMestreUnico(self) -> Mestre | None:
        return self._crud_mestre.bd_obter_mestre_unico()

    def CriarMestre(self, mestre: Mestre) -> None:
        self._crud_mestre.bd_criar_mestre(mestre)

    def EditarMestre(self, idMestre: int, mestre: Mestre) -> None:
        self._crud_mestre.bd_editar_mestre(idMestre, mestre)

    def ExcluirMestre(self, idMestre: int) -> None:
        self._crud_mestre.bd_excluir_mestre(idMestre)

    def VisualizarMestre(self, idMestre: int | None = None) -> Mestre | None:
        if idMestre is None:
            return self._crud_mestre.bd_obter_mestre_unico()
        return self._crud_mestre.bd_listar_mestre(idMestre)

    def ListarMestres(self) -> list[Mestre]:
        return self._crud_mestre.bd_listar_mestres()

    def ListarJogosDoMestre(self, idMestre: int) -> list[tuple[int, str, str]]:
        return self._crud_mestre.bd_listar_jogos_do_mestre(idMestre)

    def CriarJogo(self, jogo: Jogo) -> None:
        if jogo.id_mestre is None:
            mestre_unico = self._crud_mestre.bd_obter_mestre_unico()
            if mestre_unico:
                jogo.id_mestre = mestre_unico.id_mestre
        self._crud_jogos.bd_criar_jogo(jogo)

    def EditarJogo(self, idJogo: int, jogo: Jogo) -> None:
        if jogo.id_mestre is None:
            mestre_unico = self._crud_mestre.bd_obter_mestre_unico()
            if mestre_unico:
                jogo.id_mestre = mestre_unico.id_mestre
        self._crud_jogos.bd_editar_jogo(idJogo, jogo)

    def ExcluirJogo(self, idJogo: int) -> None:
        self._crud_jogos.bd_excluir_jogo(idJogo)

    def ListarJogos(self) -> list[Jogo]:
        return self._crud_jogos.bd_listar_jogos()

    def ObterJogo(self, idJogo: int) -> Jogo | None:
        return self._crud_jogos.bd_listar_jogo(idJogo)

    def EstatisticasJogos(self, min_personagens: int = 0) -> list[EstatisticaJogo]:
        return self._crud_jogos.bd_estatisticas_jogos(min_personagens)

    def SerializarJogos(self) -> str:
        return self._crud_jogos.serializar()

    def DesserializarJogos(self, dados: str) -> list[Jogo]:
        return self._crud_jogos.desserializar(dados)

    def SerializarMestres(self) -> str:
        return self._crud_mestre.serializar()

    def DesserializarMestres(self, dados: str) -> list[Mestre]:
        return self._crud_mestre.desserializar(dados)
