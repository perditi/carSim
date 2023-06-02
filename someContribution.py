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
#returns array of 4 numbers, (N E S W) because it's a 4-way intersection

PER_SECONDS = 30#say the period of time is 30 seconds

class Car:
    def __init__(self):
        self.direction = DIRECTIONS[GEN.integers(0,3)]#random direction
        self.arrivalTime = time.process_time_ns()
    def __str__(self):
        return f"Turning {self.direction}, arrived at {self.arrivalTime}."

class Road:
    def __init__(self):
        self.q = q.Queue()
    def put(self, n):
        for i in range(n):
            self.q.put(Car())
            time.sleep(PER_SECONDS/n)
    def pop(self):
        self.q.pop()
    def __str__(self):
        for i in self.q:
            return None
            

ROADS = np.array([Road(), Road(), Road(), Road()])#N E S W

cars = np.array([None, None], dtype=Car)
cars[0] = Car()
cars[1] = Car()
print(cars[0])
print(cars[1])
