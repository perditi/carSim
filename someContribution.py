# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 10:37:01 2023

@author: timot
"""

import numpy as np
from collections import deque
import time
import threading

DIRECTIONS = np.array(["north", "east", "south", "west"])
GEN = np.random.default_rng(None)#use GEN.poisson(1)
#lambda is average number of cars per period of time
LAMBDA = 5
PER_SECONDS = 30#say the period of time is 30 seconds
PASS_TIME = 3#say it takes 3 seconds for a car to leave the intersection



class Car:
    def __init__(self, road):
        self.road = road
        self.destination = GEN.integers(0,4)#random direction
        self.arrivalTime = time.localtime()
    def __eq__(self, other):
        if other == None:
            return False
        return (self.arrivalTime == other.arrivalTime)
    def __ne__(self, other):
        return not (self == other)
    def __lt__(self, other):
        if other == None:
            return False
        return (self.arrivalTime < other.arrivalTime)
    def __gt__(self, other):
        return (not (self < other)) and (self != other)
    def __le__(self, other):
        return not (self > other)
    def __ge__(self, other):
        return not (self < other)
    def __str__(self):
        direction = DIRECTIONS[self.destination]
        coming = DIRECTIONS[self.road]
        return f"From the {coming} Road, going {direction}, arrived at " + time.strftime("%H:%M:%S", self.arrivalTime)
    
class Road:
    def __init__(self, road):
        self.q = deque()
        self.road = road
        
    def put(self):
        print("put called successfully")
        time.sleep(GEN.integers(0, PER_SECONDS+1))
        temp = Car(self.road)
        self.q.append(temp)
        print(temp)

            
    def pop(self):
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
    def __init__(self, ROADS, startTime):
        self.o = deque()#the order in which cars will go
        self.ROADS = ROADS
        self.stop = False
        
    def sleep(self, num):
        time.sleep(num)
        self.stop = True
        
    def fill(self):
        self.front = np.array([self.ROADS[0].peek(), self.ROADS[1].peek(),
                               self.ROADS[2].peek(), self.ROADS[3].peek()])
        #print("start of fill")
        while (not self.stop or (len(self.ROADS[0].q) != 0 or len(self.ROADS[1].q) != 0 or len(self.ROADS[2].q) != 0  or len(self.ROADS[3].q) != 0 )):
            if len(self.ROADS[0].q) != 0 and self.front[0] == None:
                self.front[0] = self.ROADS[0].peek()
            if len(self.ROADS[1].q) != 0 and self.front[1] == None:
                self.front[1] = self.ROADS[1].peek()
            if len(self.ROADS[2].q) != 0 and self.front[2] == None:
                self.front[2] = self.ROADS[2].peek()
            if len(self.ROADS[3].q) != 0 and self.front[3] == None:
                self.front[3] = self.ROADS[3].peek()
            #print(self.front)
            self.sort(self.front)
            #print("sorted")
            #print(self.front)
            goThread = threading.Thread(target=self.go)
            #print("running goThread")
            goThread.run()
            #print("presleep")
            time.sleep(1)
            #print("postsleep")
        #print("end of fill")
        
    def go(self):
        #print("start go")
        going = deque()
        if self.front[0] != None:
            going.append(0)
            first = self.front[0]
            firstFrom = self.shift(first.road, first.road)
            firstTo = self.shift(first.destination, first.road)
            for r in range(len(self.front)):
                if self.front[r] != None:
                    compareFrom = self.shift(self.front[r].road, first.road)
                    compareTo = self.shift(self.front[r].destination, first.road)
                    if (compareFrom > firstFrom and compareTo != firstTo):
                        if (compareFrom > firstFrom and compareFrom <= firstTo):
                            if (compareTo >= firstFrom and compareTo < firstTo):
                                going.append(r)
                        elif (compareFrom > firstTo and compareTo > firstTo):
                            going.append(r)
            thr = deque()
            for i in range(len(going)):
                t1 = threading.Thread(target=self.remove, args=[going.popleft()])
                t1.start()
                thr.append(t1)
            for i in range(len(thr)):
                temp = thr.popleft()
                temp.join()
            
        #print("end go")
        
    def shift(self, num, s):
        temp = num - s
        if temp < 0:
            temp += len(self.ROADS)
        return temp 
                    
    def remove(self, frontI):
        road = self.front[frontI].road
        leaving = self.ROADS[road].pop()
        self.front[frontI] = None
        startTime = time.mktime(leaving.arrivalTime)
        endTime = time.mktime(time.localtime())
        waitingTime = endTime - startTime
        print("A car from the", DIRECTIONS[leaving.road], "road has exited the intersection heading", DIRECTIONS[leaving.destination], ", total waiting time:", waitingTime, "seconds.")
        
    def sort(self, a):
        num = len(a)
        for i in range(num):
            smol = i
            for j in range(i + 1, num):
                if a[smol] == None:
                    smol = j
                elif a[j] == None:
                    continue
                elif a[j] < a[smol]:
                    smol = j
            temp = a[i]
            a[i] = a[smol]
            a[smol] = temp
        return a
        




intersection = Intersection(np.array([Road(0), Road(1), Road(2), Road(3)]), time.localtime())#N E S W

numCars = GEN.poisson(LAMBDA)

#FOR TESTING===========================================================================
numCars = 7


print("Number of cars entering the intersection: ", numCars)
threads = deque()
print(time.strftime("%H:%M:%S", time.localtime()))



for i in range(numCars):
    threads.append(threading.Thread(target=intersection.ROADS[GEN.integers(0,4)].put))


for i in range(len(threads)):
    temp = threads.popleft()
    temp.start()
    threads.append(temp)
    

fillLoop = threading.Thread(target=intersection.fill)
fillLoop2 = threading.Thread(target=fillLoop.run)
fillLoop2.start()
threads.append(fillLoop2)

#print("timer moment")
timer = threading.Thread(target=intersection.sleep(PER_SECONDS))
timer.start()
threads.append(timer)



for i in range(len(threads)):
    temp = threads.popleft()
    temp.join()
    #print("chk4")

print(time.strftime("%H:%M:%S", time.localtime()))
#for i in range(4):
#    print(DIRECTIONS[intersection.ROADS[i].road], "Road:\n", intersection.ROADS[i])