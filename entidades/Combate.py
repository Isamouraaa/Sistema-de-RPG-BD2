from entidades.Personagem import Personagem


class Combate:

    def __init__(self, id_partida: int, personagens: list[Personagem], controladora_personagem=None) -> None:
        self._id_partida: int = id_partida
        self._iniciativas: list[tuple[Personagem, int]] = self._ordenar_iniciativas(personagens)
        self._indice_turno: int = 0
        self._turno: str = self._iniciativas[0][0].getNomePersonagem() if self._iniciativas else ""
        self._controladora_personagem = controladora_personagem

    def getIdPartida(self) -> int:
        return self._id_partida

    def getTurno(self) -> str:
        return self._turno

    def getIniciativas(self) -> list[tuple[Personagem, int]]:
        return self._iniciativas

    def iniciarCombate(self) -> None:
        if not self._iniciativas:
            print("Nenhum personagem na lista de iniciativas.")
            return

        while True:
            self._exibir_tela_combate()
            opcao = input("\nOpção: ").strip()

            if opcao == "1":
                self.proximoTurno()
            elif opcao == "2":
                nome = input("Nome do personagem a editar: ").strip()
                personagem = self._buscar_personagem_por_nome(nome)
                if personagem:
                    self.chamaEdicao(personagem)
                else:
                    print(f"Personagem '{nome}' não encontrado.")
                    input("Pressione Enter para continuar...")
            elif opcao == "0":
                self.finalizarCombate()
                break
            else:
                print("Opção inválida.")
                input("Pressione Enter para continuar...")

    def finalizarCombate(self) -> None:
        print("Combate encerrado.")

    def proximoTurno(self) -> None:
        if not self._iniciativas:
            return
        self._indice_turno = (self._indice_turno + 1) % len(self._iniciativas)
        self._turno = self._iniciativas[self._indice_turno][0].getNomePersonagem()

    def chamaEdicao(self, personagem: Personagem) -> None:
        if self._controladora_personagem:
            nova_iniciativa = input(f"Nova iniciativa [{personagem.getIniciativa()}]: ").strip()
            if nova_iniciativa.isdigit():
                personagem.setIniciativa(int(nova_iniciativa))
            self._controladora_personagem.editarPersonagem(personagem.getIdPersonagem(), personagem)
            self._iniciativas = self._ordenar_iniciativas([p for p, _ in self._iniciativas])

    def _ordenar_iniciativas(self, personagens: list[Personagem]) -> list[tuple[Personagem, int]]:
        pares = [(p, p.getIniciativa()) for p in personagens]
        return sorted(pares, key=lambda x: x[1], reverse=True)

    def _buscar_personagem_por_nome(self, nome: str) -> Personagem | None:
        for personagem, _ in self._iniciativas:
            if personagem.getNomePersonagem().lower() == nome.lower():
                return personagem
        return None

    def _exibir_tela_combate(self) -> None:
        print("\n" + "=" * 45)
        print(f"  COMBATE — Partida #{self._id_partida}")
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
