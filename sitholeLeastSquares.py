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
from dataCheck import traverseO, dictP, unknowns, dirO
from weightP import P
import numpy as np
import math as mt
 
 
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
        if pi[2] != 1:
            dsdyi, dsdxi = (pi[0] - pj[0]) / sijo, (pi[1] - pj[1]) / sijo
 
        if pj[2] != 1:
            dsdyj, dsdxj = (pj[0] - pi[0]) / sijo, (pj[1] - pi[1]) / sijo
 
        # calculate l - lo
        dl = obs - sijo
 
        return [dsdxi, dsdyi, dsdxj, dsdyj, dl]


    def direction(self, pi, pj):
            # pi and pj of the for [x, y, bool]
            dy = pj[0] - pi[0]
            dx = pj[1] - pi[1]
#            print(dy,dx)
            if dy < 0 and dx > 0 :
                angle = mt.atan2(dy,dx) + 2*(mt.pi)
            if dy < 0 and dx < 0:
                angle = mt.atan2(dy,dx) + 2*(mt.pi)
            if dy > 0 and dx < 0:
                angle = mt.atan2(dy,dx) + mt.pi
            else:
                angle = mt.atan2(dy,dx)
            return angle

    def angleEqn(self, pi, pj, obs,station):
        sijo = self.distance(pi, pj) 
        distC = self.direction(pi,pj)
#        p = 206264.8062471
        p=1        
# calculate partial differentials
        dsdxi = dsdyi = dsdxj = dsdyj = None
        if pi[2] != 1 :
            dsdyi, dsdxi =p* (pi[0] - pj[0]) / (sijo)**2,p* (pi[1] - pj[1]) / (sijo)**2
 
        if pj[2] != 1:
            dsdyj, dsdxj = p*(pj[0] - pi[0]) / (sijo)**2, p*(pj[1] - pi[1]) / (sijo)**2
 
        # calculate l - lo
       # print(obs ,distC ,station)
        dl = p*(obs - distC)
        
        return [dsdxi, dsdyi, dsdxj, dsdyj, dl]
 
ls = LeastSquares()
 
for itera in range(10):
        A_list = []
        L_list = []
        num_unknown = len(unknowns)
        
        for o in dirO:
            name_pi = o[0]
            name_pj = o[1]
            pi = dictP[name_pi]
            pj = dictP[name_pj]
            obs = o[2]
            dsdxi, dsdyi, dsdxj, dsdyj, dl = ls.angleEqn(pi, pj, obs,name_pj)
            #print(dsdxi, dsdyi, dsdxj, dsdyj, dl)
            
            rowA =[0.0] * num_unknown
            
            add_row = False
                
        #   print(name_pi,name_pj)
            if 'O'+name_pi in unknowns:
                index = unknowns.index('O'+name_pi)
                rowA[index] = -1
                add_row = True
                   
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
    
    
        
    
    
        A = np.matrix(A_list, dtype = 'float' )
        L = np.matrix(L_list,dtype = 'float'  )
    
        ATP = (A.T*P*A).I
        ATL = A.T*P*L
        
        X = ATP*ATL
        V = A*X - L
        
        sigma0 = V.T*P*V/(A.shape[0]-A.shape[1]) 
        
        AdjCoords = []
        for j in unknowns:
            if j[-1] == 'x':
                dictP[j[:-1]][1] += float(X[(unknowns).index(j)])
            
            if j[-1] == 'y':
               dictP[j[:-1]][0] += float(X[(unknowns).index(j)])
        
            for k,u in enumerate(dirO):
                if j[1:] == u[0]:
                    dirO[k][2] += float(X[sorted(unknowns).index(j)])
                    
                    
                    
                    
        AdjCoords = dictP 
        
        Cv = float(sigma0)*ATP