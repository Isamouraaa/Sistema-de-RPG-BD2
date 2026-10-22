from __future__ import annotations
import json
from personagem import Personagem

class PersonagemSerializadora:

    def serializar_infos_jogadores(self, personagens: list[Personagem]) -> str:
        payload = [self._personagem_para_dict(personagem) for personagem in personagens]
        return json.dumps(payload, ensure_ascii=False, indent=2)

    def desserializar_infos_personagem(self, dados: str) -> list[Personagem]:
        try:
            payload: list[dict] = json.loads(dados)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON inválido: {exc}") from exc

        personagens: list[Personagem] = []
        for item in payload:
            try:
                personagens.append(
                    Personagem(
                        _idPersonagem=item.get("_idPersonagem"),
                        _nomePersonagem=item["_nomePersonagem"],
                        _descricao=item["_descricao"],
                        _tipo=item["_tipo"],
                        _raca=item["_raca"],
                        _classe=item["_classe"],
                        _forca=item["_forca"],
                        _inteligencia=item["_inteligencia"],
                        _vigor=item["_vigor"],
                        _destreza=item["_destreza"],
                        _sabedoria=item["_sabedoria"],
                        _iniciativa=item["_iniciativa"],
                        _idJogador=item.get("_idJogador")
                    )
                )
            except KeyError as exc:
                raise ValueError(f"Campo obrigatório ausente no JSON: {exc}") from exc
        return personagens

    @staticmethod
    def _personagem_para_dict(personagem: Personagem) -> dict:
        return {
            "id_personagem": personagem.getIdPersonagem(),
            "_nomePersonagem": personagem.getNomePersonagem(),
            "_descricao": personagem.getDescricao(),
            "_tipo": personagem.getTipo(),
            "_raca": personagem.getRaca(),
            "_classe": personagem.getClasse(),
            "_forca": personagem.getForca(),
            "_inteligencia": personagem.getInteligencia(),
            "_vigor": personagem.getVigor(),
            "_destreza": personagem.getDestreza(),
            "_sabedoria": personagem.getSabedoria(),
            "_iniciativa": personagem.getIniciativa(),
            "_idJogador": personagem.getIdJogador(),
        }