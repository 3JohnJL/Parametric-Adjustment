# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 16:20:21 2017

@author: JHNLYD001
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 16:03:50 2017
 
@author: rsnang001
"""
from dataCheck import traverseO, dictP,unknowns 
import numpy as np
 
 
class LeastSquares:
    def __init__(self):
        pass
 
    def distance(self, pi, pj):
        # pi and pj of the for [x, y, bool]
        dy = pj[0] - pi[0]
        dx = pj[1] - pi[1]
        #print(dy,dx)
        return (dx * dx + dy * dy)**(1/2)
        
    def distanceEqn(self, pi, pj, obs):
        sijo = self.distance(pi, pj)       
 
        # calculate partial differentials
        dsdxi = dsdyi = dsdxj = dsdyj = None
        if not pi[2]:
            dsdyi, dsdxi = (pi[0] - pj[0]) / sijo, (pi[1] - pj[1]) / sijo
 
        if not pj[2]:
            dsdyj, dsdxj = (pj[0] - pi[0]) / sijo, (pj[1] - pi[1]) / sijo
 
        # calculate l - lo
        dl = obs - sijo
 
        return [dsdxi, dsdyi, dsdxj, dsdyj, dl]




 
ls = LeastSquares()
 


 

 
for itera in range(10):
    A_list = []
    L_list = []
    num_unknown = len(unknowns)
    for o in traverseO:
        name_pi = o[0]
        name_pj = o[1]
        pi = dictP[name_pi]
        pj = dictP[name_pj]
        obs = o[2]
        dsdxi, dsdyi, dsdxj, dsdyj, dl = ls.distanceEqn(pi, pj, obs)
        #print(dsdxi, dsdyi, dsdxj, dsdyj, dl)
    
        rowA =[0.0] * num_unknown
    
        add_row = False
        if dsdxi != None:
            index = unknowns.index(name_pi + 'x')
            rowA[index] = dsdxi
            add_row = True
    
        if dsdyi != None:
            index = unknowns.index(name_pi + 'y')
            rowA[index] = dsdyi
            add_row = True
    
        if dsdxj != None:
            index = unknowns.index(name_pj + 'x')
            rowA[index] = dsdxj
            add_row = True
    
        if dsdyj != None:
            index = unknowns.index(name_pj + 'y')
            rowA[index] = dsdyj
            add_row = True
    
        if add_row:
            A_list += [rowA]
            L_list += [[dl]]


    A = np.matrix(A_list)
    L = np.matrix(L_list)

    print(L)
  # x = (A.T * A).I * A.T * L
