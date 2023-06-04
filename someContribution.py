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
        print("does this run?")
        time.sleep(GEN.integers(0, PER_SECONDS+1))
        print("lmao")
        self.q.append(Car())
        print("yes it does")

            
    def pop(self, interference):#interference boolean, see if 2 cars can go at once
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

class Label:
    def __init__(self, car, label):#label which road it came from
        self.label = label#for ordering purposes
        self.car = car
        self.front = None
        
class Intersection:
    def __init__(self, ROADS):
        self.o = deque()#the order in which cars will go
        self.ROADS = ROADS
        
    def fill(self):
        self.front = np.array([Label(self.ROADS[0].peek(), 0), Label(self.ROADS[1].peek(), 1),
                               Label(self.ROADS[2].peek(), 2), Label(self.ROADS[3].peek(), 3)])
        while (len(self.ROADS[0]) != 0 or len(self.ROADS[1]) != 0 or len(self.ROADS[2]) != 0  or len(self.ROADS[3]) != 0 ):
            if len(self.ROADS[0]) != 0 and self.front[0].car == None:
                self.front[0] = Label(self.ROADS[0].peek(), 0)
            if len(self.ROADS[1]) != 0 and self.front[1].car == None:
                self.front[1] = Label(self.ROADS[1].peek(), 1)
            if len(self.ROADS[2]) != 0 and self.front[2].car == None:
                self.front[2] = Label(self.ROADS[2].peek(), 2)
            if len(self.ROADS[3]) != 0 and self.front[3].car == None:
                self.front[3] = Label(self.ROADS[3].peek(), 3)
        
    def order(self):
        while (self.front[0].car != None or self.front[1].car != None or self.front[2].car != None or self.front[3].car != None):
            for i in range(len(self.front) - 1):
                #sort in place, order all four cars
                return None
            
            
        

intersection = Intersection(np.array([Road(), Road(), Road(), Road()]))#N E S W

numCars = GEN.poisson(LAMBDA)
print("Number of cars entering the intersection: ", numCars)
threads = deque()
print(time.strftime("%H:%M:%S", time.localtime()))
for i in range(numCars):
    threads.append(threading.Thread(target=intersection.ROADS[GEN.integers(0,4)].put, args=[numCars]))
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
print("North Road:\n", intersection.ROADS[0])
print("East Road:\n", intersection.ROADS[1])
print("South Road:\n", intersection.ROADS[2])
print("West Road:\n", intersection.ROADS[3])