from __future__ import annotations
import json
from jogador import Jogador

class SerializadorJogador:

    def serializar_infos_jogadores(self, jogadores: list[Jogador]) -> str:
        payload = [self._jogador_para_dict(jogador) for jogador in jogadores]
        return json.dumps(payload, ensure_ascii=False, indent=2)

    def desserializar_infos_jogadores(self, dados: str) -> list[Jogador]:
        try:
            payload: list[dict] = json.loads(dados)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON inválido: {exc}") from exc

        jogadores: list[Jogador] = []
        for item in payload:
            try:
                jogadores.append(
                    Jogador(
                        _idJogador=item.get("_idJogador"),
                        _nomeJogador=item["_nomeJogador"]
                    )
                )
            except KeyError as exc:
                raise ValueError(f"Campo obrigatório ausente no JSON: {exc}") from exc
        return jogadores

    @staticmethod
    def _jogador_para_dict(jogador: Jogador) -> dict:
        return {
            "_idJogador": jogador.getIdJogador(),
            "_nomeJogador": jogador.getNome(),
        }
