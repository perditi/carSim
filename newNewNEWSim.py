# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 00:25:05 2023

@author: timot
"""
import numpy as np
from copy import deepcopy
"""
A slightly less simple example,
                                    DIRECTION 0
                         |                     |          |
                         |          |          |          |
                         |                     |          |
                         |          |          |          |
                         |                     |          |
                         |    |     |    |     |    /\    |
                         |    |          |     |    |     |
                         |    |     |    |     |    |     |
                         |    |          |     |    |     |
                         |  <-/     |    \->   |    |     |
                         |                     |          |
                         |          |          |          |
DIRECTION 2              |                     |          |             DIRECTION 1
-------------------------|          |          |          |------------------------
                                                              /\
                 <-------                                  <--------

-------------------------                                  ------------------------
                      /\                                   ]]]]]]]]]]]]]]]]]]]]]]]]
                ______/                                    ]]]]]]]]]]]]]]]]]]]]]]]]
                                                           ]]]]]]]]]]]]]]]]]]]]]]]]
-  -  -  -  -  -  -  -  -                                  ------------------------

                 -------->                                 -------->

-----------------------------------------------------------------------------------
Say there's no U-turns allowed (i.e. a car can't go to the same direction it came from)
L1 = 0 -> 1
L2 = 0 -> 2
L3 = 1 -> 0
L4 = 1 -> 2
L5 = 2 -> 0
L6 = 2 -> 1

[L1, L2, L3]
[L2, L5, L6]
[L2, L3, L6]
[L4, L6]

light 0: direction 0 goes, direction 1 turns right
light 1: direction 1 goes and direction 2 goes straight
(direction 2 turns left if no cars, direction 0 turns right if no cars)
light 2: direction 2 goes straight and left, direction 0 turns right
(direction 1 turns right if no cars)

[L2, L1, L3/L4, L6, L5]

"""
#all possible paths
PATHS = ([0,1,"L1"],[0,2,"L2"],[1,0,"L3"],[1,2,"L4"],[2,0,"L5"],[2,1,"L6"])
#maximal concurrent lanes
CONC_LANES = (["L1","L2","L3"],["L2","L3","L6"],["L2","L5","L6"],["L4","L6"])

#CONSTANT VARIABLES, CHANGE AS NEEDED -- ALL TIMES IN SECONDS
LIGHT_DURATION = 30#for the red light simulation, how long until it changes
SIM_TIME = 10800#how long the simulation runs for
LAMBDA = 4#average number of cars per period of time
PER_SECONDS = 12#the period of time
PASS_TIME = 3#how long it takes for a car to enter and leave the intersection
UPPER_BOUND_TIME = 60#if a car has been waiting for longer than this, it gets more priority
EMERGENCY_CHANCE = 0.01#1% chance of emergency car




GEN = np.random.default_rng(None)#use GEN.poisson(1)
EMERGENCY_WEIGHT = 1000000000
PRIORITY_WEIGHT = 1000

class Car:
    #if a road/destination isn't specified, picks random ones
    def __init__(self, road=None, destination=None, emergency=False):
        """A car is initialized with an entry road and a destination road (0-4).
        If either one is not given, it is randomly chosen from a uniform distribution.
        A car cannot go to the same road it came from.
        Additionally, a car can be an emergency car. If unspecified, it is default NOT an emergency car.

        A car has a waitTime variable, which increases during the simulation to track its waiting time.
        A car has a weight variable, which may vary depending on its waiting time during a simulation.
        Emergency vehicles have very large weight.
        The weight is used to determine priority in our experimental algorithm.
        """
        if (road == None):
            self.road = GEN.integers(0,3)
        else:
            self.road = road
        if (destination == None):
            self.destination = self.road
            while (self.destination == self.road):
                self.destination = GEN.integers(0,3)
        else:
            self.destination = destination
        self.lane = 0
        for i in PATHS:
            if self.road == i[0]:
                if self.destination == i[1]:
                    self.lane = i[2]
                    break
        self.waitTime = 0
        if emergency:
            self.weight = EMERGENCY_WEIGHT
        else: self.weight = 1
                
    def __str__(self):
        """Returns the car's lane of travel, represented as L#"""
        return self.lane
        
