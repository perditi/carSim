# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 10:37:01 2023

@author: timot
"""

import numpy as np
import queue as q

DIRECTIONS = np.array(["left", "straight", "right"])

class Car:
    def __init__(self):
        
        self.direction = DIRECTIONS[0]
        print(self.direction)


class Road:
    def __init__(self):
        self.q = q.Queue()
    def put(self, n):
        for i in range(n):
            self.q.put(Car())


gen = np.random.default_rng(None)#use gen.poisson(1)
#lambda is average number of cars per period of time -- how long do i want?? rn set to 1
#five seconds isn't bad but how fast are these fucking cars going :skull:
#returns array of 4 numbers, (N E S W) because it's a 4-way intersection


