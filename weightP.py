# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 13:20:08 2017

@author: JHNLYD001
"""
from Ass2 import traverseU, G
from dataCheck import dirO, traverseO, dictP 
import numpy as np
import math as mt


weightlst = []

    
def dirP(e,dictP) :   
    code = dictP[e[1]][2]
    if code != 1 and e[1]!='SUR09':
     #   print(e)
        weight = 0.01
        return weight
    else:
    #    print(e,'k')
        weight = 0.25
        return weight

for o in dirO:
    weight = dirP(o,dictP)
    weightlst.append((weight))

for o in traverseO:
   # print(o)
    weight = (5/1000)**2
    weightlst.append(1/weight)
    
P = np.diag(weightlst)