class Intersection:
    
    def __init__(self, r=None):
        """An intersection can be initialized with a pre-existing road,
        otherwise creates a blank one.
        This simulation has 5 roads, one for each entry lane (see diagram above).
        The roads have a status, either "WAITING" or "GOING".
        """
        if r == None:
            self.roads = ([],[],[],[],[])
            self.weight = [0,0,0,0,0]
        else:
            self.roads = deepcopy(r)
            self.weight = [0,0,0,0,0]
            self.updateWeight()
        self.status = ["WAITING", "WAITING", "WAITING", "WAITING", "WAITING"]
        
    def peekRoad(self, road):
        """Peeks at the first car in a given road, returns it (or None, if the road is empty)."""
        if len(self.roads[road]) == 0:
            return None
        else:
            return self.roads[road][0]
    
    def carIn(self, road=None, destination=None, emergency=False):
        """Inserts a car into a road in the intersection. Also returns it"""
        tempCar = Car(road, destination, emergency)#if road, destination == None, randomizes
        i = tempCar.road
        if i == 0:
            if tempCar.destination == 1:
                i = 1
            else:
                i = 0
        elif i == 1:
            i = 2
        elif i == 2:
            if tempCar.destination == 0:
                i = 4
            else:
                i = 3
        self.roads[i].append(tempCar)
        self.updateWeight()#see updateWeight
        return tempCar
    
    def carOut(self, p):
        """Removes a car from a given road and returns it"""
        temp = self.roads[p].pop(0)
        self.updateWeight()#see updateWeight
        return temp
        
    def updateWeight(self):
        """Goes through each road and recalculates the weights for each road
        
        If a car has been waiting longer than UPPER_BOUND_TIME seconds, and is not an emergency vehicle,
        its weight is adjusted to have more priority
        """
        for i in range(5):
            self.weight[i] = 0
            for j in range(len(self.roads[i])):
                if self.roads[i][j].waitTime > UPPER_BOUND_TIME and self.roads[i][j].weight < EMERGENCY_WEIGHT:#if a car has been waiting too long and isn't an emergency vehicle
                    self.roads[i][j].weight = PRIORITY_WEIGHT + self.roads[i][j].waitTime
                self.weight[i] += self.roads[i][j].weight
            
    def wait(self, t):
        """Roads that have status "WAITING" have their cars' waiting times increased by t seconds"""
        for i in range(len(self.roads)):
            if self.status[i] == "WAITING":
                for j in self.roads[i]:
                        j.waitTime += t
            
    def stringHelper(self, ind):
        """Helper method for formatting the string representation"""
        r = ""
        for i in range(len(self.roads[ind])):
            r += self.roads[ind][i].__str__()
            if i < len(self.roads[ind])-1:
                r += ","
        return r
        
    def __str__(self):
        """Returns all roads represented as a tuple of lists. Cars represented by their lanes (L#)"""
        r0 = self.stringHelper(0)
        r1 = self.stringHelper(1)
        r2 = self.stringHelper(2)
        r3 = self.stringHelper(3)
        r4 = self.stringHelper(4)
        return f"([{r0}],[{r1}],[{r2}],[{r3}],[{r4}])"
            
def findBest(intersection):
    """Based on our experimental algorithm, derives the optimal combination of cars to exit the intersection"""
    weights = []
    first = []
    for i in range(len(intersection.roads)):
        weights.append(0)
        first.append(intersection.peekRoad(i))
    for i in range(len(CONC_LANES)):#look at a set of concurrent lanes
        w = 0
        for j in range(len(first)):#take each next car to go
            if first[j] != None:
                #print(first[j])
                if first[j].lane in CONC_LANES[i]:
                    w += intersection.weight[j]#if the car is in that set, add the weight of the road to the weight of the concurrency set
        #do this for all 4 concurrency sets
        weights[i] = w
        #print(w)
    #print(weights)
    return CONC_LANES[weights.index(max(weights))]
    #afterwards, compare all 4 weights do the one with the most weight

def newLight(i=None):#2 is left turn light
    """Goes through the light cycle very simply
    
    0 -> 1 -> 2 -> 0... etc.
    """
    if i == None:
        return GEN.integers(0,3)#if unspecified initially, picks a random state
    elif i == 0:
        return 1
    elif i == 1:
        return 2
    elif i == 2:
        return 0
    
