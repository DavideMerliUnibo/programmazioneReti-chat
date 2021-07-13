#!/usr/bin/env python3
import time as t
import tkinter as tk
import sys
from threading import Thread

class Timer:
    
    def __init__(self, ):
        Thread.__init__(self)
        self.counter = 20
        self.running = True
        self.timerLabel = tk.Label(text = self.converti(self.counter))
        
    def countdown(cls):
        while cls.counter > 0:
            if cls.running == False:
                sys.exit(1)
            t.sleep(1)
            cls.counter -= 1
            cls.timerLabel.config(text = cls.converti(cls.counter))
            
    def converti(cls, num):
        minutes = 0
        while num >= 60:
            minutes += 1
            num -= 60
        seconds = num
        return '{0:02d}:{1:02d}s'.format(minutes, seconds)