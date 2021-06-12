#!/usr/bin/env python3
class Giocatore:
    
    def __init__(self, nome, ruolo, punteggio):
        self.nome = nome
        self.ruolo = ruolo
        self.punteggio = punteggio
        
    @classmethod
    def getNome(self):
        return self.nome
    
    @classmethod
    def getRuolo(self):
        return self.ruolo
    
    @classmethod
    def getPunteggio(self):
        return self.punteggio