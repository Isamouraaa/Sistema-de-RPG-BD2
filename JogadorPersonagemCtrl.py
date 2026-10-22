from __future__ import annotations
import sqlite3
from jogadorCrud import JogadorCrud
from jogador import Jogador
from personagemCrud import PersonagemCrud
from personagem import Personagem

class Controladora:

    #jogador
    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao
        self._crud_jogador = JogadorCrud(conexao)
        self._crud_personagem = PersonagemCrud(conexao)

    def criarJogador(self, jogador: Jogador) -> None:
        self._crud_jogador.bd_criar_jogador(jogador)

    def editarJogador(self, _idJogador: int, jogador: Jogador) -> None:
        self._crud_jogador.bd_editar_jogador(_idJogador, jogador)

    def excluirJogador(self, _idJogador: int, jogador: Jogador) -> None:
        self._crud_jogador.bd_excluir_jogador(_idJogador)

    def listarJogadores(self) -> list[Jogador]:
        self._crud_jogador.bd_listar_jogadores()

    def obterJogador(self, _idJogador: int) -> Jogador:
        self._crud_jogador.bd_obter_jogador(_idJogador)

    #personagem
    def criarPersonagem(self, personagem: Personagem):
        self._crud_personagem.bd_criar_personagem(personagem)

    def criarHabilidade(self, nomeHab: str, _idPersonagem: int):
        self._crud_personagem.bd_vincular_habilidade(_idPersonagem, nomeHab)

    def editarPersonagem(self, _idJogador: int, jogador: Jogador) -> None:
        self._crud_jogador.bd_editar_jogador(_idJogador, jogador)

    def listarTodosPersonagens(self) -> list[str]:
        self._crud_personagem.bd_listar_todos_personagens()

    def obter_personagem(self, _idPersonagem: int) -> Personagem | None:
        self._crud_personagem.bd_obter_personagem(_idPersonagem)

    def listarPersonagensPorJogador(self, _idJogador: int) -> list[tuple[int,str]]:
        self._crud_personagem.bd_listar_personagens_por_jogador(_idJogador)

    def vincular_habilidade(self, id_personagem: int, nome_habilidade: str) -> None:
        self._crud_personagem.bd_vincular_habilidade(id_personagem, nome_habilidade)

    def alterar_habilidade(self, id_personagem: int, nome_antigo: str, nome_novo: str) -> None:
        self._crud_personagem.bd_alterar_habilidade(id_personagem, nome_antigo, nome_novo)

    def deletar_habilidade(self, id_personagem: int, nome_habilidade: str) -> None:
        self._crud_personagem.bd_deletar_habilidade(id_personagem, nome_habilidade)

    def listar_habilidades(self, id_personagem: int) -> list[str]:
        self._crud_personagem.bd_listar_habilidades_personagem(id_personagem)