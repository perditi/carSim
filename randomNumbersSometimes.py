# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 01:18:15 2023

@author: timot
"""

"""UNUSED IN THIS VERSION, KEEPING IT HERE FOR RECORDS

associates certain outcomes with certain probabilities
"""
import random


POSSIBILITIES = ((3,0.70),(5,0.20),(10,0.10))#assume percentages add up to 1
#if you want to add an outcome, add a (x,y) to this list, where
#x is the outcome you want, and y is its probability (between 0 and 1)
POSSIBILITIES = ((0,0.50),(1,0.20),(2,0.30))


BOUNDS = []
track = 0.0
for i in range(len(POSSIBILITIES)-1):
    track += POSSIBILITIES[i][1]
    BOUNDS.append(track)
BOUNDS.append(1.0)

def get():
    """gets a random outcome using the distribution as stated above"""
    num = random.random()
    checks = []
    for i in range(len(BOUNDS)):
        checks.append(num <= BOUNDS[i])
    ind = checks.index(True)
    return POSSIBILITIES[ind][0]



def test(trials):
    """will get a random number 'trials' times, record it and will give the experimental
    probability of each numbers' occurence
    """
    count = []
    for i in range(len(POSSIBILITIES)):
        count.append(0)
    for i in range(trials):
        r = get()
        for j in range(len(POSSIBILITIES)):
            if r == POSSIBILITIES[j][0]:
                count[j] += 1
    p = []
    for i in count:
        p.append(round(float(i)*100/trials,3))
    r = ""
    for i in range(len(POSSIBILITIES)):
        r += f"{POSSIBILITIES[i][0]} appeared {p[i]}% of the time"
        if i < len(POSSIBILITIES) - 1:
            r += "\n"
    print(r)