# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 14:20:08 2023

@author: timot
"""
import numpy


def createFile(name):
    """Creates/Opens a .csv file
    
    Opens a .csv file with the given name. If it doesn't exist, it creates it.
    Returns the opened file. Good coding etiquette closes the returned file object later.
    """
    
    try:
        f = open(f"{name}.csv", "x")
    except Exception:
        f = open(f"{name}.csv", "w")
    f.write("n,Mean,Std. Dev.,Minimum,Q1,Q2,Q3,Maximum\n")
    return f

def writeFormattedTimes(f, times):
    """Writes the formatted times into a .csv file f"""
    
    for i in range(len(times)):
        s = ",".join(map(str, times[i]))
        s += "\n"
        f.write(s)
        
def calculateFromFile(fileName):
    """Calculates statistics from the means from a given .csv file
    Will only work with .csv files that we made, considering it uses only the second column's values
    """
    
    f = open(f"{fileName}.csv", "r")
    means = []
    for l in f:
        t = l.split(",")
        try:
            means.append(float(t[1]))
        except Exception:
            pass
    f.close()
    result = []
    result.append(len(means))
    result.append(numpy.mean(means))
    result.append(numpy.std(means))
    result.append(min(means))
    result.append(numpy.percentile(means,25))
    result.append(numpy.percentile(means,50))
    result.append(numpy.percentile(means,75))
    result.append(max(means))
    return tuple(result)
    