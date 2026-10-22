import os
import sqlite3
import sys
import time
from controladoras import ControladoraGeral, ControladoraJogadorPersonagem
from entidades import Combate, Jogador, Jogo, Mestre, Personagem


class Main:
    # aqui tem a conexao main -> banco
    # aqui tem a conexao main -> controladora
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def __init__(self):
        if not hasattr(self, "_iniciado"):
            self._iniciado = True
            self.objetoMain = self
            banco = "bancorpg.sqlite" if os.path.exists("bancorpg.sqlite") else "bancobanco.sqlite"
            self.conexao = sqlite3.connect(banco)
            self.conexao.execute("PRAGMA foreign_keys = ON;")
            self.controladoraGeral = ControladoraGeral(self.conexao)
            self.controladora = ControladoraJogadorPersonagem(self.conexao)
            self.mestreSessao = None

    def limparTela(self):
        time.sleep(0.4)
        os.system("cls" if os.name == "nt" else "clear")

    def pedirEntrada(self, prompt="Opção: "):
        valor = input(prompt).strip()
        if valor.lower() in ("q", "sair"):
            self.limparTela()
            print("Saindo do sistema...")
            sys.exit(0)
        return valor

    def pedirTipoPersonagem(self, atual=None):
        print("\n" + "-" * 50)
        print("  DEFINIÇÃO DO TIPO DE PERSONAGEM")
        print("  O tipo define a função do personagem no RPG:")
        print("  - Herói   : Personagem jogável / protagonista da aventura")
        print("  - NPC     : Personagem não-jogável (aliado, habitante, mentor)")
        print("  - Criatura: Monstro, fera ou antagonista de combate")
        print("-" * 50)
        print("  [1] Herói")
        print("  [2] NPC")
        print("  [3] Criatura")
        if atual:
            print(f"  [Enter] Manter atual ({atual})")
        print("-" * 50)
        opcao = self.pedirEntrada("Escolha a opção (1, 2, 3) ou digite o tipo: ")
        if not opcao and atual:
            return atual
        mapa = {"1": "Herói", "2": "NPC", "3": "Criatura"}
        return mapa.get(opcao, opcao if opcao else "Herói")

    def perguntarMestreInicio(self):
        self.limparTela()
        print("-" * 50)
        print("  BEM-VINDO AO SISTEMA DE RPG IVI")
        print("  SELEÇÃO DO MESTRE DA SESSÃO")
        print("-" * 50)
        mestres = self.controladoraGeral.ListarMestres()
        if mestres:
            print("  Quem é o mestre da sessão?")
            for m in mestres:
                print(f"  [{m.id_mestre}] {m.nome}")
            print("  [0] Nenhum destes")
            print("-" * 50)
            escolha = self.pedirEntrada("Opção: ")
            if escolha.isdigit() and int(escolha) != 0:
                mEncontrado = self.controladoraGeral.VisualizarMestre(int(escolha))
                if mEncontrado:
                    self.mestreSessao = mEncontrado
                    print(f"\nMestre selecionado: {mEncontrado.nome}")
                    self.pedirEntrada("\nPressione Enter para continuar...")
                    return
                else:
                    print("\nMestre não encontrado.")
                    self.pedirEntrada("\nPressione Enter para continuar...")
            self.submenuMestreNenhum()
        else:
            print("  Nenhum mestre cadastrado.")
            print("-" * 50)
            self.submenuMestreNenhum()

    def submenuMestreNenhum(self):
        while True:
            self.limparTela()
            print("-" * 50)
            print("  OPÇÕES DE MESTRE")
            print("-" * 50)
            print("  [1] Criar novo Mestre")
            print("  [2] Editar Mestre existente")
            print("  [0] Continuar sem Mestre")
            print("-" * 50)
            sub = self.pedirEntrada("Opção: ")
            if sub == "1":
                nome = self.pedirEntrada("Nome do novo Mestre: ")
                if nome:
                    novoMestre = Mestre(id_mestre=None, nome=nome)
                    self.controladoraGeral.CriarMestre(novoMestre)
                    self.mestreSessao = novoMestre
                    print(f"\nMestre '{nome}' criado e definido como mestre da sessão!")
                    self.pedirEntrada("\nPressione Enter para continuar...")
                    break
            elif sub == "2":
                mestres = self.controladoraGeral.ListarMestres()
                if not mestres:
                    print("\nNenhum mestre para editar.")
                    self.pedirEntrada("\nPressione Enter para continuar...")
                    continue
                print("-" * 50)
                for m in mestres:
                    print(f"  ID: {m.id_mestre:<4} | Nome: {m.nome}")
                print("-" * 50)
                idStr = self.pedirEntrada("ID do Mestre a editar: ")
                if idStr.isdigit():
                    self.editarMestreFluxo(int(idStr))
                    break
            elif sub == "0":
                break

    def menu(self):
        self.perguntarMestreInicio()
        while True:
            self.limparTela()
            nomeMestre = self.mestreSessao.nome if self.mestreSessao else "Nenhum"
            print("-" * 50)
            print("  SISTEMA DE RPG  (digite 'q' a qualquer momento para sair)")
            print(f"  Mestre da Sessão: {nomeMestre}")
            print("-" * 50)
            print("  [1] Combate")
            print("  [2] Criação")
            print("  [3] Edição")
            print("  [4] Biblioteca")
            print("  [5] Escolher Mestre da Sessão")
            print("  [0] Sair")
            print("-" * 50)

            opcao = self.pedirEntrada("\nOpção: ")

            if opcao == "1":
                self.menuCombate()
            elif opcao == "2":
                self.menuCriacao()
            elif opcao == "3":
                self.menuEdicao()
            elif opcao == "4":
                self.menuBiblioteca()
            elif opcao == "5":
                self.menuEscolherMestreSessao()
            elif opcao == "0":
                self.limparTela()
                print("Saindo do sistema...")
                break
            else:
                print("\nOpção inválida.")
                self.pedirEntrada("Pressione Enter para continuar...")

    def menuEscolherMestreSessao(self):
        self.limparTela()
        print("-" * 50)
        print("  ESCOLHA DO MESTRE DA SESSÃO")
        print("-" * 50)
        mestres = self.controladoraGeral.ListarMestres()
        if not mestres:
            print("  Nenhum mestre cadastrado.")
            print("-" * 50)
            self.submenuMestreNenhum()
            return

        for m in mestres:
            marcador = " (Ativo)" if self.mestreSessao and self.mestreSessao.id_mestre == m.id_mestre else ""
            print(f"  ID: {m.id_mestre:<4} | Nome: {m.nome}{marcador}")
        print("  [0] Nenhum destes (Criar novo ou Editar)")
        print("-" * 50)

        idEscolhido = self.pedirEntrada("\nDigite o ID do mestre para a sessão: ")
        if idEscolhido == "0":
            self.submenuMestreNenhum()
        elif idEscolhido.isdigit():
            mEncontrado = self.controladoraGeral.VisualizarMestre(int(idEscolhido))
            if mEncontrado:
                self.mestreSessao = mEncontrado
                print(f"\nMestre da sessão definido: {mEncontrado.nome}")
            else:
                print("\nMestre não encontrado.")
            self.pedirEntrada("\nPressione Enter para continuar...")

    def menuCombate(self):
        self.limparTela()
        print("-" * 50)
        print("  SELEÇÃO DE JOGO PARA COMBATE")
        if self.mestreSessao:
            print(f"  Filtrando por Mestre: {self.mestreSessao.nome}")
        print("-" * 50)

        if self.mestreSessao:
            jogos = [j for j in self.controladoraGeral.ListarJogos() if j.id_mestre == self.mestreSessao.id_mestre]
        else:
            jogos = self.controladoraGeral.ListarJogos()

        if not jogos:
            print("  Nenhum jogo cadastrado para este mestre.")
            print("-" * 50)
            self.pedirEntrada("\nPressione Enter para continuar...")
            return

        for j in jogos:
            print(f"  ID: {j.id_jogo:<4} | Nome: {j.nome}")
        print("-" * 50)

        idEscolhido = self.pedirEntrada("\nDigite o ID do jogo para combate (ou 0 para voltar): ")
        if idEscolhido == "0" or not idEscolhido.isdigit():
            return

        idJogo = int(idEscolhido)
        personagens = self.controladora.listarTodosPersonagens()
        if not personagens:
            print("\nNenhum personagem cadastrado para combate.")
            self.pedirEntrada("Pressione Enter para continuar...")
            return

        batalha = Combate(id_partida=idJogo, personagens=personagens, controladora_personagem=self.controladora)
        batalha.iniciarCombate()

    def menuCriacao(self):
        while True:
            self.limparTela()
            print("-" * 50)
            print("  MENU DE CRIAÇÃO")
            print("-" * 50)
            print("  [1] Criar Jogo")
            print("  [2] Criar Mestre")
            print("  [3] Criar Jogador")
            print("  [4] Criar Personagem")
            print("  [0] Voltar")
            print("-" * 50)

            subOpcao = self.pedirEntrada("\nOpção: ")

            if subOpcao == "1":
                nome = self.pedirEntrada("Nome do Jogo: ")
                descricao = self.pedirEntrada("Descrição do Jogo: ")
                if not self.mestreSessao:
                    self.menuEscolherMestreSessao()
                idMestre = self.mestreSessao.id_mestre if self.mestreSessao else None
                novoJogo = Jogo(id_jogo=None, nome=nome, descricao=descricao, id_mestre=idMestre)
                self.controladoraGeral.CriarJogo(novoJogo)
                nomeMestre = self.mestreSessao.nome if self.mestreSessao else "Sem mestre"
                print(f"Jogo '{nome}' criado e associado ao Mestre '{nomeMestre}'!")
                self.pedirEntrada("\nPressione Enter para continuar...")

            elif subOpcao == "2":
                nome = self.pedirEntrada("Nome do Mestre: ")
                novoMestre = Mestre(id_mestre=None, nome=nome)
                self.controladoraGeral.CriarMestre(novoMestre)
                if not self.mestreSessao:
                    self.mestreSessao = novoMestre
                print(f"Mestre '{nome}' criado com sucesso!")
                self.pedirEntrada("\nPressione Enter para continuar...")

            elif subOpcao == "3":
                nome = self.pedirEntrada("Nome do Jogador: ")
                novoJogador = Jogador(nomeJogador=nome)
                self.controladora.criarJogador(novoJogador)
                print(f"Jogador '{nome}' criado com sucesso!")
                self.pedirEntrada("\nPressione Enter para continuar...")

            elif subOpcao == "4":
                nome = self.pedirEntrada("Nome do Personagem: ")
                raca = self.pedirEntrada("Raça: ")
                classe = self.pedirEntrada("Classe: ")
                descricao = self.pedirEntrada("Descrição: ")
                tipo = self.pedirTipoPersonagem()
                idJogadorStr = self.pedirEntrada("ID do Jogador (dono, Enter para pular): ")
                idJogador = int(idJogadorStr) if idJogadorStr.isdigit() else None

                habsDisponiveis = self.controladora.listarTodasHabilidades()
                habilidadesEscolhidas = []
                if habsDisponiveis:
                    print("-" * 50)
                    print("  HABILIDADES DISPONÍVEIS NO BANCO")
                    print("-" * 50)
                    for h in habsDisponiveis:
                        pts = f"| Pontos: {h[3]}" if h[3] is not None else ""
                        print(f"  ID: {h[0]:<3} | {h[1]:<20} {pts}")
                    print("-" * 50)
                    idsStr = self.pedirEntrada("Digite os IDs das habilidades (separados por vírgula, ou Enter para pular): ")
                    for pedaco in idsStr.split(","):
                        pedaco = pedaco.strip()
                        if pedaco.isdigit():
                            habObj = self.controladora.obterHabilidade(int(pedaco))
                            if habObj:
                                habilidadesEscolhidas.append(habObj[1])

                p = Personagem(
                    idPersonagem=None,
                    nomePersonagem=nome,
                    descricao=descricao,
                    tipo=tipo,
                    raca=raca,
                    classe=classe,
                    forca=10,
                    inteligencia=10,
                    vigor=10,
                    destreza=10,
                    sabedoria=10,
                    iniciativa=10,
                    habilidades=habilidadesEscolhidas,
                    idJogador=idJogador,
                )
                self.controladora.criarPersonagem(p)
                print(f"Personagem '{nome}' criado com sucesso!")
                self.pedirEntrada("\nPressione Enter para continuar...")

            elif subOpcao == "0":
                break

    def editarMestreFluxo(self, idM):
        while True:
            self.limparTela()
            mestre = self.controladoraGeral.VisualizarMestre(idM)
            if not mestre:
                print("\nMestre não encontrado.")
                self.pedirEntrada("Pressione Enter para continuar...")
                break

            jogos = [j.nome for j in self.controladoraGeral.ListarJogos() if j.id_mestre == mestre.id_mestre]
            nomesJogos = ", ".join(jogos) if jogos else "Nenhum"

            print("-" * 50)
            print("  CARACTERÍSTICAS DO MESTRE")
            print("-" * 50)
            print(f"  ID   : {mestre.id_mestre}")
            print(f"  Nome : {mestre.nome}")
            print(f"  Jogos: {nomesJogos}")
            print("-" * 50)
            print("  O que deseja editar?")
            print("  [1] Nome")
            print("  [0] Concluir edição deste mestre")
            print("-" * 50)

            campo = self.pedirEntrada("Opção: ")
            if campo == "1":
                novo = self.pedirEntrada(f"Novo nome [{mestre.nome}]: ")
                if novo:
                    mestre.nome = novo
                    self.controladoraGeral.EditarMestre(idM, mestre)
                    if self.mestreSessao and self.mestreSessao.id_mestre == idM:
                        self.mestreSessao = mestre
                    print("\nNome do mestre atualizado com sucesso!")
                    self.pedirEntrada("Pressione Enter para continuar...")
            elif campo == "0":
                break

    def editarJogadorFluxo(self, idJog):
        while True:
            self.limparTela()
            jogador = self.controladora.obterJogador(idJog)
            if not jogador:
                print("\nJogador não encontrado.")
                self.pedirEntrada("Pressione Enter para continuar...")
                break

            pers = self.controladora.listarPersonagensPorJogador(jogador.getId())
            nomesPers = ", ".join([p.getNomePersonagem() for p in pers]) if pers else "Nenhum"

            print("-" * 50)
            print("  CARACTERÍSTICAS DO JOGADOR")
            print("-" * 50)
            print(f"  ID         : {jogador.getId()}")
            print(f"  Nome       : {jogador.getNome()}")
            print(f"  Personagens: {nomesPers}")
            print("-" * 50)
            print("  O que deseja editar?")
            print("  [1] Nome")
            print("  [0] Concluir edição deste jogador")
            print("-" * 50)

            campo = self.pedirEntrada("Opção: ")
            if campo == "1":
                novo = self.pedirEntrada(f"Novo nome [{jogador.getNome()}]: ")
                if novo:
                    jogador.setNome(novo)
                    self.controladora.editarJogador(idJog, jogador)
                    print("\nNome do jogador atualizado com sucesso!")
                    self.pedirEntrada("Pressione Enter para continuar...")
            elif campo == "0":
                break

    def editarPersonagemFluxo(self, idP):
        while True:
            self.limparTela()
            personagem = self.controladora.obterPersonagem(idP)
            if not personagem:
                print("\nPersonagem não encontrado.")
                self.pedirEntrada("Pressione Enter para continuar...")
                break

            dono = self.controladora.obterJogador(personagem.getIdJogador()) if personagem.getIdJogador() else None
            nomeDono = f"{dono.getNome()} (ID: {dono.getId()})" if dono else "Nenhum"
            habs = personagem.getHabilidades()
            habsStr = ", ".join(habs) if habs else "Nenhuma"

            print("-" * 50)
            print("  CARACTERÍSTICAS DO PERSONAGEM")
            print("-" * 50)
            print(f"  ID           : {personagem.getIdPersonagem()}")
            print(f"  Nome         : {personagem.getNomePersonagem()}")
            print(f"  Descrição    : {personagem.getDescricao() or '-'}")
            print(f"  Tipo         : {personagem.getTipo() or '-'}")
            print(f"  Raça         : {personagem.getRaca() or '-'}")
            print(f"  Classe       : {personagem.getClasse() or '-'}")
            print(f"  Força        : {personagem.getForca()}")
            print(f"  Inteligência : {personagem.getInteligencia()}")
            print(f"  Vigor        : {personagem.getVigor()}")
            print(f"  Destreza     : {personagem.getDestreza()}")
            print(f"  Sabedoria    : {personagem.getSabedoria()}")
            print(f"  Iniciativa   : {personagem.getIniciativa()}")
            print(f"  Jogador Dono : {nomeDono}")
            print(f"  Habilidades  : {habsStr}")
            print("-" * 50)
            print("  O que deseja editar?")
            print("  [1] Nome")
            print("  [2] Descrição")
            print("  [3] Tipo")
            print("  [4] Raça")
            print("  [5] Classe")
            print("  [6] Atributos (Força, INT, VIG, DES, SAB, Inic)")
            print("  [7] Habilidades (Adicionar / Remover)")
            print("  [8] Jogador Dono")
            print("  [0] Concluir edição deste personagem")
            print("-" * 50)

            campo = self.pedirEntrada("Opção: ")
            if campo == "1":
                novo = self.pedirEntrada(f"Novo nome [{personagem.getNomePersonagem()}]: ")
                if novo:
                    personagem.setNomePersonagem(novo)
                    self.controladora.editarPersonagem(idP, personagem)
                    print("\nNome atualizado com sucesso!")
                    self.pedirEntrada("Pressione Enter para continuar...")
            elif campo == "2":
                novo = self.pedirEntrada(f"Nova descrição [{personagem.getDescricao()}]: ")
                if novo:
                    personagem.setDescricao(novo)
                    self.controladora.editarPersonagem(idP, personagem)
                    print("\nDescrição atualizada com sucesso!")
                    self.pedirEntrada("Pressione Enter para continuar...")
            elif campo == "3":
                novoTipo = self.pedirTipoPersonagem(atual=personagem.getTipo())
                if novoTipo:
                    personagem.setTipo(novoTipo)
                    self.controladora.editarPersonagem(idP, personagem)
                    print("\nTipo atualizado com sucesso!")
                    self.pedirEntrada("Pressione Enter para continuar...")
            elif campo == "4":
                novo = self.pedirEntrada(f"Nova raça [{personagem.getRaca()}]: ")
                if novo:
                    personagem.setRaca(novo)
                    self.controladora.editarPersonagem(idP, personagem)
                    print("\nRaça atualizada com sucesso!")
                    self.pedirEntrada("Pressione Enter para continuar...")
            elif campo == "5":
                novo = self.pedirEntrada(f"Nova classe [{personagem.getClasse()}]: ")
                if novo:
                    personagem.setClasse(novo)
                    self.controladora.editarPersonagem(idP, personagem)
                    print("\nClasse atualizada com sucesso!")
                    self.pedirEntrada("Pressione Enter para continuar...")
            elif campo == "6":
                print("\nDigite os novos valores dos atributos (ou Enter para manter):")
                f = self.pedirEntrada(f"Força [{personagem.getForca()}]: ")
                i = self.pedirEntrada(f"Inteligência [{personagem.getInteligencia()}]: ")
                v = self.pedirEntrada(f"Vigor [{personagem.getVigor()}]: ")
                d = self.pedirEntrada(f"Destreza [{personagem.getDestreza()}]: ")
                s = self.pedirEntrada(f"Sabedoria [{personagem.getSabedoria()}]: ")
                inic = self.pedirEntrada(f"Iniciativa [{personagem.getIniciativa()}]: ")
                if f.isdigit():
                    personagem.setForca(int(f))
                if i.isdigit():
                    personagem.setInteligencia(int(i))
                if v.isdigit():
                    personagem.setVigor(int(v))
                if d.isdigit():
                    personagem.setDestreza(int(d))
                if s.isdigit():
                    personagem.setSabedoria(int(s))
                if inic.isdigit():
                    personagem.setIniciativa(int(inic))
                self.controladora.editarPersonagem(idP, personagem)
                print("\nAtributos atualizados com sucesso!")
                self.pedirEntrada("Pressione Enter para continuar...")
            elif campo == "7":
                habsDoPersonagem = self.controladora.listarHabilidadesDetalhadasPersonagem(idP)
                print("\n" + "-" * 50)
                print("  HABILIDADES DO PERSONAGEM")
                print("-" * 50)
                if not habsDoPersonagem:
                    print("  Nenhuma habilidade vinculada a este personagem.")
                else:
                    for h in habsDoPersonagem:
                        pts = f"| Pontos: {h[3]}" if h[3] is not None else ""
                        print(f"  ID: {h[0]:<3} | {h[1]:<20} {pts}")
                print("-" * 50)
                print("  [1] Adicionar habilidade existente por ID")
                print("  [2] Remover habilidade vinculada por ID")
                print("  [0] Voltar")
                print("-" * 50)
                opH = self.pedirEntrada("Opção: ")
                if opH == "1":
                    todasHabs = self.controladora.listarTodasHabilidades()
                    idsJaVinculados = {h[0] for h in habsDoPersonagem}
                    habsParaAdicionar = [h for h in todasHabs if h[0] not in idsJaVinculados]
                    if not habsParaAdicionar:
                        print("\nTodas as habilidades do banco já estão vinculadas a este personagem.")
                        self.pedirEntrada("Pressione Enter para continuar...")
                    else:
                        print("-" * 50)
                        print("  HABILIDADES DISPONÍVEIS NO BANCO DE DADOS")
                        print("-" * 50)
                        for h in habsParaAdicionar:
                            pts = f"| Pontos: {h[3]}" if h[3] is not None else ""
                            print(f"  ID: {h[0]:<3} | {h[1]:<20} {pts}")
                        print("-" * 50)
                        idEscolhida = self.pedirEntrada("Digite o ID da habilidade para adicionar (ou 0 para cancelar): ")
                        if idEscolhida.isdigit() and int(idEscolhida) != 0:
                            idHabInt = int(idEscolhida)
                            habEncontrada = self.controladora.obterHabilidade(idHabInt)
                            if habEncontrada:
                                self.controladora.vincularHabilidadePorId(idP, idHabInt)
                                print(f"\nHabilidade '{habEncontrada[1]}' vinculada com sucesso!")
                            else:
                                print("\nHabilidade não encontrada.")
                            self.pedirEntrada("Pressione Enter para continuar...")
                elif opH == "2":
                    if not habsDoPersonagem:
                        print("\nNenhuma habilidade para remover.")
                        self.pedirEntrada("Pressione Enter para continuar...")
                    else:
                        idRemover = self.pedirEntrada("Digite o ID da habilidade para remover (ou 0 para cancelar): ")
                        if idRemover.isdigit() and int(idRemover) != 0:
                            idHabRemover = int(idRemover)
                            self.controladora.desvincularHabilidadePorId(idP, idHabRemover)
                            print("\nHabilidade removida com sucesso!")
                            self.pedirEntrada("Pressione Enter para continuar...")
            elif campo == "8":
                novoDono = self.pedirEntrada(f"Novo ID do Jogador dono [{personagem.getIdJogador()}]: ")
                if novoDono.isdigit():
                    personagem.setIdJogador(int(novoDono))
                    self.controladora.editarPersonagem(idP, personagem)
                    print("\nJogador dono atualizado com sucesso!")
                    self.pedirEntrada("Pressione Enter para continuar...")
            elif campo == "0":
                break

    def editarJogoFluxo(self, idJogo):
        while True:
            self.limparTela()
            jogo = self.controladoraGeral.ObterJogo(idJogo)
            if not jogo:
                print("\nJogo não encontrado.")
                self.pedirEntrada("Pressione Enter para continuar...")
                break

            mestre = self.controladoraGeral.VisualizarMestre(jogo.id_mestre) if jogo.id_mestre else None
            nomeMestre = f"{mestre.nome} (ID: {mestre.id_mestre})" if mestre else "Nenhum"

            print("-" * 50)
            print("  CARACTERÍSTICAS DO JOGO")
            print("-" * 50)
            print(f"  ID        : {jogo.id_jogo}")
            print(f"  Nome      : {jogo.nome}")
            print(f"  Descrição : {jogo.descricao or '-'}")
            print(f"  Mestre    : {nomeMestre}")
            print("-" * 50)
            print("  O que deseja editar?")
            print("  [1] Nome")
            print("  [2] Descrição")
            print("  [3] Mestre do Jogo")
            print("  [0] Concluir edição deste jogo")
            print("-" * 50)

            campo = self.pedirEntrada("Opção: ")
            if campo == "1":
                novo = self.pedirEntrada(f"Novo nome [{jogo.nome}]: ")
                if novo:
                    jogo.nome = novo
                    self.controladoraGeral.EditarJogo(idJogo, jogo)
                    print("\nNome do jogo atualizado com sucesso!")
                    self.pedirEntrada("Pressione Enter para continuar...")
            elif campo == "2":
                novaDesc = self.pedirEntrada(f"Nova descrição [{jogo.descricao}]: ")
                if novaDesc:
                    jogo.descricao = novaDesc
                    self.controladoraGeral.EditarJogo(idJogo, jogo)
                    print("\nDescrição do jogo atualizada com sucesso!")
                    self.pedirEntrada("Pressione Enter para continuar...")
            elif campo == "3":
                novoMestreId = self.pedirEntrada(f"Novo ID do Mestre [{jogo.id_mestre}]: ")
                if novoMestreId.isdigit():
                    jogo.id_mestre = int(novoMestreId)
                    self.controladoraGeral.EditarJogo(idJogo, jogo)
                    print("\nMestre do jogo atualizado com sucesso!")
                    self.pedirEntrada("Pressione Enter para continuar...")
            elif campo == "0":
                break

    def menuEdicao(self):
        while True:
            self.limparTela()
            print("-" * 50)
            print("  MENU DE EDIÇÃO")
            print("-" * 50)
            print("  [1] Editar Jogo")
            print("  [2] Editar Jogador")
            print("  [3] Editar Personagem")
            print("  [4] Editar Mestre")
            print("  [0] Voltar")
            print("-" * 50)

            subOpcao = self.pedirEntrada("\nOpção: ")

            if subOpcao == "1":
                jogos = self.controladoraGeral.ListarJogos()
                if not jogos:
                    print("\nNenhum jogo cadastrado.")
                    self.pedirEntrada("Pressione Enter para continuar...")
                else:
                    print("-" * 50)
                    for j in jogos:
                        print(f"  ID: {j.id_jogo:<4} | Nome: {j.nome}")
                    print("-" * 50)
                    idStr = self.pedirEntrada("ID do Jogo a editar (ou 0 para voltar): ")
                    if idStr.isdigit() and int(idStr) != 0:
                        self.editarJogoFluxo(int(idStr))

            elif subOpcao == "2":
                jogadores = self.controladora.listarJogadores()
                if not jogadores:
                    print("\nNenhum jogador cadastrado.")
                    self.pedirEntrada("Pressione Enter para continuar...")
                else:
                    print("-" * 50)
                    for jog in jogadores:
                        print(f"  ID: {jog.getId():<4} | Nome: {jog.getNome()}")
                    print("-" * 50)
                    idStr = self.pedirEntrada("ID do Jogador a editar (ou 0 para voltar): ")
                    if idStr.isdigit() and int(idStr) != 0:
                        self.editarJogadorFluxo(int(idStr))

            elif subOpcao == "3":
                personagens = self.controladora.listarTodosPersonagens()
                if not personagens:
                    print("\nNenhum personagem cadastrado.")
                    self.pedirEntrada("Pressione Enter para continuar...")
                else:
                    print("-" * 50)
                    for p in personagens:
                        print(f"  ID: {p.getIdPersonagem():<4} | Nome: {p.getNomePersonagem():<15} | Classe: {p.getClasse()}")
                    print("-" * 50)
                    idStr = self.pedirEntrada("ID do Personagem a editar (ou 0 para voltar): ")
                    if idStr.isdigit() and int(idStr) != 0:
                        self.editarPersonagemFluxo(int(idStr))

            elif subOpcao == "4":
                mestres = self.controladoraGeral.ListarMestres()
                if not mestres:
                    print("\nNenhum mestre cadastrado.")
                    self.pedirEntrada("Pressione Enter para continuar...")
                else:
                    print("-" * 50)
                    for m in mestres:
                        print(f"  ID: {m.id_mestre:<4} | Nome: {m.nome}")
                    print("-" * 50)
                    idStr = self.pedirEntrada("ID do Mestre a editar (ou 0 para voltar): ")
                    if idStr.isdigit() and int(idStr) != 0:
                        self.editarMestreFluxo(int(idStr))

            elif subOpcao == "0":
                break

    def exibirPersonagensBiblioteca(self, tipo=None, titulo="PERSONAGENS"):
        self.limparTela()
        if tipo:
            personagens = self.controladora.listarPersonagensPorTipo(tipo)
        else:
            personagens = self.controladora.listarTodosPersonagens()
        print("-" * 50)
        print(f"  {titulo}")
        print("-" * 50)
        if not personagens:
            print("  Nenhum personagem encontrado nesta categoria.")
            print("-" * 50)
            self.pedirEntrada("\nPressione Enter para continuar...")
            return
        for p in personagens:
            tipo_label = f"[{p.getTipo()}]" if p.getTipo() else ""
            print(f"  ID: {p.getIdPersonagem():<4} | Nome: {p.getNomePersonagem():<15} | Classe: {p.getClasse():<10} {tipo_label}")
        print("-" * 50)
        idEscolhido = self.pedirEntrada("\nDigite o ID do personagem para ver detalhes (Enter para voltar): ")
        if idEscolhido.isdigit():
            pEncontrado = self.controladora.obterPersonagem(int(idEscolhido))
            if pEncontrado:
                self.limparTela()
                print("-" * 50)
                print("  DETALHES DO PERSONAGEM")
                print("-" * 50)
                print(f"  ID: {pEncontrado.getIdPersonagem()}")
                print(f"  Nome: {pEncontrado.getNomePersonagem()}")
                print(f"  Descrição: {pEncontrado.getDescricao() or '-'}")
                print(f"  Tipo: {pEncontrado.getTipo() or '-'}")
                print(f"  Raça: {pEncontrado.getRaca() or '-'}")
                print(f"  Classe: {pEncontrado.getClasse() or '-'}")
                print(f"  Atributos: FOR {pEncontrado.getForca()} | INT {pEncontrado.getInteligencia()} | VIG {pEncontrado.getVigor()} | DES {pEncontrado.getDestreza()} | SAB {pEncontrado.getSabedoria()}")
                print(f"  Iniciativa: {pEncontrado.getIniciativa()}")
                print(f"  ID Jogador Dono: {pEncontrado.getIdJogador() or '-'}")
                habs = pEncontrado.getHabilidades()
                print(f"  Habilidades: {', '.join(habs) if habs else 'Nenhuma'}")
                print("-" * 50)
            else:
                print("\nPersonagem não encontrado.")
            self.pedirEntrada("\nPressione Enter para continuar...")

    def submenuBibliotecaPersonagens(self):
        while True:
            self.limparTela()
            print("-" * 50)
            print("  BIBLIOTECA - PERSONAGENS POR TIPO")
            print("-" * 50)
            print("  [1] Personagens (Heróis)")
            print("  [2] NPCs")
            print("  [3] Criaturas")
            print("  [4] Todos os Personagens")
            print("  [0] Voltar")
            print("-" * 50)
            op = self.pedirEntrada("Escolha uma opção: ")
            if op == "1":
                self.exibirPersonagensBiblioteca("Herói", "PERSONAGENS (HERÓIS)")
            elif op == "2":
                self.exibirPersonagensBiblioteca("NPC", "NPCS")
            elif op == "3":
                self.exibirPersonagensBiblioteca("Criatura", "CRIATURAS")
            elif op == "4":
                self.exibirPersonagensBiblioteca(None, "TODOS OS PERSONAGENS")
            elif op == "0":
                break
            else:
                print("Opção inválida!")
                self.pedirEntrada("\nPressione Enter para continuar...")

    def menuBiblioteca(self):
        while True:
            self.limparTela()
            nomeMestre = self.mestreSessao.nome if self.mestreSessao else "Nenhum"
            print("-" * 50)
            print("  BIBLIOTECA")
            print(f"  Mestre da Sessão: {nomeMestre}")
            print("-" * 50)
            print("  [1] Jogadores")
            print("  [2] Personagens")
            print("  [3] Habilidades")
            print("  [4] Jogos")
            print("  [5] Mestre da Sessão e Jogos Associados")
            print("  [6] Estatísticas dos Jogos")
            print("  [7] Estatísticas de Personagens e Habilidades")
            print("  [8] Estatísticas de Habilidades por Classe")
            print("  [9] Comparativo por Tipo de Personagem (Herói, NPC, Criatura)")
            print("  [10] Consulta por Tipo e Característica (com especificação)")
            print("  [11] Censo de Tipos de Personagem por Jogo")
            print("  [0] Voltar")
            print("-" * 50)

            subOpcao = self.pedirEntrada("\nOpção: ")

            if subOpcao == "1":
                self.limparTela()
                jogadores = self.controladora.listarJogadores()
                print("-" * 50)
                print("  JOGADORES")
                print("-" * 50)
                if not jogadores:
                    print("  Nenhum jogador encontrado.")
                    print("-" * 50)
                    self.pedirEntrada("\nPressione Enter para continuar...")
                else:
                    for jog in jogadores:
                        print(f"  ID: {jog.getId():<4} | Nome: {jog.getNome()}")
                    print("-" * 50)
                    idEscolhido = self.pedirEntrada("\nDigite o ID do jogador para ver detalhes (Enter para voltar): ")
                    if idEscolhido.isdigit():
                        jogEncontrado = self.controladora.obterJogador(int(idEscolhido))
                        if jogEncontrado:
                            self.limparTela()
                            print("-" * 50)
                            print("  DETALHES DO JOGADOR")
                            print("-" * 50)
                            print(f"  ID: {jogEncontrado.getId()}")
                            print(f"  Nome: {jogEncontrado.getNome()}")
                            pers = self.controladora.listarPersonagensPorJogador(jogEncontrado.getId())
                            nomesPers = ", ".join([p.getNomePersonagem() for p in pers]) if pers else "Nenhum"
                            print(f"  Personagens: {nomesPers}")
                            print("-" * 50)
                        else:
                            print("\nJogador não encontrado.")
                        self.pedirEntrada("\nPressione Enter para continuar...")

            elif subOpcao == "2":
                self.submenuBibliotecaPersonagens()

            elif subOpcao == "3":
                self.limparTela()
                cursor = self.conexao.cursor()
                cursor.execute("SELECT IDhabilidade, nomeHabilidade, efeitoHabilidade, Pontos FROM HABILIDADE")
                habilidades = cursor.fetchall()
                print("-" * 50)
                print("  HABILIDADES")
                print("-" * 50)
                if not habilidades:
                    print("  Nenhuma habilidade encontrada.")
                    print("-" * 50)
                    self.pedirEntrada("\nPressione Enter para continuar...")
                else:
                    for h in habilidades:
                        print(f"  ID: {h[0]:<4} | Nome: {h[1]:<15} | Pontos: {h[3]}")
                    print("-" * 50)
                    idEscolhido = self.pedirEntrada("\nDigite o ID da habilidade para ver detalhes (Enter para voltar): ")
                    if idEscolhido.isdigit():
                        cursor.execute("SELECT IDhabilidade, nomeHabilidade, efeitoHabilidade, Pontos FROM HABILIDADE WHERE IDhabilidade = ?", (int(idEscolhido),))
                        hEncontrada = cursor.fetchone()
                        if hEncontrada:
                            self.limparTela()
                            print("-" * 50)
                            print("  DETALHES DA HABILIDADE")
                            print("-" * 50)
                            print(f"  ID: {hEncontrada[0]}")
                            print(f"  Nome: {hEncontrada[1]}")
                            print(f"  Pontos: {hEncontrada[3]}")
                            print(f"  Efeito: {hEncontrada[2] or '-'}")
                            persComHab = self.controladora.listarPersonagensPorHabilidade(hEncontrada[1])
                            nomesPers = ", ".join([x.getNomePersonagem() for x in persComHab]) if persComHab else "Nenhum"
                            print(f"  Personagens com esta habilidade: {nomesPers}")
                            print("-" * 50)
                        else:
                            print("\nHabilidade não encontrada.")
                        self.pedirEntrada("\nPressione Enter para continuar...")

            elif subOpcao == "4":
                self.limparTela()
                jogos = self.controladoraGeral.ListarJogos()
                print("-" * 50)
                print("  JOGOS")
                print("-" * 50)
                if not jogos:
                    print("  Nenhum jogo encontrado.")
                    print("-" * 50)
                    self.pedirEntrada("\nPressione Enter para continuar...")
                else:
                    for j in jogos:
                        print(f"  ID: {j.id_jogo:<4} | Nome: {j.nome}")
                    print("-" * 50)
                    idEscolhido = self.pedirEntrada("\nDigite o ID do jogo para ver detalhes (Enter para voltar): ")
                    if idEscolhido.isdigit():
                        jEncontrado = self.controladoraGeral.ObterJogo(int(idEscolhido))
                        if jEncontrado:
                            mestreObj = self.controladoraGeral.VisualizarMestre(jEncontrado.id_mestre) if jEncontrado.id_mestre else None
                            self.limparTela()
                            print("-" * 50)
                            print("  DETALHES DO JOGO")
                            print("-" * 50)
                            print(f"  ID: {jEncontrado.id_jogo}")
                            print(f"  Nome: {jEncontrado.nome}")
                            print(f"  Descrição: {jEncontrado.descricao or '-'}")
                            print(f"  Mestre: {mestreObj.nome if mestreObj else 'Nenhum'}")
                            persJogo = self.controladora.listarPersonagensPorJogo(jEncontrado.id_jogo)
                            nomesPers = ", ".join([x.getNomePersonagem() for x in persJogo]) if persJogo else "Nenhum"
                            print(f"  Personagens participantes: {nomesPers}")
                            print("-" * 50)
                        else:
                            print("\nJogo não encontrado.")
                        self.pedirEntrada("\nPressione Enter para continuar...")

            elif subOpcao == "5":
                self.limparTela()
                print("-" * 50)
                print("  MESTRE DA SESSÃO E SEUS JOGOS")
                print("-" * 50)
                if not self.mestreSessao:
                    print("  Nenhum mestre ativo na sessão.")
                    print("-" * 50)
                    self.pedirEntrada("\nPressione Enter para continuar...")
                else:
                    print(f"  ID: {self.mestreSessao.id_mestre} | Nome: {self.mestreSessao.nome}")
                    print("-" * 50)
                    jogosMestre = [j for j in self.controladoraGeral.ListarJogos() if j.id_mestre == self.mestreSessao.id_mestre]
                    if not jogosMestre:
                        print("  Nenhum jogo associado a este mestre.")
                    else:
                        print("  JOGOS ASSOCIADOS:")
                        for j in jogosMestre:
                            print(f"  ID: {j.id_jogo:<4} | Nome: {j.nome} | Descrição: {j.descricao or '-'}")
                    print("-" * 50)
                    idEscolhido = self.pedirEntrada("\nDigite o ID do jogo para ver detalhes (Enter para voltar): ")
                    if idEscolhido.isdigit():
                        jEncontrado = self.controladoraGeral.ObterJogo(int(idEscolhido))
                        if jEncontrado and jEncontrado.id_mestre == self.mestreSessao.id_mestre:
                            self.limparTela()
                            print("-" * 50)
                            print("  DETALHES DO JOGO DO MESTRE")
                            print("-" * 50)
                            print(f"  ID: {jEncontrado.id_jogo}")
                            print(f"  Nome: {jEncontrado.nome}")
                            print(f"  Descrição: {jEncontrado.descricao or '-'}")
                            print(f"  Mestre: {self.mestreSessao.nome}")
                            persJogo = self.controladora.listarPersonagensPorJogo(jEncontrado.id_jogo)
                            nomesPers = ", ".join([x.getNomePersonagem() for x in persJogo]) if persJogo else "Nenhum"
                            print(f"  Personagens participantes: {nomesPers}")
                            print("-" * 50)
                        else:
                            print("\nJogo não encontrado ou não pertence a este mestre.")
                        self.pedirEntrada("\nPressione Enter para continuar...")

            elif subOpcao == "6":
                self.limparTela()
                stats = self.controladoraGeral.EstatisticasJogos()
                print("-" * 70)
                print("  ESTATÍSTICAS DOS JOGOS")
                print("-" * 70)
                if not stats:
                    print("  Nenhum jogo encontrado.")
                for s in stats:
                    print(f"  [{s['id_jogo']}] {s['nome_jogo']}")
                    print(f"      Mestre          : {s['nome_mestre'] or 'Sem mestre'}")
                    print(f"      Jogadores       : {s['total_jogadores']}")
                    print(f"      Personagens     : {s['total_personagens']}")
                    print(f"      Classe + comum  : {s['classe_mais_comum'] or '-'}")
                    print(f"      Força média     : {s['forca_media']}")
                    print("-" * 70)
                self.pedirEntrada("\nPressione Enter para continuar...")

            elif subOpcao == "7":
                self.limparTela()
                stats = self.controladora.estatisticasPersonagensHabilidades()
                print("-" * 75)
                print("  ESTATÍSTICAS DE PERSONAGENS E HABILIDADES (PODER TOTAL)")
                print("-" * 75)
                if not stats:
                    print("  Nenhum personagem encontrado.")
                for s in stats:
                    print(f"  [{s['id_personagem']}] {s['nome_personagem']} ({s['classe']}) | Jogador: {s['nome_jogador']}")
                    print(f"      Habilidades     : {s['lista_habilidades']}")
                    print(f"      Qtd Habilidades : {s['total_habilidades']} | Soma Pontos: {s['soma_pontos_habilidades']} | Média: {s['media_pontos_habilidade']}")
                    print(f"      Poder Total     : {s['poder_total']}")
                    print("-" * 75)
                self.pedirEntrada("\nPressione Enter para continuar...")

            elif subOpcao == "8":
                self.limparTela()
                stats = self.controladora.estatisticasHabilidadesClasses()
                print("-" * 75)
                print("  ESTATÍSTICAS DE HABILIDADES POR CLASSE")
                print("-" * 75)
                if not stats:
                    print("  Nenhuma habilidade encontrada.")
                for s in stats:
                    print(f"  [{s['id_habilidade']}] {s['nome_habilidade']} (Pontos: {s['pontos_habilidade']})")
                    if s['efeito']:
                        print(f"      Efeito          : {s['efeito']}")
                    print(f"      Total Usuários  : {s['total_personagens']}")
                    print(f"      Classe Preferida: {s['classe_mais_comum'] or 'Nenhuma'}")
                    print(f"      Força Média     : {s['forca_media']} | INT Média: {s['inteligencia_media']}")
                    print("-" * 75)
                self.pedirEntrada("\nPressione Enter para continuar...")

            elif subOpcao == "9":
                self.limparTela()
                stats = self.controladora.estatisticasPorTipo()
                print("-" * 75)
                print("  COMPARATIVO POR TIPO DE PERSONAGEM (HERÓI, NPC, CRIATURA)")
                print("-" * 75)
                if not stats:
                    print("  Nenhum personagem encontrado.")
                for s in stats:
                    print(f"  Tipo: {s['tipo']:<12} | Total: {s['total_personagens']} personagem(ns)")
                    print(f"      Médias Atributos: FOR {s['forca_media']} | VIG {s['vigor_medio']} | INT {s['inteligencia_media']} | INIC {s['iniciativa_media']}")
                    print("-" * 75)
                self.pedirEntrada("\nPressione Enter para continuar...")

            elif subOpcao == "10":
                self.limparTela()
                print("-" * 75)
                print("  CONSULTA: TIPO DE PERSONAGEM + CARACTERÍSTICA ESPECIFICADA")
                print("-" * 75)
                tipoFiltro = self.pedirEntrada("Filtrar por Tipo (Herói / NPC / Criatura ou Enter para qualquer): ").strip()
                classeFiltro = self.pedirEntrada("Filtrar por Classe (ex: Guerreiro, Mago ou Enter para qualquer): ").strip()
                forcaStr = self.pedirEntrada("Força mínima (ou Enter para 0): ").strip()
                forcaMinima = int(forcaStr) if forcaStr.isdigit() else 0

                resultados = self.controladora.consultarTipoECaracteristica(tipoFiltro, classeFiltro, forcaMinima)
                print("-" * 75)
                if not resultados:
                    print("  Nenhum personagem atendeu aos critérios especificados.")
                for p in resultados:
                    print(f"  [{p['id_personagem']}] {p['nome_personagem']} | Tipo: {p['tipo']} | Classe: {p['classe']} | Raça: {p['raca']}")
                    print(f"      Jogador   : {p['nome_jogador']}")
                    print(f"      Atributos : FOR {p['forca']} | INT {p['inteligencia']} | VIG {p['vigor']} | INIC {p['iniciativa']}")
                    print(f"      Habilidades ({p['total_habilidades']}): {p['lista_habilidades']}")
                    print("-" * 75)
                self.pedirEntrada("\nPressione Enter para continuar...")

            elif subOpcao == "11":
                self.limparTela()
                stats = self.controladora.estatisticasTiposPorJogo()
                print("-" * 75)
                print("  CENSO DE PERSONAGENS POR JOGO")
                print("-" * 75)
                if not stats:
                    print("  Nenhum jogo encontrado.")
                for s in stats:
                    print(f"  [{s['id_jogo']}] {s['nome_jogo']} (Mestre: {s['nome_mestre']})")
                    print(f"      Total de Personagens: {s['total_geral_personagens']}")
                    print("-" * 75)
                self.pedirEntrada("\nPressione Enter para continuar...")

            elif subOpcao == "0":
                break


main = Main

if __name__ == "__main__":
    app = Main()
    app.menu()
