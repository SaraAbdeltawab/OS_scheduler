# -*- coding: utf-8 -*-

#import process as pr
from operator import attrgetter
import process
import scheduler 

class SRTN:
    def __init__(self,inputfile,contextswitching):
        self.readyProcesses = [] #sorted list of all processes in ready state
        self.processes = scheduler.ReadFile(inputfile)
        self.contextSwitching = int(1000*contextswitching)
        self.procNo=[]
        self.startTimes=[]
        self.endTimes=[]
        self.SRTNAlgorithm()
        scheduler.OutputFile(self.processes,self.avgTAT,self.avgWTAT)
        
    def GetArrivedProcesses(self, time):
        self.processes.sort() # sorted by arrival time
        i=0
        while(i<len(self.processes) and self.processes[i].arrivalTime <= time):
            self.readyProcesses.append(self.processes[i])
            self.processes.pop(i) 
            i+=1

    def GetStatsData(self):
        return self.procNo ,self.startTimes,self.endTimes
    
    
    def SRTNAlgorithm(self):
        currentTime=0
        totalTAT=0
        totalWTAT=0
        executedProcesses= [] #all executed processes
        previousProcess = process.Process(-1,0,0,0)
        currentProcess = 0
        while (len(self.processes)>0 or len(self.readyProcesses)>0):
            
            self.GetArrivedProcesses(currentTime)
            
            if len(self.readyProcesses) == 0: #no new process arrived
                currentTime+=1
                continue
            self.readyProcesses.sort(key=attrgetter('remaingBurstTime','ID'))
            currentProcess = self.readyProcesses[0]
            
            if previousProcess.ID != currentProcess.ID: #running a new process
                currentTime += self.contextSwitching #assume there is switching time before running fist process
                self.procNo.append(currentProcess.ID)
                self.startTimes.append(currentTime)
                if previousProcess.ID != -1: self.endTimes.append(currentTime) #endTime of the previous process
                
            currentTime+=1
            self.readyProcesses[0].remaingBurstTime -= 1
            currentProcess = self.readyProcesses[0]
            
            if currentProcess.remaingBurstTime == 0: #process finished executing
                currentProcess.WT = currentTime-currentProcess.arrivalTime-currentProcess.burstTime
                currentProcess.TAT = currentTime-currentProcess.arrivalTime #finish - arrival
                currentProcess.WTAT = float(currentProcess.TAT)/currentProcess.burstTime
                totalTAT+= currentProcess.TAT
                totalWTAT+=currentProcess.WTAT
    
                executedProcesses.append(currentProcess)
                self.readyProcesses.pop(0) #remove from ready queue
                                       
            previousProcess = currentProcess
            
        self.endTimes.append(currentTime) #end time of last process
        self.processes=executedProcesses
        self.avgTAT= float(totalTAT)/len(self.processes)
        self.avgWTAT= float(totalWTAT)/len(self.processes)
        
            