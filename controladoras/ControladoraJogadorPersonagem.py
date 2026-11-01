import sqlite3

from entidades.jogador import Jogador
from cruds.CrudJogador import CrudJogador
from entidades.personagem import Personagem
from cruds.CrudPersonagem import CrudPersonagem
from serializadores.SerializadorJogador import SerializadorJogador
from serializadores.SerializadorPersonagem import SerializadorPersonagem


class ControladoraJogadorPersonagem:

    def __init__(self, conexao):
        self._conexao = conexao
        self._crudJogador = CrudJogador(conexao)
        self._crudPersonagem = CrudPersonagem(conexao)
        self._serializadorJogador = SerializadorJogador()
        self._serializadorPersonagem = SerializadorPersonagem()

    # --- Operações de Jogador ---

    def criarJogador(self, jogador):
        dadosJson = self._serializadorJogador.serializarInfosJogadores([jogador])
        jogadorValidado = self._serializadorJogador.desserializarInfosJogadores(dadosJson)[0]
        self._crudJogador.bdCriarJogador(jogadorValidado)
        jogador.setIdJogador(jogadorValidado.getIdJogador())

    def editarJogador(self, idJogador, jogador):
        dadosJson = self._serializadorJogador.serializarInfosJogadores([jogador])
        jogadorValidado = self._serializadorJogador.desserializarInfosJogadores(dadosJson)[0]
        self._crudJogador.bdEditarJogador(idJogador, jogadorValidado)

    def excluirJogador(self, idJogador):
        self._crudJogador.bdExcluirJogador(idJogador)

    def listarJogadores(self):
        jogadores = self._crudJogador.bdListarJogadores()
        dadosJson = self._serializadorJogador.serializarInfosJogadores(jogadores)
        return self._serializadorJogador.desserializarInfosJogadores(dadosJson)

    def obterJogador(self, idJogador):
        jogador = self._crudJogador.bdObterJogador(idJogador)
        if jogador is None:
            return None
        dadosJson = self._serializadorJogador.serializarInfosJogadores([jogador])
        return self._serializadorJogador.desserializarInfosJogadores(dadosJson)[0]

    # --- Operações de Personagem ---

    def criarPersonagem(self, personagem):
        dadosJson = self._serializadorPersonagem.serializarInfosPersonagens([personagem])
        personagemValidado = self._serializadorPersonagem.desserializarInfosPersonagens(dadosJson)[0]
        self._crudPersonagem.bdCriarPersonagem(personagemValidado)
        personagem.setIdPersonagem(personagemValidado.getIdPersonagem())

    def editarPersonagem(self, idPersonagem, personagem):
        dadosJson = self._serializadorPersonagem.serializarInfosPersonagens([personagem])
        personagemValidado = self._serializadorPersonagem.desserializarInfosPersonagens(dadosJson)[0]
        self._crudPersonagem.bdEditarPersonagem(idPersonagem, personagemValidado)

    def excluirPersonagem(self, idPersonagem):
        self._crudPersonagem.bdExcluirPersonagem(idPersonagem)

    def listarTodosPersonagens(self):
        return self._crudPersonagem.bdListarTodosPersonagens()

    def obterPersonagem(self, idPersonagem):
        personagem = self._crudPersonagem.bdObterPersonagem(idPersonagem)
        if personagem is None:
            return None
        dadosJson = self._serializadorPersonagem.serializarInfosPersonagens([personagem])
        return self._serializadorPersonagem.desserializarInfosPersonagens(dadosJson)[0]

    def listarPersonagensPorJogador(self, idJogador):
        return self._crudPersonagem.bdListarPersonagensPorJogador(idJogador)

    # --- Operações de Habilidade ---

    def vincularHabilidade(self, idPersonagem, nomeHabilidade):
        self._crudPersonagem.bdVincularHabilidade(idPersonagem, nomeHabilidade)

    def alterarHabilidade(self, idPersonagem, nomeAntigo, nomeNovo):
        self._crudPersonagem.bdAlterarHabilidade(idPersonagem, nomeAntigo, nomeNovo)

    def deletarHabilidade(self, idPersonagem, nomeHabilidade):
        self._crudPersonagem.bdDeletarHabilidade(idPersonagem, nomeHabilidade)

    def listarHabilidades(self, idPersonagem):
        return self._crudPersonagem.bdListarHabilidadesPersonagem(idPersonagem)
