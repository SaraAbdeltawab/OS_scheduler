# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 14:10:10 2018

@author: hagar
"""

#import process as pr
from operator import attrgetter

def getArrivedProcesses(processes,time): #assume processes are sorted with arrival time
    arrived=[]
    i=0
    while(i<len(processes) and processes[i].arrivalTime<=time):
        arrived.append(processes[i])
        i+=1
    return arrived
    
    
    


def HPF(processes,contextSwitching):
    i=0
    TotalTAT=0
    TotalWTAT=0
    NewProcesses=[]
    while (len(processes)>0):
        processes.sort() # sorted by arrival time
        if (processes[0].arrivalTime > i):
            i+= (processes[0].arrivalTime-i)
        else:
            arrived= getArrivedProcesses(processes,i)
            arrived.sort(key=attrgetter('ID')) # sort on secandry key first 
            arrived.sort(key=attrgetter('priority'),reverse=True) #then on primary key descending
            proc=arrived[0]
            proc.WT= i-proc.arrivalTime + contextSwitching
            proc.TAT=proc.burstTime+proc.WT
            proc.WTAT = float(proc.TAT)/proc.burstTime
            TotalTAT+= proc.TAT
            TotalWTAT+=proc.WTAT
            i+=proc.burstTime + contextSwitching
            processes.remove(proc)
            NewProcesses.append(proc)
    AvgTAT= float(TotalTAT)/len(NewProcesses)
    AvgWTAT= float(TotalWTAT)/len(NewProcesses)
    return NewProcesses, AvgTAT,AvgWTAT
    
        