import os
import sqlite3
import sys
from controladoras.ControladoraJogadorPersonagem import ControladoraJogadorPersonagem
from controladoras.ControladoraMestreJogo import ControladoraMestreJogo
from entidades.combate import Combate
from entidades.jogador import Jogador
from entidades.jogo import Jogo
from entidades.mestre import Mestre
from entidades.personagem import Personagem


class Main:
    def __init__(self):
        self.nomeBanco = "bancorpg.sqlite"
        self.conexao = sqlite3.connect(self.nomeBanco)
        self.conexao.execute("PRAGMA foreign_keys = ON;")
        self.controladoraPersonagem = ControladoraJogadorPersonagem(self.conexao)
        self.controladoraJogo = ControladoraMestreJogo(self.conexao)
        self.mestreSessao = None

    def limparTela(self):
        os.system("cls" if os.name == "nt" else "clear")

    def lerEntrada(self, mensagem="Opção: "):
        valorDigitado = input(mensagem).strip()
        if valorDigitado.lower() == "q" or valorDigitado.lower() == "sair":
            print("Saindo do sistema...")
            sys.exit(0)
        return valorDigitado

    def menu(self):
        self.selecionarMestreSessao()
        while True:
            self.limparTela()
            nomeMestreAtivo = self.mestreSessao.getNome()

            print("========================================")
            print("            SISTEMA DE RPG")
            print(f" Mestre da Sessão: {nomeMestreAtivo}")
            print("========================================")
            print("[1] Combate")
            print("[2] Criação")
            print("[3] Edição")
            print("[4] Biblioteca")
            print("[5] Trocar Mestre da Sessão")
            print("[0] Sair")
            print("========================================")

            opcao = self.lerEntrada()
            if opcao == "1":
                self.menuCombate()
            elif opcao == "2":
                self.menuCriacao()
            elif opcao == "3":
                self.menuEdicao()
            elif opcao == "4":
                self.menuBiblioteca()
            elif opcao == "5":
                self.selecionarMestreSessao()
            elif opcao == "0":
                print("Encerrando o programa...")
                break

    def selecionarMestreSessao(self):
        while self.mestreSessao is None:
            self.limparTela()
            listaMestres = self.controladoraJogo.listarMestres()
            print("=== SELEÇÃO OBRIGATÓRIA DO MESTRE DA SESSÃO ===")
            if len(listaMestres) > 0:
                print("Mestres cadastrados:")
                for mestre in listaMestres:
                    print(f"[{mestre.getIdMestre()}] {mestre.getNome()}")
            else:
                print("Nenhum mestre cadastrado ainda.")
            print("[0] Cadastrar novo Mestre")

            idDigitado = self.lerEntrada("Digite o ID do mestre ou 0 para cadastrar: ")
            if idDigitado == "0":
                nomeMestre = self.lerEntrada("Nome do novo Mestre: ")
                if nomeMestre != "":
                    novoMestre = Mestre(nome=nomeMestre)
                    self.controladoraJogo.criarMestre(novoMestre)
                    self.mestreSessao = novoMestre
                    print(f"Mestre '{nomeMestre}' cadastrado e definido como mestre da sessão!")
                    self.lerEntrada("\nPressione Enter para continuar...")
                else:
                    print("O nome do mestre não pode ser vazio.")
                    self.lerEntrada("\nPressione Enter para tentar novamente...")
            elif idDigitado.isdigit():
                mestreEncontrado = self.controladoraJogo.visualizarMestre(int(idDigitado))
                if mestreEncontrado is not None:
                    self.mestreSessao = mestreEncontrado
                    print(f"Mestre '{mestreEncontrado.getNome()}' selecionado com sucesso!")
                    self.lerEntrada("\nPressione Enter para continuar...")
                else:
                    print("Mestre não encontrado.")
                    self.lerEntrada("\nPressione Enter para tentar novamente...")
            else:
                print("É obrigatório escolher ou cadastrar um mestre para iniciar.")
                self.lerEntrada("\nPressione Enter para tentar novamente...")

    def menuCombate(self):
        self.limparTela()
        print("=== COMBATE ===")
        listaJogos = self.controladoraJogo.listarJogos()
        if len(listaJogos) == 0:
            print("Nenhum jogo cadastrado.")
            self.lerEntrada("\nPressione Enter para voltar...")
            return

        for jogo in listaJogos:
            print(f"[{jogo.getIdJogo()}] {jogo.getNome()}")

        idJogoDigitado = self.lerEntrada("ID do jogo (ou 0 para voltar): ")
        if not idJogoDigitado.isdigit() or idJogoDigitado == "0":
            return

        listaDadosPersonagens = self.controladoraPersonagem.listarTodosPersonagens()
        listaPersonagensObjetos = []
        for dadoPersonagem in listaDadosPersonagens:
            idPersonagem = dadoPersonagem[0]
            personagemObjeto = self.controladoraPersonagem.obterPersonagem(idPersonagem)
            if personagemObjeto is not None:
                listaPersonagensObjetos.append(personagemObjeto)

        if len(listaPersonagensObjetos) == 0:
            print("Nenhum personagem cadastrado.")
            self.lerEntrada("\nPressione Enter para voltar...")
            return

        sessaoCombate = Combate(int(idJogoDigitado), listaPersonagensObjetos, self.controladoraPersonagem)
        sessaoCombate.iniciarCombate()

    def menuCriacao(self):
        while True:
            self.limparTela()
            print("=== MENU DE CRIAÇÃO ===")
            print("[1] Criar Jogo")
            print("[2] Criar Mestre")
            print("[3] Criar Jogador")
            print("[4] Criar Personagem")
            print("[0] Voltar")

            opcaoCriacao = self.lerEntrada()
            if opcaoCriacao == "1":
                nomeJogo = self.lerEntrada("Nome do Jogo: ")
                descricaoJogo = self.lerEntrada("Descrição do Jogo: ")
                idMestre = self.mestreSessao.getIdMestre()

                novoJogo = Jogo(nome=nomeJogo, descricao=descricaoJogo, idMestre=idMestre)
                self.controladoraJogo.criarJogo(novoJogo)
                print(f"Jogo criado com sucesso e associado ao mestre '{self.mestreSessao.getNome()}'!")
                self.lerEntrada("\nPressione Enter para continuar...")

            elif opcaoCriacao == "2":
                nomeMestre = self.lerEntrada("Nome do Mestre: ")
                if nomeMestre != "":
                    novoMestre = Mestre(nome=nomeMestre)
                    self.controladoraJogo.criarMestre(novoMestre)
                    print("Mestre criado com sucesso!")
                self.lerEntrada("\nPressione Enter para continuar...")

            elif opcaoCriacao == "3":
                nomeJogador = self.lerEntrada("Nome do Jogador: ")
                if nomeJogador != "":
                    novoJogador = Jogador(nomeJogador=nomeJogador)
                    self.controladoraPersonagem.criarJogador(novoJogador)
                    print("Jogador criado com sucesso!")
                self.lerEntrada("\nPressione Enter para continuar...")

            elif opcaoCriacao == "4":
                nomePersonagem = self.lerEntrada("Nome do Personagem: ")
                racaPersonagem = self.lerEntrada("Raça: ")
                classePersonagem = self.lerEntrada("Classe: ")
                descricaoPersonagem = self.lerEntrada("Descrição: ")
                tipoPersonagem = self.lerEntrada("Tipo (Herói, NPC, Criatura): ")
                if tipoPersonagem == "":
                    tipoPersonagem = "Herói"

                idJogadorTexto = self.lerEntrada("ID do Jogador dono (Enter para pular): ")
                idJogador = None
                if idJogadorTexto.isdigit():
                    idJogador = int(idJogadorTexto)

                idJogoTexto = self.lerEntrada("ID do Jogo (Enter para pular): ")
                idJogo = None
                if idJogoTexto.isdigit():
                    idJogo = int(idJogoTexto)

                nomeHabilidade = self.lerEntrada("Habilidade inicial (opcional): ")
                listaHabilidades = []
                if nomeHabilidade != "":
                    listaHabilidades.append(nomeHabilidade)

                novoPersonagem = Personagem(
                    nomePersonagem=nomePersonagem,
                    descricao=descricaoPersonagem,
                    tipo=tipoPersonagem,
                    raca=racaPersonagem,
                    classe=classePersonagem,
                    forca=10,
                    inteligencia=10,
                    vigor=10,
                    destreza=10,
                    sabedoria=10,
                    iniciativa=10,
                    habilidades=listaHabilidades,
                    idJogador=idJogador,
                    idJogo=idJogo
                )
                self.controladoraPersonagem.criarPersonagem(novoPersonagem)
                print("Personagem criado com sucesso!")
                self.lerEntrada("\nPressione Enter para continuar...")

            elif opcaoCriacao == "0":
                break

    def menuEdicao(self):
        while True:
            self.limparTela()
            print("=== MENU DE EDIÇÃO ===")
            print("[1] Editar Jogo")
            print("[2] Editar Jogador")
            print("[3] Editar Personagem")
            print("[4] Editar Mestre")
            print("[0] Voltar")

            opcaoEdicao = self.lerEntrada()
            if opcaoEdicao == "1":
                idJogoTexto = self.lerEntrada("ID do Jogo a editar: ")
                if idJogoTexto.isdigit():
                    jogoEncontrado = self.controladoraJogo.obterJogo(int(idJogoTexto))
                    if jogoEncontrado is not None:
                        novoNomeJogo = self.lerEntrada(f"Novo nome [{jogoEncontrado.getNome()}]: ")
                        if novoNomeJogo != "":
                            jogoEncontrado.setNome(novoNomeJogo)

                        novaDescricaoJogo = self.lerEntrada(f"Nova descrição [{jogoEncontrado.getDescricao()}]: ")
                        if novaDescricaoJogo != "":
                            jogoEncontrado.setDescricao(novaDescricaoJogo)

                        self.controladoraJogo.editarJogo(jogoEncontrado.getIdJogo(), jogoEncontrado)
                        print("Jogo editado com sucesso!")
                    else:
                        print("Jogo não encontrado.")
                self.lerEntrada("\nPressione Enter para continuar...")

            elif opcaoEdicao == "2":
                idJogadorTexto = self.lerEntrada("ID do Jogador a editar: ")
                if idJogadorTexto.isdigit():
                    jogadorEncontrado = self.controladoraPersonagem.obterJogador(int(idJogadorTexto))
                    if jogadorEncontrado is not None:
                        novoNomeJogador = self.lerEntrada(f"Novo nome [{jogadorEncontrado.getNome()}]: ")
                        if novoNomeJogador != "":
                            jogadorEncontrado.setNome(novoNomeJogador)

                        self.controladoraPersonagem.editarJogador(jogadorEncontrado.getId(), jogadorEncontrado)
                        print("Jogador editado com sucesso!")
                    else:
                        print("Jogador não encontrado.")
                self.lerEntrada("\nPressione Enter para continuar...")

            elif opcaoEdicao == "3":
                idPersonagemTexto = self.lerEntrada("ID do Personagem a editar: ")
                if idPersonagemTexto.isdigit():
                    personagemEncontrado = self.controladoraPersonagem.obterPersonagem(int(idPersonagemTexto))
                    if personagemEncontrado is not None:
                        novoNomePersonagem = self.lerEntrada(f"Novo nome [{personagemEncontrado.getNomePersonagem()}]: ")
                        if novoNomePersonagem != "":
                            personagemEncontrado.setNomePersonagem(novoNomePersonagem)

                        novaDescricaoPersonagem = self.lerEntrada(f"Nova descrição [{personagemEncontrado.getDescricao()}]: ")
                        if novaDescricaoPersonagem != "":
                            personagemEncontrado.setDescricao(novaDescricaoPersonagem)

                        novaClassePersonagem = self.lerEntrada(f"Nova classe [{personagemEncontrado.getClasse()}]: ")
                        if novaClassePersonagem != "":
                            personagemEncontrado.setClasse(novaClassePersonagem)

                        novaForcaTexto = self.lerEntrada(f"Nova força [{personagemEncontrado.getForca()}]: ")
                        if novaForcaTexto.isdigit():
                            personagemEncontrado.setForca(int(novaForcaTexto))

                        self.controladoraPersonagem.editarPersonagem(personagemEncontrado.getIdPersonagem(), personagemEncontrado)
                        print("Personagem editado com sucesso!")
                    else:
                        print("Personagem não encontrado.")
                self.lerEntrada("\nPressione Enter para continuar...")

            elif opcaoEdicao == "4":
                idMestreTexto = self.lerEntrada("ID do Mestre a editar: ")
                if idMestreTexto.isdigit():
                    mestreEncontrado = self.controladoraJogo.visualizarMestre(int(idMestreTexto))
                    if mestreEncontrado is not None:
                        novoNomeMestre = self.lerEntrada(f"Novo nome [{mestreEncontrado.getNome()}]: ")
                        if novoNomeMestre != "":
                            mestreEncontrado.setNome(novoNomeMestre)

                        self.controladoraJogo.editarMestre(mestreEncontrado.getIdMestre(), mestreEncontrado)
                        if self.mestreSessao.getIdMestre() == mestreEncontrado.getIdMestre():
                            self.mestreSessao = mestreEncontrado
                        print("Mestre editado com sucesso!")
                    else:
                        print("Mestre não encontrado.")
                self.lerEntrada("\nPressione Enter para continuar...")

            elif opcaoEdicao == "0":
                break

    def menuBiblioteca(self):
        while True:
            self.limparTela()
            print("=== BIBLIOTECA ===")
            print("[1] Listar Jogadores")
            print("[2] Listar Personagens")
            print("[3] Listar Jogos")
            print("[4] Estatísticas dos Jogos")
            print("[0] Voltar")

            opcaoBiblioteca = self.lerEntrada()
            if opcaoBiblioteca == "1":
                self.limparTela()
                listaJogadores = self.controladoraPersonagem.listarJogadores()
                print("--- LISTA DE JOGADORES ---")
                for jogador in listaJogadores:
                    print(f"ID: {jogador.getId()} | Nome: {jogador.getNome()}")
                self.lerEntrada("\nPressione Enter para continuar...")

            elif opcaoBiblioteca == "2":
                self.limparTela()
                listaDadosPersonagens = self.controladoraPersonagem.listarTodosPersonagens()
                print("--- LISTA DE PERSONAGENS ---")
                for dadoPersonagem in listaDadosPersonagens:
                    idPersonagem = dadoPersonagem[0]
                    personagem = self.controladoraPersonagem.obterPersonagem(idPersonagem)
                    if personagem is not None:
                        habilidadesTexto = ", ".join(personagem.getHabilidades())
                        if habilidadesTexto == "":
                            habilidadesTexto = "Nenhuma"
                        print(f"ID: {personagem.getIdPersonagem()} | Nome: {personagem.getNomePersonagem()} | Classe: {personagem.getClasse()} | Tipo: {personagem.getTipo()} | Força: {personagem.getForca()} | Habilidades: {habilidadesTexto}")
                self.lerEntrada("\nPressione Enter para continuar...")

            elif opcaoBiblioteca == "3":
                self.limparTela()
                listaJogos = self.controladoraJogo.listarJogos()
                print("--- LISTA DE JOGOS ---")
                for jogo in listaJogos:
                    print(f"ID: {jogo.getIdJogo()} | Nome: {jogo.getNome()} | Descrição: {jogo.getDescricao()}")
                self.lerEntrada("\nPressione Enter para continuar...")

            elif opcaoBiblioteca == "4":
                self.limparTela()
                listaEstatisticas = self.controladoraJogo.estatisticasJogos()
                print("--- ESTATÍSTICAS DOS JOGOS ---")
                for estatistica in listaEstatisticas:
                    nomeMestre = estatistica.getNomeMestre()
                    if nomeMestre is None:
                        nomeMestre = "Nenhum"
                    print(f"Jogo: {estatistica.getNome()} | Mestre: {nomeMestre} | Total Jogadores: {estatistica.getTotalJogadores()} | Total Personagens: {estatistica.getTotalPersonagens()} | Força Média: {estatistica.getForcaMedia()}")
                self.lerEntrada("\nPressione Enter para continuar...")

            elif opcaoBiblioteca == "0":
                break


if __name__ == "__main__":
    aplicacao = Main()
    aplicacao.menu()
