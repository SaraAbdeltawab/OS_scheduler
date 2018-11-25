# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 22:46:35 2018

@author: hagar
"""

import scheduler
class RR:
    def __init__(self,inputfile,contextswitching,quantum):
        self.processes = scheduler.ReadFile(inputfile)
        self.contextSwitching = int(1000*contextswitching)
        self.quantum = int(1000*quantum)
        self.arrived=[]
        self.procNo=[]
        self.startTimes=[]
        self.endTimes=[]
        self.RRAlgorithm()
        scheduler.OutputFile(self.processes,self.avgTAT,self.avgWTAT)
        
            
    def GetArrivedProcesses(self,time): #assume processes are sorted with arrival time
        while(len(self.processes)>0 and self.processes[0].arrivalTime<=time):
            self.arrived.append(self.processes[0])
            self.processes.remove(self.processes[0])
        
        
    
    def GetStatsData(self):
        return self.procNo ,self.startTimes,self.endTimes
    
    
    def RRAlgorithm(self):
        i=0
        totalTAT=0
        totalWTAT=0
        newProcesses=[]
        self.processes.sort()
        running =False
        quant=0
        while (len(self.processes)>0 or len(self.arrived)>0 or running):
            self.GetArrivedProcesses(i) #push them at the end
            if len(self.arrived)==0 and running ==False:
                i+=1
                
            else:
                if running==False:
                    #take a process from ready queue
                    proc=self.arrived[0] #maza lw el burst time zero dan dan dan daaaan !!!
                    self.arrived.remove(proc)
                    self.procNo.append(proc.ID)
                    i+=self.contextSwitching
                    self.startTimes.append(i)
                    proc.remaingBurstTime -=1
                    i+=1
                    quant+=1
                    running=True
                else: #running true   
                    proc.remaingBurstTime -=1
                    i+=1
                    quant+=1
                    
                if quant==self.quantum: #put process at the end of the queue
                    quant=0
                    running=False
                    if proc.remaingBurstTime >0 and len(self.arrived)==0:
                        #keep running but with new quantum 
                        #don't put in the queue to save context switching
                        running=True
                    elif proc.remaingBurstTime >0:
                        self.arrived.append(proc) #push at the end
                        self.endTimes.append(i)
                    # if it is zero then  
                
                if proc.remaingBurstTime ==0: 
                    #process finished
                    start=i-proc.burstTime
                    proc.SetTimes(start)
                    totalTAT+= proc.TAT
                    totalWTAT+=proc.WTAT
                    self.endTimes.append(i)
                    newProcesses.append(proc)
                    quant=0
                    running=False
                                
        self.processes=newProcesses
        
        self.avgTAT= float(totalTAT)/len(self.processes)
        self.avgWTAT= float(totalWTAT)/len(self.processes)
        
