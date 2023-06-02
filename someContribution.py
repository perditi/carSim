# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 10:37:01 2023

@author: timot
"""

import numpy as np
from collections import deque
import time
import threading

DIRECTIONS = np.array(["left", "straight", "right"])
GEN = np.random.default_rng(None)#use GEN.poisson(1)
#lambda is average number of cars per period of time
LAMBDA = 5
PER_SECONDS = 30#say the period of time is 30 seconds
PASS_TIME = 3#say it takes 3 seconds for a car to leave the intersection



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
    def __gt__(self, other):
        return (not (self < other)) and (self != other)
    def __le__(self, other):
        return not (self > other)
    def __ge__(self, other):
        return not (self < other)
    def __str__(self):
        return f"Turning {self.direction}, arrived at " + time.strftime("%H:%M:%S", self.arrivalTime)
    
class Road:
    def __init__(self):
        self.q = deque()
        
    def put(self, n):
        self.q.append(Car())
        time.sleep(PER_SECONDS/(n))
            
    def pop(self):
        time.sleep(PASS_TIME)
        return self.q.popleft()
    
    def peek(self):
        temp = self.q.popleft()
        self.q.appendleft(temp)
        return temp
    
    def __str__(self):
        string = ""
        r = len(self.q)
        if r == 0:
            string = "Road is empty\n"
        else:
            for i in range(r):
                temp = self.q.popleft()
                string = string + temp.__str__() + "\n"
                self.q.append(temp)
        return string
        
            

ROADS = np.array([Road(), Road(), Road(), Road()])#N E S W

numCars = GEN.poisson(LAMBDA)
threads = deque()
print(time.strftime("%H:%M:%S", time.localtime()))
for i in range(numCars):
    threads.append(threading.Thread(target=ROADS[GEN.integers(0,4)].put, args=[numCars]))
    print("chk1")
    
for i in range(len(threads)):
    print("chk2")
    temp = threads.popleft()
    print("chk3")
    temp.run()
    print("chk4")
#i tried to use threads to do some concurrent stuff, because technically cars could arrive
#at the same time. the concurrency isn't working rn, but the cars still arrive so
#this will work for now

print(time.strftime("%H:%M:%S", time.localtime()))
print(ROADS[0])
print(ROADS[1])
print(ROADS[2])
print(ROADS[3])