from entidades.personagem import Personagem

class Combate:

    def __init__(self, idPartida, personagens, controladoraPersonagem=None):
        self._idPartida = idPartida
        self._iniciativas = self._ordenarIniciativas(personagens)
        self._indiceTurno = 0
        self._turno = self._iniciativas[0][0].getNomePersonagem() if self._iniciativas else ""
        self._controladoraPersonagem = controladoraPersonagem

    def getIdPartida(self):
        return self._idPartida

    def getTurno(self):
        return self._turno

    def getIniciativas(self):
        return self._iniciativas

    def iniciarCombate(self):
        if not self._iniciativas:
            print("Nenhum personagem na lista de iniciativas.")
            return

        while True:
            self._exibirTelaCombate()
            opcao = input("\nOpção: ").strip()

            if opcao == "1":
                self.proximoTurno()
            elif opcao == "2":
                nome = input("Nome do personagem a editar: ").strip()
                personagem = self._buscarPersonagemPorNome(nome)
                if personagem:
                    self.chamaEdicao(personagem)
                else:
                    print(f"Personagem '{nome}' não encontrado.")
                    input("Pressione Enter para continuar...")
            elif opcao == "0":
                print("Combate encerrado.")
                break
            else:
                print("Opção inválida.")
                input("Pressione Enter para continuar...")

    def proximoTurno(self):
        if not self._iniciativas:
            return
        self._indiceTurno = (self._indiceTurno + 1) % len(self._iniciativas)
        self._turno = self._iniciativas[self._indiceTurno][0].getNomePersonagem()

    def chamaEdicao(self, personagem):
        self._controladoraPersonagem.editarPersonagem(personagem)

    @staticmethod
    def _ordenarIniciativas(personagens):
        pares = [(p, p.getIniciativa()) for p in personagens]
        return sorted(pares, key=lambda x: x[1], reverse=True)

    def _buscarPersonagemPorNome(self, nome):
        for personagem, _ in self._iniciativas:
            if personagem.getNomePersonagem().lower() == nome.lower():
                return personagem
        return None

    def _exibirTelaCombate(self):
        print("\n" + "=" * 45)
        print(f"  COMBATE — Partida #{self._idPartida}")
        print("=" * 45)
        print(f"  Turno atual: {self._turno}")
        print("-" * 45)
        print(f"  {'#':<4} {'Personagem':<20} {'Iniciativa':>10}")
        print("-" * 45)
        for i, (personagem, iniciativa) in enumerate(self._iniciativas):
            marcador = ">>>" if personagem.getNomePersonagem() == self._turno else "   "
            print(f"  {marcador} {i + 1:<3} {personagem.getNomePersonagem():<20} {iniciativa:>10}")
        print("=" * 45)
        print("  [1] Próximo turno")
        print("  [2] Editar personagem")
        print("  [0] Encerrar combate")
        print("=" * 45)