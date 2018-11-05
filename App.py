# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 10:50:42 2018

@author: user
"""

from matplotlib import pyplot as plt
#matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import tkinter as tk
from pathlib import Path

import hpf 

#takes an entry as a parameter 
#check if it is a number
def is_float(x):
    try:
        float(x.get())
        return True
    except ValueError:
        return False
    
class App(object):
    def __init__(self, master):
        self.master = master
        self.CreateWindow()
        #self.create_graph(schedulNumber, startTime, endTime)
    def CreateWindow(self):
        
        self.master.title('Scheduling')
        self.master.geometry("900x600")
        
        self.rootFrame = tk.Frame(master=self.master)
        self.rootFrame.grid(row='0',column='0')
        
        self.frame1 = tk.Frame(master=self.rootFrame, pady='15', padx='50')
        self.frame1.grid(row='0',column='0')

        self.fileNameLbl = tk.Label(master = self.frame1, text="File Name")
        self.fileNameLbl.grid(row='1')
        
        self.fileName = tk.Entry(master = self.frame1, bd = 4)
        self.fileName.grid(row='1', column='1')
        
        self.contextSwitchingLbl = tk.Label(master = self.frame1, text="Context Switching Time")
        self.contextSwitchingLbl.grid(row='2')
        
        self.contextSwitchingTime = tk.Entry(master = self.frame1, bd = 4, )
        self.contextSwitchingTime.grid(row='2', column='1')
        
        
        self.frame2 =  tk.Frame(master=self.rootFrame, pady='50', padx='50')
        self.frame2.grid(row='3',column='0')
        
        self.lblframe = tk.LabelFrame(master=self.frame2, text="Scheduling algorithms", height="320", width='32', pady='5', padx = '5')
        self.lblframe.grid(row='3', column='0')
         
        self.HPF = tk.Button(master=self.lblframe, text='Non-Preemptive Highest Priority First', width='32', bd=4, command=self.RunHPF)
        self.HPF.grid(row='4',column='0')
        
        self.FCFS = tk.Button(master=self.lblframe, text='First Come First Served', width='32', bd=4, command=self.RunFCFS)
        self.FCFS.grid(row='5',column='0')
        
        self.STRN = tk.Button(master=self.lblframe, text='Preemptive Shortest Remaining Time Next', width='32', bd=4, command=self.RunSTRN)
        self.STRN.grid(row='6',column='0')
        
        self.RR = tk.Button(master=self.lblframe, text='Round Robin with fixed time quantum', width='32', bd=4, command=self.ViewQuantum)
        self.RR.grid(row='7',column='0')
        
        self.frame3 =  tk.Frame(master=self.frame2, pady ='5')
        self.frame3.grid(row='4',column='0', sticky='w')
        

        self.timeQuantumLbl = tk.Label(master = self.frame3, text="Time Quantum")
        self.timeQuantumLbl.grid(row='1', column= '0')
        self.timeQuantumLbl.grid_remove()
        
        self.timeQuantum = tk.Entry(master = self.frame3, bd = 4)
        self.timeQuantum.grid(row='1', column='1', padx = '15')
        self.timeQuantum.grid_remove()
        
        self.timeQuantumBtn = tk.Button(master=self.frame3, text='Run', bd=4, command=self.RunRR)
        self.timeQuantumBtn.grid(row='1',column='3')
        self.timeQuantumBtn.grid_remove()
        
        self.errorMsgLbl = tk.Label(master=self.frame3, text='Please double check all required inputs', foreground='red')
        self.errorMsgLbl.grid(row='2',column='1')
        self.errorMsgLbl.grid_remove()
        
    def CheckInputs(self):
        if self.fileName.get() == "" or self.contextSwitchingTime.get() == "" or not is_float(self.contextSwitchingTime): 
            self.errorMsgLbl.grid()
            return False
        
        file = Path(self.fileName.get())
        if not file.is_file():
            self.errorMsgLbl.grid()
            return False
        return True
        
    def RunHPF(self):
        self.timeQuantumLbl.grid_remove()
        self.timeQuantum.grid_remove()
        self.timeQuantumBtn.grid_remove()
        self.errorMsgLbl.grid_remove()
        
        if not self.CheckInputs():
            return
        
        myAlgo=hpf.HPF(self.fileName.get(),float(self.contextSwitchingTime.get()))
        schedulNumber,startTime,endTime=myAlgo.GetStatsData()
        
#        schedulNumber = [1,2,3,1,5]
#        startTime = [5,10,20,30,40]
#        endTime = [9,20,25,40,100]
        self.CreateGraph(schedulNumber,startTime,endTime, "HPF")
        
    def RunFCFS(self):
        self.timeQuantumLbl.grid_remove()
        self.timeQuantum.grid_remove()
        self.timeQuantumBtn.grid_remove()
        self.errorMsgLbl.grid_remove()
            
        if not self.CheckInputs():
            return
        
        schedulNumber = [1,2,3,1,5]
        startTime = [5,10,20,30,40]
        endTime = [9,20,25,40,100]
        self.CreateGraph(schedulNumber,startTime,endTime, "FCFS")
        
    def RunSTRN(self):
        self.timeQuantumLbl.grid_remove()
        self.timeQuantum.grid_remove()
        self.timeQuantumBtn.grid_remove()
        self.errorMsgLbl.grid_remove()
        
        if not self.CheckInputs():
            return
            
        schedulNumber = [1,2,3,1,5]
        startTime = [5,10,20,30,40]
        endTime = [9,20,25,40,100]
        self.CreateGraph(schedulNumber,startTime,endTime, "STRN")
        
    def RunRR(self):
        self.errorMsgLbl.grid_remove()
        
        if not self.CheckInputs():
            return
        
        if not is_float(self.timeQuantum):
            self.errorMsgLbl.grid()
            return
        
        schedulNumber = [1,2,3,1,5]
        startTime = [5,10,20,30,40]
        endTime = [9,20,25,40,100]
        print('b4 call graph, RUN RR')
        self.CreateGraph(schedulNumber,startTime,endTime, "RR")
        print('after call graph, RUN RR')
         
    def ViewQuantum(self):
        self.errorMsgLbl.grid_remove()
        
        self.timeQuantumLbl.grid()
        self.timeQuantum.grid()
        self.timeQuantumBtn.grid()
        
    def CreateGraph(self, schedulNumber, startTime, endTime, algoName):
        
        fig = plt.figure(figsize = (5,5), dpi = 100) #??
        ax1= fig.add_subplot(1,1,1) #??
        #xs = [6,6,8,8,10,10,11,11,13]
        #ys = [0,1,1,2,2,0,0,3,3]
        xs = []
        ys = []
        xs.append(startTime[0])
        ys.append(0)
        print('xs: ', xs)
        print('ys: ', ys)
        for i in range (len(schedulNumber)):#?? len walla len-1 ??
            if i != 0 and startTime[i] != endTime[i-1]: 
                ys.append(0)
                ys.append(0)
                xs.append(endTime[i-1])
                xs.append(startTime[i])
                    
            ys.append(schedulNumber[i])
            ys.append(schedulNumber[i])
            xs.append(startTime[i])
            xs.append(endTime[i])
        ys.append(0)
        xs.append(endTime[len(schedulNumber)-1])
        
        ax1.clear()
        ax1.plot(xs,ys)

        self.canvas = FigureCanvasTkAgg(fig, self.master) #,self
        self.canvas.show() #??
        self.canvas.get_tk_widget().grid(row = '0', column = '5')
        print('endof create graph')
      
        self.toolbar_frame = tk.Frame(self.master)
        self.toolbar_frame.grid(row=21,column=4,columnspan=2)
        self.toolbar = NavigationToolbar2TkAgg( self.canvas, self.toolbar_frame )
        #toolbar = NavigationToolbar2TkAgg(canvas, window) #,self
        self.toolbar.update()
        #canvas._tkcanvas.grid(row='7',column='3')
        
        plt.ylabel('Process number')
        plt.xlabel('Running time')
        plt.title(algoName)
        plt.show()
       
        
root = tk.Tk()
app = App(root)
root.mainloop()