# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 10:37:01 2023

@author: timot
"""
import newNewNEWSim as s
import writeAgain as w
import time

def run(num=10,modifier=""):
    """Runs the dualSim num (default 10) times, saves to 4 .csv files
    Data_RedLight_ALL_{modifier}.csv
    Data_RedLight_E_{modifier}.csv
    Data_Julien_ALL_{modifier}.csv
    Data_Julien_E_{modifier}.csv
    
    ALL has waiting times for all cars that pass through the intersection
    E has waiting times for emergency cars specifically
    
    see dualSim in newNewNEWSim.py for details on the simulation
    """
    
    start = time.localtime()#for tracking time elapsed
    
    all_L = w.createFile(f"Data_RedLight_ALL_{modifier}")
    emergency_L = w.createFile(f"Data_RedLight_E_{modifier}")
    all_J = w.createFile(f"Data_Julien_ALL_{modifier}")
    emergency_J = w.createFile(f"Data_Julien_E_{modifier}")
    
    for i in range(num):
        test = s.Intersection()
        T = s.dualSim(test, s.SIM_TIME)
        w.writeFormattedTimes(all_L, s.formatTimes(T[0]))
        w.writeFormattedTimes(emergency_L, s.formatTimes(T[1]))
        w.writeFormattedTimes(all_J, s.formatTimes(T[2]))
        w.writeFormattedTimes(emergency_J, s.formatTimes(T[3]))
        print(f"Progress: {i}/{num}")
    
    #finishing up
    all_L.close()
    emergency_L.close()
    all_J.close()
    emergency_J.close()
    end = time.localtime()
    elapse = time.mktime(end) - time.mktime(start)
    print(f"Time elapsed: {elapse} seconds")
    
    
def calculate(modifier=""):
    """Given a set of .csv files (selected by using the modifier), calculates and returns statistics. Also prints"""
    
    LA = w.calculateFromFile(f"Data_RedLight_ALL_{modifier}")
    LE = w.calculateFromFile(f"Data_RedLight_E_{modifier}")
    JA = w.calculateFromFile(f"Data_Julien_ALL_{modifier}")
    JE = w.calculateFromFile(f"Data_Julien_E_{modifier}")
    t = (LA, LE, JA, JE)
    l = [["n\t\t"],["Mean\t"],["Std. Dev."],["Min\t\t"],["Q1\t\t"],["Q2\t\t"],["Q3\t\t"],["Max\t\t"]]
    for i in t:
        l[0].append(i[0])
        l[1].append((round(i[1],3)))
        l[2].append((round(i[2],3)))
        l[3].append(round(i[3],3))
        l[4].append(round(i[4],3))
        l[5].append(round(i[5],3))
        l[6].append(round(i[6],3))
        l[7].append(round(i[7],3))
    r = []
    for i in l:
        r.append("|\t|".join(map(str, i)))
    print("\n".join(r))
    return t

def calculateToFile(modifier=""):
    """Same as calculate() but writes to a .csv instead of returning"""
    
    LA = w.calculateFromFile(f"Data_RedLight_ALL_{modifier}")
    LE = w.calculateFromFile(f"Data_RedLight_E_{modifier}")
    JA = w.calculateFromFile(f"Data_Julien_ALL_{modifier}")
    JE = w.calculateFromFile(f"Data_Julien_E_{modifier}")
    t = (LA, LE, JA, JE)
    f = w.createFile(f"CombinedData_{modifier}")
    w.writeFormattedTimes(f, t)
    f.close()