import json
from entidades.Mestre import Mestre


class SerializadorMestre:

    def mestre_para_dict(self, mestre: Mestre) -> dict:
        return {
            "id_mestre": mestre.id_mestre,
            "nome": mestre.nome,
        }

    def linha_para_mestre(self, linha: tuple) -> Mestre:
        return Mestre(id_mestre=linha[0], nome=linha[1])

    def serializar_infos_mestres(self, mestres: list[Mestre]) -> str:
        payload = [self.mestre_para_dict(m) for m in mestres]
        return json.dumps(payload, ensure_ascii=False, indent=2)

    def desserializar_infos_mestres(self, dados: str) -> list[Mestre]:
        try:
            payload: list[dict] = json.loads(dados)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON inválido: {exc}") from exc

        mestres: list[Mestre] = []
        for item in payload:
            try:
                mestres.append(Mestre(id_mestre=item.get("id_mestre"), nome=item["nome"]))
            except KeyError as exc:
                raise ValueError(f"Campo obrigatório ausente no JSON: {exc}") from exc
        return mestres
