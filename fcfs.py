# -*- coding: utf-8 -*-

from operator import attrgetter
import scheduler 

class FCFS:
    def __init__(self,inputfile,contextswitching):
        self.readyProcesses = [] #sorted list of all processes in ready state
        self.processes = scheduler.ReadFile(inputfile)
        self.contextSwitching = int(1000*contextswitching)
        self.procNo=[]
        self.startTimes=[]
        self.endTimes=[]
        self.FCFSAlgorithm()
        scheduler.OutputFile(self.processes,self.avgTAT,self.avgWTAT)
        
            
    def GetArrivedProcesses(self,time):
        self.processes.sort() # sorted by arrival time
        i=0
        while(i<len(self.processes) and self.processes[i].arrivalTime <= time):
            self.readyProcesses.append(self.processes[i])
            self.processes.pop(i) 
            i+=1
        
    def GetStatsData(self):
        return self.procNo ,self.startTimes,self.endTimes
    
    def FCFSAlgorithm(self):
        currentTime=0
        totalTAT=0
        totalWTAT=0
        executedProcesses= [] #all executed processes
        while (len(self.processes)>0 or len(self.readyProcesses)>0):
            self.GetArrivedProcesses(currentTime) #after each process check the arrival of new process 
            
            if len(self.readyProcesses) == 0: #no new process arrived
                currentTime+=1
                continue
            
            #self.readyProcesses.sort(key=attrgetter('arrivalTime','ID')) #sort by arrivalTime and ID
            currentProcess = self.readyProcesses[0]
            currentTime += self.contextSwitching #assume there is switching time before running fist process
            self.procNo.append(currentProcess.ID)
            self.startTimes.append(currentTime)
            currentProcess.WT = currentTime-currentProcess.arrivalTime    #start - arrival
            currentProcess.TAT = currentProcess.burstTime+currentProcess.WT
            currentProcess.WTAT = float(currentProcess.TAT)/currentProcess.burstTime
            totalTAT+= currentProcess.TAT
            totalWTAT+= currentProcess.WTAT
            currentTime+= currentProcess.burstTime 
            self.endTimes.append(currentTime) #processes finished execusion
            executedProcesses.append(currentProcess)
            self.readyProcesses.pop(0) #remove from ready queue
            
        self.processes=executedProcesses
        self.avgTAT= float(totalTAT)/len(self.processes)
        self.avgWTAT= float(totalWTAT)/len(self.processes)
        
            