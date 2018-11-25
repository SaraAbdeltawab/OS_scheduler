# -*- coding: utf-8 -*-

import scheduler 
from operator import attrgetter
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

        while(self.processes and self.processes[0].arrivalTime <= time):
            self.readyProcesses.append(self.processes[0])
            self.processes.pop(0)
        
    def GetStatsData(self):
        return self.procNo ,self.startTimes,self.endTimes
    
    def FCFSAlgorithm(self):
        currentTime=0
        totalTAT=0
        totalWTAT=0
        executedProcesses= [] #all executed processes
        self.processes.sort() # sorted by arrival time #ID??
        #for i in  range (len(self.processes)):
        #    print(self.processes[i].arrivalTime)
        #print(len(self.processes))
        running = False # Is there a running process
        while (self.processes or self.readyProcesses or running):
            self.GetArrivedProcesses(currentTime) #check the arrival of new process 
            
            if len(self.readyProcesses) == 0 and not running: #no running process or new process arrived
                currentTime+=1
                continue
            
            if not running:
                runningProcess = self.readyProcesses[0]
                running = True
                self.readyProcesses.pop(0) #remove from ready queue
                currentTime += self.contextSwitching #assume there is a full switching time before running fist process
                self.procNo.append(runningProcess.ID)
                self.startTimes.append(currentTime)
                runningProcess.SetTimes(currentTime) #set WT,TAT, WTAT, 
                totalTAT+= runningProcess.TAT
                totalWTAT+= runningProcess.WTAT
                
            runningProcess.burstTime -= 1
            currentTime+=1
            if runningProcess.burstTime == 0:
                self.endTimes.append(currentTime) #process finished execusion
                executedProcesses.append(runningProcess)
                running = False
        
        self.processes=executedProcesses
        self.avgTAT= float(totalTAT)/len(self.processes)
        self.avgWTAT= float(totalWTAT)/len(self.processes)
        
            