class Personagem:
    def __init__(self,idPersonagem,nomePersonagem,descricao,tipo,raca,
                 classe,forca,inteligencia,vigor,destreza,sabedoria,
                 iniciativa,habilidades,idJogador):
        self._idPersonagem = idPersonagem
        self._nomePersonagem = nomePersonagem
        self._descricao = descricao
        self._tipo = tipo
        self._raca = raca
        self._classe = classe
        self._forca = forca
        self._inteligencia = inteligencia
        self._vigor = vigor
        self._destreza = destreza
        self._sabedoria = sabedoria
        self._iniciatica = iniciativa
        self._habilidades = habilidades
        self._idJogador = idJogador

    def getIdPersonagem(self):
        return self._idPersonagem

    def getNomePersonagem(self):
        return self._nomePersonagem

    def getDescricao(self):
        return self._descricao

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
        return self._habilidades
    
    def getIdJogador(self):
        return self._idJogador



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

    def setHabilidades(self, novaHab):
        self._habilidades.append(novaHab)
    
    def setIdJogador(self, idJoga):
        self._idJogador = idJoga
