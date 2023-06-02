# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 10:37:01 2023

@author: timot
"""

import numpy as np
import queue as q
import time

DIRECTIONS = np.array(["left", "straight", "right"])
GEN = np.random.default_rng(None)#use GEN.poisson(1)
#lambda is average number of cars per period of time -- how long do i want??
#five seconds isn't bad but how fast are these fucking cars going :skull:

PER_SECONDS = 5#say the period of time is 30 seconds

class Car:
    def __init__(self):
        self.direction = DIRECTIONS[GEN.integers(0,3)]#random direction
        self.arrivalTime = time.localtime()
    def __eq__(self, other):
        return (self.arrivalTime == other.arrivalTime)
    def __ne__(self, other):
        return not (self == other)
    def __lt__(self, other):
        return (self.arrivalTime < other.arrivalTime)
    def __le__(self, other):
        return ((self == other) or (self < other))
    def __gt__(self, other):
        return not (self < other)
    def __ge__(self, other):
        return ((self == other) or (not (self < other)))
    def __str__(self):
        return f"Turning {self.direction}, arrived at " + time.strftime("%H:%M:%S", self.arrivalTime)
    
class Road:
    def __init__(self):
        self.q = q.Queue()
        
    def put(self, n):
        for i in range(n):
            self.q.put(Car())
            if i < n:
                time.sleep(PER_SECONDS/(n-1))
            
    def pop(self):
        return self.q.get()
    
    def __str__(self):
        tempQ = q.Queue()
        string = ""
        r = self.q.qsize()
        for i in range(r):
            temp = self.q.get()
            string = string + temp.__str__() + "\n"
            tempQ.put(temp)
        for i in range(r):
            self.q.put(tempQ.get())
        return string
        
            

ROADS = np.array([Road(), Road(), Road(), Road()])#N E S W


ROADS[0].put(2)
print(ROADS[0])
test1 = ROADS[0].pop()
test2 = ROADS[0].pop()
print(test1)
print(test2)
print(test1 < test2)
print(test2 > test1)
print(test1 != test2)


