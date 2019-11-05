# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 19:42:57 2017

@author: DELL
"""
from Ass2 import traverseU,start,G
import numpy as np
import sympy as sp
import math as mt


def direction(e,G):
    data = G.get_edge_data(e[0],e[1])
    #print(e)
    observed = data['direction']
    print(observed)
    dy = G.node[e[1]]['y'] - G.node[e[0]]['y']
    dx = G.node[e[1]]['x'] - G.node[e[0]]['x']
    
    if dy < 0 and dx > 0:
        #print('1',dy,dx)
        calculated = mt.atan2(dy,dx) + 2*(mt.pi)
        correction = observed - calculated  
    if dy < 0 and dx < 0:
        #print('2',dy,dx)
        calculated = mt.atan2(dy,dx) + mt.pi
        correction = observed - calculated    
    if dy > 0 and dx < 0:
        #print('3',dy,dx)        
        calculated = mt.atan2(dy,dx) + mt.pi
        correction = observed - calculated    
    if dy > 0 and dx > 0:
       # print('4',dy,dx)
        calculated = mt.atan2(dy,dx)
        correction = observed - calculated
        
    return correction 

    
def appCorrection(start,G,coord_dict):
    dirCorrect = []
    data = G.edges(start)    
    for e in data:
        if G.node[e[1]]['code'] > 0 or e[1] in coord_dict :
            #print(e)
            dirCorrect.append(direction(e,G))
            tbc = 0
    mean = dirCorrect[-1]
    
    
    #print(dirCorrect[:-1],mean)
         
    for e in data:
        if G.node[e[1]]['code'] ==  0 and e[1] not in coord_dict:
            #print(e[1])
            free = G.get_edge_data(e[0],e[1])
            tbc = free['direction']
            er = tbc + mean
            if er < 0:
                free['direction'] = er + 2*np.pi
            else:
                free['direction'] = er
          #  print(dirCorrect,tbc,free['direction'],er,mean)
            return G

end = traverseU[-1][1]
    
coord_dict = {} 
coord_dict[start] = [G.node[start]['y'],G.node[start]['x']]
coord_dict[end] = [G.node[end]['y'],G.node[end]['x']]
#print(coord_dict)
d,z,xq,yq = sp.symbols('d z xq yq')

for point in traverseU:
  
    y = yq + d*sp.sin(z)
    x = xq + d*sp.cos(z)
    
    
    if point[0] in coord_dict.keys():
       # print(point)
        new = appCorrection(point[0],G,coord_dict)

        data = G.get_edge_data(point[0], point[1])
        p = point[0]
       # print(p)
        yf = y.subs({yq:coord_dict[p][0], d:data['distance'], z:data['direction']})
        xf = x.subs({xq:coord_dict[p][1], d:data['distance'], z:data['direction']})
        if G.node[point[1]]['code'] == 0:
            coord_dict[point[1]] = [yf,xf]   
            G.node[point[1]]['y'] = yf
            G.node[point[1]]['x'] = xf
      



