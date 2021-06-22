#!/usr/bin/env python3
import time as t
from threading import Thread
from tkinter import Label

class Timer:
    
    def __init__(self, label):
        Thread.__init__(self)
        self.contatore = 120
        self.label = label
        self.countdown()
        
    def countdown(cls):
        while cls.contatore > 0:
            t.sleep(1)
            cls.contatore = cls.contatore - 1;
            cls.label.config(text = cls.converti(cls.contatore))
            
    def converti(cls, numero):
        minuti = 0
        while numero > 60:
            minuti = minuti + 1
            numero = numero - 60
        secondi = numero
        #sistemare la stampa e poi forse va
        return minuti + ':' + secondi + 's'
            
            