def dualSim(intersection, simTime=0, waver=False, differ=False, verbose=False):
    """Runs two simulations on a given intersection: a red light simulation and our experimental algorithm.
    
    simTime is how long the simulation runs, if it's set to 0 then it stops as soon as the intersection is empty
    waver is True or False. If True, then LAMBDA changes throughout the simulation (see dualRandInsert)
    differ is True or False. If True, then light state 1 lasts twice as long
    verbose is True or False. If True, then more detailed progress print statements are included
    (Note: verbose clogs up the console a lot, use mainly for debugging and testing)
    """
    globalTime = 0#tracks total simulation time
    intersectionL = Intersection(intersection.roads)
    intersectionJ = Intersection(intersection.roads)
    passageOfTime = 0
    light = 0
    timesJ_ALL = ([],[],[],[],[])
    timesJ_E = ([],[],[],[],[])
    timesL_ALL = ([],[],[],[],[])
    timesL_E = ([],[],[],[],[])
    #L is for the light sim, J is for the experimental sim
    while (simTime <= 0 and (intersectionL.roads != ([],[],[],[],[]) or intersectionJ.roads != ([],[],[],[],[]))) or (simTime > 0 and globalTime <= simTime):
        #get the first cars in each road
        firstJ = [intersectionJ.peekRoad(0), intersectionJ.peekRoad(1), intersectionJ.peekRoad(2), intersectionJ.peekRoad(3), intersectionJ.peekRoad(4)]
        firstL = [intersectionL.peekRoad(0), intersectionL.peekRoad(1), intersectionL.peekRoad(2), intersectionL.peekRoad(3), intersectionL.peekRoad(4)]
        
        #gets road indexes for what can go, saves into bestJ
        tempBest = findBest(intersectionJ)
        bestJ = []
        for i in range(len(firstJ)):
            if firstJ[i] != None and firstJ[i].lane in tempBest:
                bestJ.append(i)
        for i in bestJ:
            if firstJ[i] == None:
                bestJ.remove(i)#gets rid of roads without cars
        
        #this is poorly written but i can't do it better
        #literally checks what light state it is and sees what can go
        #saves road indexes into bestL
        if light == 0:
            bestL = [0,1]
            if firstL[0] == None:
                bestL = bestL[1:]
            if firstL[1] == None:
                bestL = bestL[0:1]
        elif light == 1:
            bestL = []
            if firstL[2] != None:
                bestL.append(2)
            if firstL[3] != None:
                bestL.append(3)
            if firstL[0] != None:
                if firstL[2] == None or firstL[2].lane == "L3": bestL.append(0)
            if 2 not in bestL:
                if firstL[4] != None:
                    bestL.append(4)
        elif light == 2:
            bestL = []
            if firstL[3] != None:
                bestL.append(3)
            if firstL[4] != None:
                bestL.append(4)
            if firstL[0] != None:
                bestL.append(0)
            if bestL == []:
                if firstL[2] != None and firstL[2].lane == "L3":
                    bestL.append(2)
        
        #if a car is supposed to go, that lane is marked "GOING", otherwise "WAITING"
        for i in (0,1,2,3,4):
            if i in bestJ:
                intersectionJ.status[i] = "GOING"
            else:
                intersectionJ.status[i] = "WAITING"
            if i in bestL:
                intersectionL.status[i] = "GOING"
            else:
                intersectionL.status[i] = "WAITING"
        printStrJ = "J\n"
        printStrL = "L\n"
        
        #goes through each best and removes cars from those roads
        for i in bestJ:
            temp = intersectionJ.carOut(i)
            timesJ_ALL[i].append(temp.waitTime)
            if temp.weight == EMERGENCY_WEIGHT:
                timesJ_E[i].append(temp.waitTime)
            printStrJ += temp.__str__()
        for i in bestL:
            if intersectionL.roads[i] != []:
                temp = intersectionL.carOut(i)
                timesL_ALL[i].append(temp.waitTime)
                if temp.weight == EMERGENCY_WEIGHT:
                    timesL_E[i].append(temp.waitTime)
                printStrL += temp.__str__()
        #checking in, these print statements (needs verbose)
        if verbose and printStrL != "L\n": print(printStrL)
        if verbose and printStrJ != "J\n": print(printStrJ)
        
        #the waiting stuff
        intersectionJ.wait(PASS_TIME)
        intersectionL.wait(PASS_TIME)
        globalTime += PASS_TIME
        if globalTime % LIGHT_DURATION == 0:#change light if it's been enough time
            if differ and light == 1:
                if globalTime % (LIGHT_DURATION*2) == 0:
                    light = newLight(light)
            else:
                light = newLight(light)
        if simTime > 0 and (globalTime // PER_SECONDS > passageOfTime):
            for i in range((globalTime//PER_SECONDS) - passageOfTime):
                #if enough time has passed, it's time to add cars
                dualRandInsert(intersectionJ,intersectionL,waver,globalTime,simTime,verbose)
            passageOfTime = globalTime // PER_SECONDS
            #checking in, these print statments (needs verbose)
            if verbose: print(f"L:{intersectionL}")
            if verbose: print(f"J:{intersectionJ}")
    
    #returns 4 tuples in a tuple
    #each tuple is the waiting times for each simulation
    #example inner tuple: ([road 0 times], [road 1 times], [road 2 times], [road 3 times], [road 4 times])
    return (timesL_ALL, timesL_E, timesJ_ALL, timesJ_E)

def dualRandInsert(i1, i2, waver, t, sim, verbose=False):
    """Adds cars to the intersection based on a Poisson distribution (see LAMBDA, PER_SECONDS)
    
    Picks random cars, adds the SAME car to both simulations
    Also randomly makes cars emergency (see EMERGENCY_CHANCE)
    """
    if waver:
        if t < sim/4:
            use = LAMBDA/2
        elif t >= sim/4 and t < sim/3:
            use = LAMBDA
        elif t >= sim/3 and t < sim/2:
            use = LAMBDA*2
        else:
            use = LAMBDA
    else:
        use = LAMBDA
    n = GEN.poisson(use)
    for i in range(n):
        p = GEN.binomial(1,EMERGENCY_CHANCE)
        if p == 1:        
            temp = i1.carIn(emergency=True)
            i2.carIn(temp.road, temp.destination, emergency=True)
        else:
            temp = i1.carIn()
            i2.carIn(temp.road, temp.destination)
    if verbose: print(f"Adding {n} car(s)...")
    
def formatTimes(times):
    """Calculates statistics from given waiting times (like those you'd get after running a simulation)
    
    Returns the statistics in a tuple of lists
    """
    result = ([],[],[],[],[])
    for t in range(len(times)):
        result[t].append(len(times[t]))
        result[t].append(np.mean(times[t]))
        result[t].append(np.std(times[t]))
        result[t].append(min(times[t]))
        result[t].append(np.percentile(times[t], 25))
        result[t].append(np.percentile(times[t], 50))
        result[t].append(np.percentile(times[t], 75))
        result[t].append(max(times[t]))
    return result
    
def printTimes(t):
    """Formats times, then prints to console"""
    times = formatTimes(t)
    printStr = "n\tMean\tStd. Dev.\tMin\tQ1\t\tQ2\t\tQ3\t\tMax\n"
    for i in range(len(times)):
        n = times[i][0]
        mean = round(times[i][1],3)
        std = round(times[i][2],3)
        min = times[i][3]
        Q1 = round(times[i][4],3)
        Q2 = round(times[i][5],3)
        Q3 = round(times[i][6],3)
        max = times[i][7]
        printStr += f"{n}\t{mean}\t{std}\t\t{min}\t{Q1}\t\t{Q2}\t\t{Q3}\t\t{max}\n"
    print(printStr)
    
    
    
    
    
def testInt():
    """Small test, for debugging purposes"""
    test = Intersection()
    test.carIn(0,2)
    test.carIn(1,0)
    test.carIn(2,1)
    test.carIn(0,1)
    return test

def testInt25():
    """Bigger test, for debugging purposes"""
    test = Intersection()
    test.carIn(0,2)
    for i in range(3): test.carIn(0,1)
    test.carIn(0,2)
    test.carIn(0,1)
    test.carIn(0,2)
    for i in range(2): test.carIn(0,1)
    for i in range(2): test.carIn(1,2)
    for i in range(2): test.carIn(1,0)
    for i in range(3): test.carIn(1,2)
    test.carIn(1,0)
    test.carIn(1,2)
    test.carIn(2,0)
    for i in range(2): test.carIn(2,1)
    test.carIn(2,0)
    for i in range(2): test.carIn(2,1)
    test.carIn(2,0)
    return test
