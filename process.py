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
        self.WT=0    #waiting time
        self.TAT=0   #turnaround time
        self.WTAT=0  #weighted turn around time
        
        
    #operator overloading of less than operator    
    def __lt__(self, other):
        return self.arrivalTime < self.arrivalTime
    
    
    
    
    #operator overloading for printing process
    def __str__(self):
        return str(self.arrivalTime) +" "+str(self.burstTime)+ " "+str(self.priority)+"\n"
    