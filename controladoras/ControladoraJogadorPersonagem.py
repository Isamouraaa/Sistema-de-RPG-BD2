import sqlite3
from cruds.CrudJogador import CrudJogador
from cruds.CrudPersonagem import CrudPersonagem
from entidades.Jogador import Jogador
from entidades.Personagem import Personagem


class ControladoraJogadorPersonagem:
    # aqui tem a conexao controladora -> crud

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao
        self._crud_jogador = CrudJogador(conexao)
        self._crud_personagem = CrudPersonagem(conexao)

    def criarJogador(self, jogador: Jogador) -> None:
        self._crud_jogador.bd_criar_jogador(jogador)

    def editarJogador(self, idJogador: int, jogador: Jogador) -> None:
        self._crud_jogador.bd_editar_jogador(idJogador, jogador)

    def excluirJogador(self, idJogador: int) -> None:
        self._crud_jogador.bd_excluir_jogador(idJogador)

    def listarJogadores(self) -> list[Jogador]:
        return self._crud_jogador.bd_listar_jogadores()

    def obterJogador(self, idJogador: int) -> Jogador | None:
        return self._crud_jogador.bd_listar_jogador(idJogador)

    def criarPersonagem(self, personagem: Personagem) -> None:
        self._crud_personagem.bd_criar_personagem(personagem)

    def editarPersonagem(self, idPersonagem: int, personagem: Personagem) -> None:
        self._crud_personagem.bd_editar_personagem(idPersonagem, personagem)

    def excluirPersonagem(self, idPersonagem: int) -> None:
        self._crud_personagem.bd_excluir_personagem(idPersonagem)

    def listarTodosPersonagens(self) -> list[Personagem]:
        return self._crud_personagem.bd_listar_personagens()

    def obterPersonagem(self, idPersonagem: int) -> Personagem | None:
        return self._crud_personagem.bd_listar_personagem(idPersonagem)

    def listarPersonagensPorJogador(self, idJogador: int) -> list[Personagem]:
        return self._crud_personagem.bd_listar_personagens_por_jogador(idJogador)

    def listarTodasHabilidades(self) -> list[tuple]:
        return self._crud_personagem.bd_listar_todas_habilidades()

    def obterHabilidade(self, id_habilidade: int) -> tuple | None:
        return self._crud_personagem.bd_obter_habilidade(id_habilidade)

    def listarHabilidadesDetalhadasPersonagem(self, id_personagem: int) -> list[tuple]:
        return self._crud_personagem.bd_listar_habilidades_detalhadas_personagem(id_personagem)

    def vincularHabilidadePorId(self, id_personagem: int, id_habilidade: int) -> None:
        self._crud_personagem.bd_vincular_habilidade_por_id(id_personagem, id_habilidade)

    def desvincularHabilidadePorId(self, id_personagem: int, id_habilidade: int) -> None:
        self._crud_personagem.bd_desvincular_habilidade_por_id(id_personagem, id_habilidade)

    def criarHabilidade(self, idPersonagem: int, nomeHab: str) -> None:
        self._crud_personagem.bd_vincular_habilidade(idPersonagem, nomeHab)

    def vincularHabilidade(self, idPersonagem: int, nomeHabilidade: str) -> None:
        self._crud_personagem.bd_vincular_habilidade(idPersonagem, nomeHabilidade)

    def alterarHabilidade(self, idPersonagem: int, nomeAntigo: str, nomeNovo: str) -> None:
        self._crud_personagem.bd_alterar_habilidade(idPersonagem, nomeAntigo, nomeNovo)

    def deletarHabilidade(self, idPersonagem: int, nomeHabilidade: str) -> None:
        self._crud_personagem.bd_deletar_habilidade(idPersonagem, nomeHabilidade)

    def listarHabilidades(self, idPersonagem: int) -> list[str]:
        return self._crud_personagem.bd_listar_habilidades_personagem(idPersonagem)

    def listarPersonagensPorHabilidade(self, nomeHabilidade: str) -> list[Personagem]:
        return self._crud_personagem.bd_listar_personagens_por_habilidade(nomeHabilidade)

    def listarPersonagensPorJogo(self, idJogo: int) -> list[Personagem]:
        return self._crud_personagem.bd_listar_personagens_por_jogo(idJogo)

    def estatisticasPersonagensHabilidades(self):
        return self._crud_personagem.bd_estatisticas_personagens_habilidades()

    def estatisticasHabilidadesClasses(self):
        return self._crud_personagem.bd_estatisticas_habilidades_classes()

    def serializarJogadores(self) -> str:
        return self._crud_jogador.serializar()

    def desserializarJogadores(self, dados: str) -> list[Jogador]:
        return self._crud_jogador.desserializar(dados)

    def serializarPersonagens(self) -> str:
        return self._crud_personagem.serializar()

    def desserializarPersonagens(self, dados: str) -> list[Personagem]:
        return self._crud_personagem.desserializar(dados)


Controladora = ControladoraJogadorPersonagem
ControladoraPersonagem = ControladoraJogadorPersonagem
JogadorPersonagemControladora = ControladoraJogadorPersonagem
