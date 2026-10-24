import json
from entidades.personagem import Personagem

class SerializadorPersonagem:

    def serializarInfosPersonagens(self, personagens):
        payload = [self._personagemParaDict(personagem) for personagem in personagens]
        return json.dumps(payload, ensure_ascii=False, indent=2)

    def desserializarInfosPersonagens(self, dados):
        try:
            payload = json.loads(dados)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON inválido: {exc}") from exc

        personagens = []
        for item in payload:
            try:
                personagens.append(
                    Personagem(
                        idPersonagem=item.get("_idPersonagem"),
                        nomePersonagem=item["_nomePersonagem"],
                        descricao=item["_descricao"],
                        tipo=item["_tipo"],
                        raca=item["_raca"],
                        classe=item["_classe"],
                        forca=item["_forca"],
                        inteligencia=item["_inteligencia"],
                        vigor=item["_vigor"],
                        destreza=item["_destreza"],
                        sabedoria=item["_sabedoria"],
                        iniciativa=item["_iniciativa"],
                        habilidades=item.get("_habilidades", []),
                        idJogador=item.get("_idJogador"),
                        idJogo=item.get("_idJogo")
                    )
                )
            except KeyError as exc:
                raise ValueError(f"Campo obrigatório ausente no JSON: {exc}") from exc
        return personagens

    @staticmethod
    def _personagemParaDict(personagem):
        return {
            "_idPersonagem": personagem.getIdPersonagem(),
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
            "_habilidades": personagem.getHabilidades(),
            "_idJogador": personagem.getIdJogador(),
            "_idJogo": personagem.getIdJogo(),
        }
