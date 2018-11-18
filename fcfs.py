# -*- coding: utf-8 -*-

#import process as pr
from operator import attrgetter
import scheduler 
class FCFS:
    def __init__(self,inputfile,contextswitching):
        self.processes = scheduler.ReadFile(inputfile)
        self.contextSwitching = int(1000*contextswitching)
        self.procNo=[]
        self.startTimes=[]
        self.endTimes=[]
        self.FCFSAlgorithm()
        scheduler.OutputFile(self.Processes,self.AvgTAT,self.AvgWTAT)
        
            
    def GetArrivedProcesses(self,time): #assume processes are sorted with arrival time
        self.processes.sort() # sorted by arrival time
        arrived=[]
        i=0
        while(i<len(self.processes) and self.processes[i].arrivalTime<=time):
            arrived.append(self.processes[i])
            i+=1
        return arrived
        
    
    def GetStatsData(self):
        return self.procNo ,self.startTimes,self.endTimes
    
    
    def FCFSAlgorithm(self):
        currentTime=0
        totalTAT=0
        totalWTAT=0
        arrivedProcesses=[] #sorted list of all processes arrived at time <= currentTime
        tempProcesses=[]
        while (len(self.processes)>0):
            arrived = self.GetArrivedProcesses(currentTime)
            arrivedProcesses.extend(arrived) 
            arrived.sort(key=attrgetter('ID')) # sort on secandry key first 
            arrived.sort(key=attrgetter('arrivalTime')) # 23ml l sort marra wa7da ??
            currentProcess = arrived[0]
            self.procNo.append(currentProcess.ID)
            currentTime += self.contextSwitching #assume there is switching time before running fist process
            self.startTimes.append(currentTime)
            currentProcess.WT = currentTime-currentProcess.arrivalTime    #start - arrival
            currentProcess.TAT = currentProcess.burstTime+currentProcess.WT
            currentProcess.WTAT = float(currentProcess.TAT)/currentProcess.burstTime
            totalTAT+= currentProcess.TAT
            totalWTAT+= currentProcess.WTAT
            currentTime+= currentProcess.burstTime
            self.endTimes.append(currentTime)
            self.processes.remove(currentProcess)
            tempProcesses.append(currentProcess)
            
        self.processes=tempProcesses
        self.avgTAT= float(totalTAT)/len(self.processes)
        self.avgWTAT= float(totalWTAT)/len(self.processes)
        
            