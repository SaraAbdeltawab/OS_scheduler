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
        self.processes = scheduler.ReadFile(inputfile)
        self.contextSwitching = int(1000*contextswitching)
        self.arrived=[]
        self.procNo=[]
        self.startTimes=[]
        self.endTimes=[]
        self.HPFAlgorithm()
        scheduler.OutputFile(self.processes,self.avgTAT,self.avgWTAT)
        
            
    def GetArrivedProcesses(self,time): #assume processes are sorted with arrival time
        i=0
        while(i<len(self.processes) and self.processes[i].arrivalTime<=time):
            self.arrived.append(self.processes[i])
            self.processes.remove(self.processes[i])
            i+=1
        
    
    def GetStatsData(self):
        return self.procNo ,self.startTimes,self.endTimes
    
    
    def HPFAlgorithm(self):
        i=0
        totalTAT=0
        totalWTAT=0
        newProcesses=[]
        self.processes.sort() # sorted by arrival time
        running =False
        while (len(self.processes)>0 or len(self.arrived)>0 or running):
            self.GetArrivedProcesses(i)
            if len(self.arrived)==0 and running ==False:
                i+=1
                
            else:
                if running==False:
                    #take new process
                    self.arrived.sort(key=attrgetter('ID')) # sort on secandry key first 
                    self.arrived.sort(key=attrgetter('priority'),reverse=True) #then on primary key descending
                    proc=self.arrived[0]
                    self.arrived.remove(proc)
                    running=True
                    self.procNo.append(proc.ID)
                    i+=self.contextSwitching
                    self.startTimes.append(i)
                    proc.SetTimes(i) #i is start time
                    proc.remaingBurstTime-=1
                    i+=1
                else: #running=true
                    i+=1
                    proc.remaingBurstTime-=1
               
                if proc.remaingBurstTime==0:
                    totalTAT+= proc.TAT
                    totalWTAT+=proc.WTAT
                    self.endTimes.append(i)
                    running=False
                    newProcesses.append(proc)
        self.processes=newProcesses
        
        self.avgTAT= float(totalTAT)/len(self.processes)
        self.avgWTAT= float(totalWTAT)/len(self.processes)
        
            