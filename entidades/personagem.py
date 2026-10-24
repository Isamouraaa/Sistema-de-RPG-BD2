class Personagem:
    def __init__(self, _idPersonagem=None, _nomePersonagem=None, _descricao=None, _tipo=None, _raca=None,
                 _classe=None, _forca=0, _inteligencia=0, _vigor=0, _destreza=0, _sabedoria=0,
                 _iniciativa=0, _habilidades=None, _idJogador=None, idPersonagem=None,
                 nomePersonagem=None, descricao=None, tipo=None, raca=None, classe=None,
                 forca=None, inteligencia=None, vigor=None, destreza=None, sabedoria=None,
                 iniciativa=None, habilidades=None, idJogador=None, idJogo=None, _idJogo=None, **kwargs):
        self._idPersonagem = idPersonagem if idPersonagem is not None else (_idPersonagem if _idPersonagem is not None else kwargs.get('_idPersonagem'))
        self._nomePersonagem = nomePersonagem if nomePersonagem is not None else (_nomePersonagem if _nomePersonagem is not None else kwargs.get('_nomePersonagem'))
        self._descricao = descricao if descricao is not None else (_descricao if _descricao is not None else kwargs.get('_descricao'))
        self._tipo = tipo if tipo is not None else (_tipo if _tipo is not None else kwargs.get('_tipo'))
        self._raca = raca if raca is not None else (_raca if _raca is not None else kwargs.get('_raca'))
        self._classe = classe if classe is not None else (_classe if _classe is not None else kwargs.get('_classe'))
        self._forca = forca if forca is not None else (_forca if _forca is not None else kwargs.get('_forca', 0))
        self._inteligencia = inteligencia if inteligencia is not None else (_inteligencia if _inteligencia is not None else kwargs.get('_inteligencia', 0))
        self._vigor = vigor if vigor is not None else (_vigor if _vigor is not None else kwargs.get('_vigor', 0))
        self._destreza = destreza if destreza is not None else (_destreza if _destreza is not None else kwargs.get('_destreza', 0))
        self._sabedoria = sabedoria if sabedoria is not None else (_sabedoria if _sabedoria is not None else kwargs.get('_sabedoria', 0))
        inic = iniciativa if iniciativa is not None else (_iniciativa if _iniciativa is not None else kwargs.get('_iniciativa', kwargs.get('_iniciatica', 0)))
        self._iniciativa = inic
        self._iniciatica = inic
        habs = habilidades if habilidades is not None else (_habilidades if _habilidades is not None else kwargs.get('_habilidades'))
        self._habilidades = list(habs) if habs is not None else []
        self._idJogador = idJogador if idJogador is not None else (_idJogador if _idJogador is not None else kwargs.get('_idJogador'))
        self._idJogo = idJogo if idJogo is not None else (_idJogo if _idJogo is not None else kwargs.get('_idJogo'))

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
        return self._iniciativa

    def getHabilidades(self):
        return list(self._habilidades)
    
    def getIdJogador(self):
        return self._idJogador

    def getIdJogo(self):
        return self._idJogo

    #setters
    def setIdPersonagem(self,id):
        self._idPersonagem = id

    def setNomePersonagem(self,nome):
        self._nomePersonagem = nome

    def setDescricao(self,novaDescricao):
        self._descricao = novaDescricao

    def setTipo(self, novoTipo):
        self._tipo = novoTipo

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
        self._iniciativa = novaInic
        self._iniciatica = novaInic

    def setHabilidades(self, novasHab):
        self._habilidades = list(novasHab)
    
    def setIdJogador(self, idJoga):
        self._idJogador = idJoga

    def setIdJogo(self, novoIdJogo):
        self._idJogo = novoIdJogo
