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
    def __init__(self, interference):#interference boolean, see if 2 cars can go at once
        self.direction = DIRECTIONS[GEN.integers(0,3)]#random direction
        self.arrivalTime = time.localtime()
        self.interference = interference
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
        print("does this run?")
        time.sleep(GEN.integers(0, PER_SECONDS+1))
        print("lmao")
        self.q.append(Car())
        print("yes it does")

            
    def pop(self):
        if interference:
            time.sleep(PASS_TIME)
        return self.q.popleft()
    
    def peek(self):
        temp = None
        if (len(self.q)) > 0:
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

class Intersection:
    def __init__(self):
        self.
        
            

ROADS = np.array([Road(), Road(), Road(), Road()])#N E S W

numCars = GEN.poisson(LAMBDA)
print("Number of cars entering the intersection: ", numCars)
threads = deque()
print(time.strftime("%H:%M:%S", time.localtime()))
for i in range(numCars):
    threads.append(threading.Thread(target=ROADS[GEN.integers(0,4)].put, args=[numCars]))
    #print("chk1")


for i in range(len(threads)):
    #print("chk2")
    temp = threads.popleft()
    #print("chk3")
    temp.start()
    threads.append(temp)

timer = threading.Thread(target=time.sleep(PER_SECONDS))
timer.start()
threads.append(timer)
    
for i in range(len(threads)):
    temp = threads.popleft()
    temp.join()
    print("chk4")
#i tried to use threads to do some concurrent stuff, because technically cars could arrive
#at the same time. the concurrency isn't working rn, but the cars still arrive so
#this will work for now

print(time.strftime("%H:%M:%S", time.localtime()))
print(ROADS[0])
print(ROADS[1])
print(ROADS[2])
print(ROADS[3])

front = np.array([ROADS[0].peek(), ROADS[1].peek(), ROADS[2].peek(), ROADS[3].peek()])
print(front[0])
print(front[1])
print(front[2])
print(front[3])