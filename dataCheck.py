# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 16:27:08 2017

@author: JHNLYD001
"""

from Ass2 import traverseU,edges
from InitialCoords import G


traverseO = []
for i in traverseU:
    data = G.get_edge_data(i[0],i[1])
    dist = data['distance']
    listed = [i[0],i[1],dist]
    traverseO.append(listed)

    
    
    
keyslist = G.nodes()
dictP = {}

for k in keyslist:
    p = [G.node[k]['y'], G.node[k]['x'], G.node[k]['code']]
    dictP[k] = p 




unknowns = []    
for j in keyslist:
    if G.node[j]['code'] == 0:
        jy = j+'y'
        jx = j+'x'
        unknowns.append(jy)
        unknowns.append(jx)
        
list1 = []        
for s in range(len(traverseU)):
    list1.append(traverseU[s][0])

list1.append(traverseU[-1][1])

unknowns= sorted(unknowns)
for h in list1:
    O = 'O'+h
    unknowns.append(O)

dirO = []   
for p in list1:
    theEdges = G.edges(p)
  
    
    for e in theEdges:
        data = G.get_edge_data(e[0],e[1])
        direc = data['direction']
        listE = [e[0],e[1],direc]
        dirO.append(listE)

   
#print(dirO)