#!/usr/bin/env python3
import time as t
from threading import Thread

class Timer:
    
    def __init__(self):
        Thread.__init__(self)
        self.contatore = 120
        
    def countdown(cls):
        while cls.contatore > 0:
            t.sleep(1)
            cls.contatore -= 1;
            return cls.converti(cls.contatore)
            
    def converti(cls, numero):
        minuti = 0
        while numero >= 60:
            minuti = minuti + 1
            numero = numero - 60
        secondi = numero
        #sistemare la stampa e poi forse va
        s = ""
        s = s + str(minuti) + ':' + str(secondi) + 's'
        return s