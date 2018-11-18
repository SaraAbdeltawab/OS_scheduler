# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 14:54:48 2018

@author: user
"""

from operator import attrgetter
class variableList(object):
    def __init__(self, eight, sixteen, thirtytwo):
        self.size_8 = eight
        self.size_16 = sixteen
        self.size_32 = thirtytwo
        
s = []
s.append(variableList(2,1,4))
s.append(variableList(1,3,4))
s.append(variableList(1,2,4))
s.append(variableList(0,4,4))
s.append(variableList(6,5,4))

s.sort(key=attrgetter("size_8","size_16"))
for i in range (len(s)):
    print(s[i].size_8, " hhh ", s[i].size_16)