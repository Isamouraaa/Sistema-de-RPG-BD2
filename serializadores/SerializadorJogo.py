import json
from entidades.Jogo import Jogo


class SerializadorJogo:

    def jogo_para_dict(self, jogo: Jogo) -> dict:
        return {
            "id_jogo": jogo.id_jogo,
            "nome": jogo.nome,
            "descricao": jogo.descricao,
            "id_mestre": jogo.id_mestre,
        }

    def linha_para_jogo(self, linha: tuple) -> Jogo:
        return Jogo(id_jogo=linha[0], id_mestre=linha[1], nome=linha[2], descricao=linha[3] or "")

    def serializar_infos_jogos(self, jogos: list[Jogo]) -> str:
        payload = [self.jogo_para_dict(jogo) for jogo in jogos]
        return json.dumps(payload, ensure_ascii=False, indent=2)

    def desserializar_infos_jogos(self, dados: str) -> list[Jogo]:
        try:
            payload: list[dict] = json.loads(dados)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON inválido: {exc}") from exc

        jogos: list[Jogo] = []
        for item in payload:
            try:
                jogos.append(
                    Jogo(
                        id_jogo=item.get("id_jogo"),
                        nome=item["nome"],
                        descricao=item.get("descricao", ""),
                        id_mestre=item.get("id_mestre"),
                    )
                )
            except KeyError as exc:
                raise ValueError(f"Campo obrigatório ausente no JSON: {exc}") from exc
        return jogos
