#!/usr/bin/env python3
import time as t
from threading import Thread

class Timer:
    
    def __init__(self):
        Thread.__init__(self)
        self.counter = 120
        
    def countdown(cls):
        while cls.counter > 0:
            t.sleep(1)
            cls.counter -= 1;
            return cls.converti(cls.counter)
            
    def converti(cls, num):
        minutes = 0
        while num >= 60:
            minutes = minutes + 1
            num = num - 60
        seconds = num
        return '{0:02d}:{1:02d}s'.format(minutes, seconds)