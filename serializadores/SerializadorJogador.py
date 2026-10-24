import json
from entidades.jogador import Jogador

class SerializadorJogador:

    def serializarInfosJogadores(self, jogadores):
        payload = [self._jogadorParaDict(jogador) for jogador in jogadores]
        return json.dumps(payload, ensure_ascii=False, indent=2)

    def desserializarInfosJogadores(self, dados):
        try:
            payload = json.loads(dados)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON inválido: {exc}") from exc

        jogadores = []
        for item in payload:
            try:
                jogadores.append(
                    Jogador(
                        idJogador=item.get("_idJogador"),
                        nomeJogador=item["_nomeJogador"]
                    )
                )
            except KeyError as exc:
                raise ValueError(f"Campo obrigatório ausente no JSON: {exc}") from exc
        return jogadores

    @staticmethod
    def _jogadorParaDict(jogador):
        return {
            "_idJogador": jogador.getIdJogador(),
            "_nomeJogador": jogador.getNomeJogador(),
        }