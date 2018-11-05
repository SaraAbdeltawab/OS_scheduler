# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 14:10:10 2018

@author: hagar
"""

#import process as pr
from operator import attrgetter
import scheduler 
class HPF:
    def __init__(self,inputfile,contextswitching):
        self.Processes = scheduler.ReadFile(inputfile)
        self.contextSwitching = int(1000*contextswitching)
        self.procNo=[]
        self.startTimes=[]
        self.endTimes=[]
        self.HPFAlgorithm()
        scheduler.OutputFile(self.Processes,self.AvgTAT,self.AvgWTAT)
        
            
    def GetArrivedProcesses(self,time): #assume processes are sorted with arrival time
        arrived=[]
        i=0
        while(i<len(self.Processes) and self.Processes[i].arrivalTime<=time):
            arrived.append(self.Processes[i])
            i+=1
        return arrived
        
    
    def GetStatsData(self):
        return self.procNo ,self.startTimes,self.endTimes
    
    
    def HPFAlgorithm(self):
        i=0
        TotalTAT=0
        TotalWTAT=0
        NewProcesses=[]
        while (len(self.Processes)>0):
            self.Processes.sort() # sorted by arrival time
            if (self.Processes[0].arrivalTime > i):
                i+= (self.Processes[0].arrivalTime-i)
            else:
                arrived= self.GetArrivedProcesses(i)
                arrived.sort(key=attrgetter('ID')) # sort on secandry key first 
                arrived.sort(key=attrgetter('priority'),reverse=True) #then on primary key descending
                proc=arrived[0]
                self.procNo.append(proc.ID)
                i+=self.contextSwitching
                self.startTimes.append(i)
                proc.WT= i-proc.arrivalTime    #start - arrival
                proc.TAT=proc.burstTime+proc.WT
                proc.WTAT = float(proc.TAT)/proc.burstTime
                TotalTAT+= proc.TAT
                TotalWTAT+=proc.WTAT
                i+=proc.burstTime
                self.endTimes.append(i)
                self.Processes.remove(proc)
                NewProcesses.append(proc)
        self.Processes=NewProcesses
        
        self.AvgTAT= float(TotalTAT)/len(NewProcesses)
        self.AvgWTAT= float(TotalWTAT)/len(NewProcesses)
        
            