# -*- coding: utf-8 -*-

#import process as pr
from operator import attrgetter
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
        newProcessflag = False #run a new process
        i=0
        while(i<len(self.processes) and self.processes[i].arrivalTime <= time):
            self.readyProcesses.append(self.processes[i])
            self.processes.pop(i)
            newProcessflag = True
            i+=1
            
        if newProcessflag:
            self.readyProcesses.sort(key=attrgetter('remaingBurstTime','ID'))
            
        return newProcessflag

    def GetStatsData(self):
        return self.procNo ,self.startTimes,self.endTimes
    
    
    def SRTNAlgorithm(self):
        currentTime=0
        totalTAT=0
        totalWTAT=0
        executedProcesses= [] #all executed processes
        runningProcess = 0
        self.processes.sort() # sorted by arrival time
        running = False # Is there a running process
        
        while (len(self.processes)>0 or len(self.readyProcesses)>0 or running):

            newProcessflag = self.GetArrivedProcesses(currentTime)
            
            if len(self.readyProcesses) == 0 and not running : #no running process or new process arrived
                currentTime+=1
                continue
            
            if not running  or ( running and  newProcessflag and self.readyProcesses[0].remaingBurstTime < runningProcess.remaingBurstTime): #running a new process
                if running:
                    self.endTimes.append(currentTime) #endTime of the previous process
                    self.readyProcesses.append(runningProcess) #return back to ready state
                    self.readyProcesses.sort(key=attrgetter('remaingBurstTime','ID'))
                    
                running = True
                runningProcess = self.readyProcesses[0]
                self.readyProcesses.pop(0) #remove from ready queue
                currentTime += self.contextSwitching #assume there is switching time before running fist process
                self.procNo.append(runningProcess.ID)
                self.startTimes.append(currentTime)
              
            currentTime+=1
            runningProcess.remaingBurstTime -= 1
            
            if runningProcess.remaingBurstTime == 0: #process finished executing
                running = False
                runningProcess.WT = currentTime-runningProcess.arrivalTime-runningProcess.burstTime
                runningProcess.TAT = currentTime-runningProcess.arrivalTime #finish - arrival
                runningProcess.WTAT = float(runningProcess.TAT)/runningProcess.burstTime
                totalTAT+= runningProcess.TAT
                totalWTAT+=runningProcess.WTAT
                self.endTimes.append(currentTime)
                executedProcesses.append(runningProcess)
                                       
            
        self.processes=executedProcesses
        self.avgTAT= float(totalTAT)/len(self.processes)
        self.avgWTAT= float(totalWTAT)/len(self.processes)
        
            