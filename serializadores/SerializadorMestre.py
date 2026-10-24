import json
from entidades.mestre import Mestre

class SerializadorMestre:

    def serializarInfosMestres(self, mestres):
        payload = [self._mestreParaDict(m) for m in mestres]
        return json.dumps(payload, ensure_ascii=False, indent=2)

    def desserializarInfosMestres(self, dados):
        try:
            payload = json.loads(dados)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON inválido: {exc}") from exc

        mestres = []
        for item in payload:
            try:
                mestres.append(
                    Mestre(
                        idMestre=item.get("idMestre"),
                        nome=item["nome"],
                    )
                )
            except KeyError as exc:
                raise ValueError(f"Campo obrigatório ausente no JSON: {exc}") from exc
        return mestres

    @staticmethod
    def _mestreParaDict(mestre):
        return {
            "idMestre": mestre.getIdMestre(),
            "nome": mestre.getNome(),
        }