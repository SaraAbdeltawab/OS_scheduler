# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 20:04:38 2018

@author: hagar
"""

class Process:
    def __init__(self,no,arrivaltime,bursttime,priority):
        self.ID=no
        self.arrivalTime=arrivaltime
        self.burstTime=bursttime
        self.priority=priority
        self.WT=0    #waiting time                 #start-Arrival
        self.TAT=0   #turnaround time              #finish - arrival =burst+waiting
        self.WTAT=0  #weighted turnaround time     #TAT/burst
        
        
    #operator overloading of less than operator    
    def __lt__(self, other):
        return self.arrivalTime < self.arrivalTime
    
    
    
    
    #operator overloading for printing process
   def __str__(self):
       return str(self.arrivalTime) +" "+str(self.burstTime)+ " "+str(self.priority)+"\n"
    
    # def __str__(self):
    #     return str(self.arrivalTime) +" "+str(self.burstTime)+ " "+str(self.priority)+" "+str(self.WT)+" "+str(self.TAT)+" "+str(self.WTAT)+"\n"
    