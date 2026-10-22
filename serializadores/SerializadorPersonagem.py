import json
from entidades.Personagem import Personagem


class SerializadorPersonagem:

    def personagem_para_dict(self, personagem: Personagem) -> dict:
        return {
            "id_personagem": personagem.getIdPersonagem(),
            "nome_personagem": personagem.getNomePersonagem(),
            "descricao": personagem.getDescricao(),
            "tipo": personagem.getTipo(),
            "raca": personagem.getRaca(),
            "classe": personagem.getClasse(),
            "forca": personagem.getForca(),
            "inteligencia": personagem.getInteligencia(),
            "vigor": personagem.getVigor(),
            "destreza": personagem.getDestreza(),
            "sabedoria": personagem.getSabedoria(),
            "iniciativa": personagem.getIniciativa(),
            "habilidades": personagem.getHabilidades(),
            "id_jogador": personagem.getIdJogador(),
        }

    def linha_para_personagem(self, linha: tuple, habilidades: list[str] | None = None) -> Personagem:
        return Personagem(
            idPersonagem=linha[0],
            nomePersonagem=linha[2],
            descricao=linha[3] or "",
            tipo=linha[4] or "",
            raca=linha[5] or "",
            classe=linha[6] or "",
            forca=linha[7] or 10,
            inteligencia=linha[8] or 10,
            vigor=linha[9] or 10,
            destreza=linha[10] or 10,
            sabedoria=linha[11] or 10,
            iniciativa=linha[12] or 10,
            habilidades=habilidades or [],
            idJogador=linha[1],
        )

    def serializar_infos_personagens(self, personagens: list[Personagem]) -> str:
        payload = [self.personagem_para_dict(p) for p in personagens]
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
                        idPersonagem=item.get("id_personagem"),
                        nomePersonagem=item["nome_personagem"],
                        descricao=item.get("descricao", ""),
                        tipo=item.get("tipo", ""),
                        raca=item.get("raca", ""),
                        classe=item.get("classe", ""),
                        forca=item.get("forca", 10),
                        inteligencia=item.get("inteligencia", 10),
                        vigor=item.get("vigor", 10),
                        destreza=item.get("destreza", 10),
                        sabedoria=item.get("sabedoria", 10),
                        iniciativa=item.get("iniciativa", 10),
                        habilidades=item.get("habilidades", []),
                        idJogador=item.get("id_jogador"),
                    )
                )
            except KeyError as exc:
                raise ValueError(f"Campo obrigatório ausente no JSON: {exc}") from exc
        return personagens


PersonagemSerializadora = SerializadorPersonagem
