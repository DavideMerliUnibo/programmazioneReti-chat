#!/usr/bin/env python3
class Domanda:
    
    def _init_(self, materia, domanda, risposta):
        self.materia = materia
        self.domanda = domanda
        self.risposta = risposta
        
    @classmethod
    def getMateria(self):
        return self.materia
    
    @classmethod
    def getDomanda(self):
        return self.domanda
    
    @classmethod
    def getRisposta(self):
        return self.risposta