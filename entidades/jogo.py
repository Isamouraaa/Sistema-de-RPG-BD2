class Jogo:

    def __init__(
        self,
        idJogo=None,
        nome="",
        descricao="",
        idMestre=None,
        jogadores=None,
        npcs=None,
        criaturas=None,
        nomeMestre=None,
        totalJogadores=0,
        totalPersonagens=0,
        classeMaisComum=None,
        forcaMedia=0.0,
    ):
        # Atributos principais
        self._idJogo = idJogo
        self._nome = nome
        self._descricao = descricao
        self._idMestre = idMestre
        self._jogadores = jogadores if jogadores is not None else []
        self._npcs = npcs if npcs is not None else []
        self._criaturas = criaturas if criaturas is not None else []

        # Atributos de estatísticas integrados
        self._nomeMestre = nomeMestre
        self._totalJogadores = totalJogadores
        self._totalPersonagens = totalPersonagens
        self._classeMaisComum = classeMaisComum
        self._forcaMedia = forcaMedia

    # Getters e Setters Principais 
    def getIdJogo(self):
        return self._idJogo

    def setIdJogo(self, valor):
        self._idJogo = valor

    def getNome(self):
        return self._nome

    def setNome(self, valor):
        self._nome = valor

    def getDescricao(self):
        return self._descricao

    def setDescricao(self, valor):
        self._descricao = valor

    def getIdMestre(self):
        return self._idMestre

    def setIdMestre(self, valor):
        self._idMestre = valor

    def getJogadores(self):
        return self._jogadores

    def getNpcs(self):
        return self._npcs

    def getCriaturas(self):
        return self._criaturas

    # Getters e Setters de Estatísticas 
    def getNomeMestre(self):
        return self._nomeMestre

    def setNomeMestre(self, valor):
        self._nomeMestre = valor

    def getTotalJogadores(self):
        return self._totalJogadores

    def setTotalJogadores(self, valor):
        self._totalJogadores = valor

    def getTotalPersonagens(self):
        return self._totalPersonagens

    def setTotalPersonagens(self, valor):
        self._totalPersonagens = valor

    def getClasseMaisComum(self):
        return self._classeMaisComum

    def setClasseMaisComum(self, valor):
        self._classeMaisComum = valor

    def getForcaMedia(self):
        return self._forcaMedia

    def setForcaMedia(self, valor):
        self._forcaMedia = valor

    def __repr__(self):
        return (
            f"Jogo("
            f"idJogo={self._idJogo!r}, "
            f"nome={self._nome!r}, "
            f"descricao={self._descricao!r}, "
            f"idMestre={self._idMestre!r}, "
            f"nomeMestre={self._nomeMestre!r}, "
            f"totalJogadores={self._totalJogadores!r}, "
            f"totalPersonagens={self._totalPersonagens!r}, "
            f"classeMaisComum={self._classeMaisComum!r}, "
            f"forcaMedia={self._forcaMedia!r})"
        )