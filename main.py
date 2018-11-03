# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 21:22:58 2018

@author: hagar
"""

import processgenerator as pg
#import process as pr
from operator import attrgetter
gen=pg.Generator("input.txt")
#gen.Processes.sort(key=attrgetter('priority'),reverse=True)  # this one works alone i think cause sort is stable
#gen.Processes.sort(key=attrgetter('priority','ID'),reverse=True) #sort by priority then ID but this would reverse the id also
gen.Processes.sort(key=attrgetter('ID')) # sort on secandry key first 
gen.Processes.sort(key=attrgetter('priority'),reverse=True) #then on primary key descending
gen.Processes.sort() #sort by arrival time
for i in range (gen.n):
    print (gen.Processes[i])
