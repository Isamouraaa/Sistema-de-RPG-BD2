class Personagem:
    def __init__(self,_idPersonagem,_nomePersonagem,_descricao,_tipo,_raca,
                 _classe,_forca,_inteligencia,_vigor,_destreza,_sabedoria,
                 _iniciativa,_habilidades,_idJogador):
        self._idPersonagem = _idPersonagem
        self._nomePersonagem = _nomePersonagem
        self._descricao = _descricao
        self._tipo = _tipo
        self._raca = _raca
        self._classe = _classe
        self._forca = _forca
        self._inteligencia = _inteligencia
        self._vigor = _vigor
        self._destreza = _destreza
        self._sabedoria = _sabedoria
        self._iniciatica = _iniciativa
        self._habilidades = _habilidades if _habilidades is not None else []
        self._idJogador = _idJogador

    #getters
    def getIdPersonagem(self):
        return self._idPersonagem

    def getNomePersonagem(self):
        return self._nomePersonagem

    def getDescricao(self):
        return self._descricao

    def getTipo(self):
        return self._tipo

    def getRaca(self):
        return self._raca

    def getClasse(self):
        return self._classe

    def getForca(self):
        return self._forca

    def getInteligencia(self):
        return self._inteligencia

    def getVigor(self):
        return self._vigor

    def getDestreza(self):
        return self._destreza

    def getSabedoria(self):
        return self._sabedoria

    def getIniciativa(self):
        return self._iniciatica

    def getHabilidades(self):
        return list(self._habilidades)
    
    def getIdJogador(self):
        return self._idJogador

    #setters
    def setIdPersonagem(self,id):
        self._idPersonagem = id

    def setNomePersonagem(self,nome):
        self._nomePersonagem = nome

    def setDescricao(self,novaDescricao):
        self._descricao = novaDescricao

    def setRaca(self,novaRaca):
        self._raca = novaRaca

    def setClasse(self,novaClasse):
        self._classe = novaClasse

    def setForca(self,novaForca):
        self._forca = novaForca

    def setInteligencia(self,novaInt):
        self._inteligencia = novaInt

    def setVigor(self,novoVigor):
        self._vigor = novoVigor

    def setDestreza(self,novaDex):
        self._destreza = novaDex

    def setSabedoria(self, novaSab):
        self._sabedoria = novaSab

    def setIniciativa(self, novaInic):
        self._iniciatica = novaInic

    def setHabilidades(self, novasHab):
        self._habilidades = list(novasHab)
    
    def setIdJogador(self, idJoga):
        self._idJogador = idJoga
