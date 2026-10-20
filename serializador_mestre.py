from __future__ import annotations

import json

from mestre import Mestre


class SerializadorMestre:

    def serializar_infos_mestres(self, mestres: list[Mestre]) -> str:
        payload = [self._mestre_para_dict(m) for m in mestres]
        return json.dumps(payload, ensure_ascii=False, indent=2)

    def desserializar_infos_mestres(self, dados: str) -> list[Mestre]:
        try:
            payload: list[dict] = json.loads(dados)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON inválido: {exc}") from exc

        mestres: list[Mestre] = []
        for item in payload:
            try:
                mestres.append(
                    Mestre(
                        id_mestre=item.get("id_mestre"),
                        nome=item["nome"],
                    )
                )
            except KeyError as exc:
                raise ValueError(f"Campo obrigatório ausente no JSON: {exc}") from exc
        return mestres

    @staticmethod
    def _mestre_para_dict(mestre: Mestre) -> dict:
        return {
            "id_mestre": mestre.id_mestre,
            "nome": mestre.nome,
        }
