import json
from entidades.jogo import Jogo

class SerializadorJogo:

    def serializarInfosJogos(self, jogos):
        payload = [self._jogoParaDict(jogo) for jogo in jogos]
        return json.dumps(payload, ensure_ascii=False, indent=2)

    def desserializarInfosJogos(self, dados):
        try:
            payload = json.loads(dados)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON inválido: {exc}") from exc

        jogos = []
        for item in payload:
            try:
                jogos.append(
                    Jogo(
                        idJogo=item.get("idJogo"),
                        nome=item["nome"],
                        descricao=item["descricao"],
                        idMestre=item.get("idMestre"),
                        nomeMestre=item.get("nomeMestre"),
                        totalJogadores=item.get("totalJogadores", 0),
                        totalPersonagens=item.get("totalPersonagens", 0),
                        classeMaisComum=item.get("classeMaisComum"),
                        forcaMedia=item.get("forcaMedia", 0.0),
                    )
                )
            except KeyError as exc:
                raise ValueError(f"Campo obrigatório ausente no JSON: {exc}") from exc
        return jogos

    @staticmethod
    def _jogoParaDict(jogo):
        return {
            "idJogo": jogo.getIdJogo(),
            "nome": jogo.getNome(),
            "descricao": jogo.getDescricao(),
            "idMestre": jogo.getIdMestre(),
            "nomeMestre": jogo.getNomeMestre(),
            "totalJogadores": jogo.getTotalJogadores(),
            "totalPersonagens": jogo.getTotalPersonagens(),
            "classeMaisComum": jogo.getClasseMaisComum(),
            "forcaMedia": jogo.getForcaMedia(),
        }