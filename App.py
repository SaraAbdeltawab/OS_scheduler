# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 10:50:42 2018

@author: Sara
"""

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import tkinter as tk
from pathlib import Path
import hpf 
import srtn
import fcfs
import rr

"""
Takes an Entry and check if the passed it is a number
"""
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
        
    def CreateWindow(self):
        
        self.master.title('Scheduling')
        self.master.geometry("1200x800")
        
        self.rootFrame = tk.Frame(master=self.master)
        self.rootFrame.grid(row='0',column='0')
        
        self.CreateEntries()
        self.CreateButtons()
        self.CreateErrorMsg()
    
    def CreateEntries(self):
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
        
        self.timeLbl = tk.Label(master = self.frame1, text = "Time in sec")
        self.timeLbl.grid(row='2', column='2')
        
    def CreateButtons(self):   
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
        
    def CreateErrorMsg(self):
        self.errorMsgLbl = tk.Label(master=self.frame3, text='Please double check all required inputs', foreground='red')
        self.errorMsgLbl.grid(row='2',column='1')
        self.errorMsgLbl.grid_remove()
        
        self.fileErrorMsgLbl = tk.Label(master=self.frame3, text='File not find', foreground='red')
        self.fileErrorMsgLbl.grid(row='2',column='1')
        self.fileErrorMsgLbl.grid_remove()
        
    def CheckInputs(self):
        if self.fileName.get() == "" or self.contextSwitchingTime.get() == "" or not is_float(self.contextSwitchingTime):
            self.errorMsgLbl.grid()
            return False
        if float(self.contextSwitchingTime.get()) < 0:
            self.errorMsgLbl.grid()
            return False
        
        file = Path(self.fileName.get())
        if not file.is_file():
            self.fileErrorMsgLbl.grid()
            return False
        return True
    
    def InitializeWindow(self):
        self.timeQuantumLbl.grid_remove()
        self.timeQuantum.grid_remove()
        self.timeQuantumBtn.grid_remove()
        self.errorMsgLbl.grid_remove()
        self.fileErrorMsgLbl.grid_remove()
    
    def RunHPF(self):
        self.InitializeWindow()
        if not self.CheckInputs():
            return
        
        myAlgo=hpf.HPF(self.fileName.get(),float(self.contextSwitchingTime.get()))
        schedulNumber,startTime,endTime=myAlgo.GetStatsData()

        self.CreateGraph(schedulNumber,startTime,endTime, "HPF")
        
    def RunFCFS(self):
        self.InitializeWindow()
        if not self.CheckInputs():
            return
        
        RunAlgo=fcfs.FCFS(self.fileName.get(),float(self.contextSwitchingTime.get()))
        schedulNumber,startTime,endTime=RunAlgo.GetStatsData()

        self.CreateGraph(schedulNumber,startTime,endTime, "FCFS")
        
    def RunSTRN(self):
        self.InitializeWindow()
        if not self.CheckInputs():
            return
        
        RunAlgo=srtn.SRTN(self.fileName.get(),float(self.contextSwitchingTime.get()))
        schedulNumber,startTime,endTime=RunAlgo.GetStatsData()
        
        self.CreateGraph(schedulNumber,startTime,endTime, "STRN")
        
    def RunRR(self):
        self.errorMsgLbl.grid_remove()
        self.fileErrorMsgLbl.grid_remove()
        
        if not self.CheckInputs():
            return
        
        if not is_float(self.timeQuantum):
            self.errorMsgLbl.grid()
            return
        
        if float(self.timeQuantum.get()) <= 0:
            self.errorMsgLbl.grid()
            return 
        
        myAlgo=rr.RR(self.fileName.get(),float(self.contextSwitchingTime.get()),float(self.timeQuantum.get()))
        schedulNumber,startTime,endTime=myAlgo.GetStatsData()
        self.CreateGraph(schedulNumber,startTime,endTime, "RR")
         
    def ViewQuantum(self):
        self.errorMsgLbl.grid_remove()
        
        self.timeQuantumLbl.grid()
        self.timeQuantum.grid()
        self.timeQuantumBtn.grid()
        
    def CreateGraph(self, schedulNumber, startTime, endTime, algoName):
        fig = plt.figure(figsize = (7,7), dpi = 100) 
        ax1= fig.add_subplot(1,1,1)
        xs = []
        ys = []
        xs.append(startTime[0]/1000.0)
        ys.append(0)
        for i in range (len(schedulNumber)):
            if i != 0 and startTime[i] != endTime[i-1]: 
                ys.append(0)
                ys.append(0)
                xs.append(endTime[i-1]/1000.0)
                xs.append(startTime[i]/1000.0)
                    
            ys.append(schedulNumber[i])
            ys.append(schedulNumber[i])
            xs.append(startTime[i]/1000.0)
            xs.append(endTime[i]/1000.0)
        ys.append(0)
        xs.append(endTime[len(schedulNumber)-1]/1000.0)
        
        ax1.clear()
        #ax1.set_xticks(xs, minor=True) #view all ticks on x-axis
        plt.xticks(xs) #view all values
        plt.yticks(ys) #view all values
        ax1.plot(xs,ys)
        plt.xticks(rotation=90)

        #fig.autofmt_xdate() #make  oblique labels
        
        for i in ax1.get_xticklabels():
            i.set_fontsize('small') #labels font

        self.canvas = FigureCanvasTkAgg(fig, self.master)
        self.canvas.show() #??
        self.canvas.get_tk_widget().grid(row = '0', column = '5')
      
        self.toolbar_frame = tk.Frame(self.master)
        self.toolbar_frame.grid(row=21,column=4,columnspan=2)
        self.toolbar = NavigationToolbar2TkAgg( self.canvas, self.toolbar_frame )
        self.toolbar.update()
        
        plt.ylabel('Process number')
        plt.xlabel('Running time in seconds')
        plt.title(algoName)
#        plt.show()
       
        
root = tk.Tk()
app = App(root)
root.mainloop()