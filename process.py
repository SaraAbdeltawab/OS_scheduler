# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 20:04:38 2018

@author: hagar
"""

class Process:
    def __init__(self,arrivaltime,bursttime,priority):
        self.arrivalTime=arrivaltime
        self.burstTime=bursttime
        self.priority=priority
        
        
    #operator overloading of less than operator    
    def __lt__(self, other):
        pass
    
    #operator overloading for printing symbol
    def __str__(self):
        return str(self.arrivalTime) +" "+str(self.burstTime)+ " "+str(self.priority)+"\n"
    