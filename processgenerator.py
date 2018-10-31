# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 20:16:25 2018

@author: hagar
"""
import numpy as np

import process

class Generator: 
    def __init__(self,inputfile,outputfile):
        self.inputFile=inputfile
        self.outputFile=outputfile
        self.n=0
        # normal distribution 1
        self.mio1=0
        self.sd1=0
        # normal ditribution 2
        self.mio2=0
        self.sd2=0
        #poisson distribution 
        self.lamda=0
        self.Processes=[]
        self.ReadFile()
        self.GenerateProcesses()
        self.OutputFile()
        
        
        
        
    def ReadFile(self):
        with open (self.inputFile,'r') as rf:
            fcontents= rf.read()
            #print(fcontents)
            self.n,n1,n2,self.lamda = fcontents.split("\n")
            self.n = int(self.n)
            self.lamda=float(self.lamda)
            self.mio1,self.sd1 = n1.split(" ")
            self.mio2,self.sd2 = n2.split(" ")
            #print(self.mio1)
            self.mio1=float(self.mio1)
            self.sd1=float(self.sd1)
            self.mio2=float(self.mio2)
            self.sd2=float(self.sd2)
            print(type(self.mio1))
            


    
    def GenerateProcesses(self):
        for i in range (self.n):
            
            arrival = np.random.normal(self.mio1,self.sd1)
            burst = np.random.normal(self.mio2,self.sd2)
            priority = np.random.poisson(self.lamda)
            self.Processes.append(process.Process(arrival,burst,priority))
            

         
            
    def OutputFile (self):
        with open (self.outputFile,'w') as wf:
            wf.write(str(self.n))
            wf.write("\n")
            for i in range (self.n):
                wf.write(str(self.Processes[i]))
                
                