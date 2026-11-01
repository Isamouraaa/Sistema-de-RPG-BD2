import sqlite3
from cruds.CrudJogos import CrudJogos
from cruds.CrudMestre import CrudMestre
from serializadores.SerializadorJogo import SerializadorJogo
from serializadores.SerializadorMestre import SerializadorMestre
from entidades.jogo import Jogo
from entidades.mestre import Mestre

class ControladoraMestreJogo:

    def __init__(self, conexao):
        self._conexao = conexao
        self._crudJogos = CrudJogos(conexao)
        self._crudMestre = CrudMestre(conexao)
        self._serializadorMestre = SerializadorMestre()
        self._serializadorJogo = SerializadorJogo()

    # Operações de Mestre

    def criarMestre(self, mestre):
        dadosJson = self._serializadorMestre.serializarInfosMestres([mestre])
        mestreValidado = self._serializadorMestre.desserializarInfosMestres(dadosJson)[0]
        self._crudMestre.bdCriarMestre(mestreValidado)
        mestre.setIdMestre(mestreValidado.getIdMestre())

    def editarMestre(self, idMestre, mestre):
        dadosJson = self._serializadorMestre.serializarInfosMestres([mestre])
        mestreValidado = self._serializadorMestre.desserializarInfosMestres(dadosJson)[0]
        self._crudMestre.bdEditarMestre(idMestre, mestreValidado)

    def excluirMestre(self, idMestre):
        self._crudMestre.bdExcluirMestre(idMestre)

    def visualizarMestre(self, idMestre):
        mestre = self._crudMestre.bdListarMestre(idMestre)
        if mestre is None:
            return None
        dadosJson = self._serializadorMestre.serializarInfosMestres([mestre])
        return self._serializadorMestre.desserializarInfosMestres(dadosJson)[0]

    def listarMestres(self):
        mestres = self._crudMestre.bdListarMestres()
        dadosJson = self._serializadorMestre.serializarInfosMestres(mestres)
        return self._serializadorMestre.desserializarInfosMestres(dadosJson)

    # Operações de Jogo

    def criarJogo(self, jogo):
        dadosJson = self._serializadorJogo.serializarInfosJogos([jogo])
        jogoValidado = self._serializadorJogo.desserializarInfosJogos(dadosJson)[0]
        self._crudJogos.bdCriarJogo(jogoValidado)
        jogo.setIdJogo(jogoValidado.getIdJogo())

    def editarJogo(self, idJogo, jogo):
        dadosJson = self._serializadorJogo.serializarInfosJogos([jogo])
        jogoValidado = self._serializadorJogo.desserializarInfosJogos(dadosJson)[0]
        self._crudJogos.bdEditarJogo(idJogo, jogoValidado)

    def excluirJogo(self, idJogo):
        self._crudJogos.bdExcluirJogo(idJogo)

    def listarJogos(self):
        jogos = self._crudJogos.bdListarJogos()
        dadosJson = self._serializadorJogo.serializarInfosJogos(jogos)
        return self._serializadorJogo.desserializarInfosJogos(dadosJson)

    def obterJogo(self, idJogo):
        jogo = self._crudJogos.bdListarJogo(idJogo)
        if jogo is None:
            return None
        dadosJson = self._serializadorJogo.serializarInfosJogos([jogo])
        return self._serializadorJogo.desserializarInfosJogos(dadosJson)[0]

    # Estatísticas

    def estatisticasJogos(self, minPersonagens=0):
        jogosComEstatisticas = self._crudJogos.bdEstatisticasJogos(minPersonagens)
        dadosJson = self._serializadorJogo.serializarInfosJogos(jogosComEstatisticas)
        return self._serializadorJogo.desserializarInfosJogos(dadosJson)
