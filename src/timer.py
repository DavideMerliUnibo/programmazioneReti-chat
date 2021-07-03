#!/usr/bin/env python3
import time as t
from threading import Thread

class Timer:
    
    def __init__(self):
        Thread.__init__(self)
        self.contatore = 20
        
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
        return '{0:02d}:{1:02d}s'.format(minuti, secondi)