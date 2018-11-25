# -*- coding: utf-8 -*-

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
        self.processes.sort() # sorted by arrival time
        running = False # Is there a running process
        while (len(self.processes)>0 or len(self.readyProcesses)>0 or running):
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
            print(runningProcess.burstTime)
            if runningProcess.burstTime == 0:
                self.endTimes.append(currentTime) #process finished execusion
                executedProcesses.append(runningProcess)
                running = False
        
        self.processes=executedProcesses
        self.avgTAT= float(totalTAT)/len(self.processes)
        self.avgWTAT= float(totalWTAT)/len(self.processes)
        
            