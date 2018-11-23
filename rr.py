# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 22:46:35 2018

@author: hagar
"""

import scheduler 
class RR:
    def __init__(self,inputfile,contextswitching,quantum):
        self.Processes = scheduler.ReadFile(inputfile)
        self.contextSwitching = int(1000*contextswitching)
        self.Quantum = int(1000*quantum)
        self.arrived=[]
        self.procNo=[]
        self.startTimes=[]
        self.endTimes=[]
        self.RRAlgorithm()
        scheduler.OutputFile(self.Processes,self.AvgTAT,self.AvgWTAT)
        
            
    def GetArrivedProcesses(self,time): #assume processes are sorted with arrival time
        i=0
        while(i<len(self.Processes) and self.Processes[i].arrivalTime<=time):
            self.arrived.append(self.Processes[i])
            self.Processes.remove(self.Processes[i])
            i+=1
        
    
    def GetStatsData(self):
        return self.procNo ,self.startTimes,self.endTimes
    
    
    def RRAlgorithm(self):
        i=0
        TotalTAT=0
        TotalWTAT=0
        NewProcesses=[]
        self.Processes.sort() # sorted by arrival time
        quant=0
        while (len(self.Processes)>0 or len(self.arrived)>0):
            print("while loop bara")
            self.GetArrivedProcesses(i) #push them at the end
            if len(self.arrived)==0:
                i+=1
                
            else:
                proc=self.arrived[0] #######comment this
                if quant==0:
                    proc=self.arrived[0] #maza lw el burst time zero dan dan dan daaaan !!!
                    self.procNo.append(proc.ID)
                    i+=self.contextSwitching
                    self.startTimes.append(i)
                    proc.remaingBurstTime -=1
                    i+=1
                    quant+=1
                    print("quant =0")
                    
                    
                elif quant==self.Quantum-1: #put process at the end of the queue
                    proc=self.arrived[0] #maza lw el burst time zero dan dan dan daaaan !!!
                    proc.remaingBurstTime -=1
                    i+=1
                    quant=0
                    self.arrived.remove(proc) # here we remove it 
                    #if proc.remaingBurstTime >0:
                    self.arrived.append(proc) #push at the end
                    self.endTimes.append(i)
                    print("quant b quantum")
                else:# if quant!=0 and != Quantum
                    proc.remaingBurstTime -=1
                    i+=1
                    quant+=1
                    print("quantum msh b 0 wla quantum")
                
                print(str(proc.ID)+" "+str(proc.remaingBurstTime))
                    
                if proc.remaingBurstTime ==0: 
                    #process finished
                    proc.WT= i-proc.arrivalTime-proc.burstTime    
                    proc.TAT=proc.burstTime+proc.WT
                    proc.WTAT = float(proc.TAT)/proc.burstTime
                    TotalTAT+= proc.TAT
                    TotalWTAT+=proc.WTAT
                    if quant != 0: self.endTimes.append(i) #process ended with the quantum value msh 3arfa 2keb comment meanigful
                    self.arrived.remove(proc) 
                    NewProcesses.append(proc)
                    quant=0
                    
                                
        self.Processes=NewProcesses
        
        self.AvgTAT= float(TotalTAT)/len(NewProcesses)
        self.AvgWTAT= float(TotalWTAT)/len(NewProcesses)
        
