# -*- coding: utf-8 -*-
"""
Created on Mon May 29 13:14:06 2017

@author: JHNLYD001
"""

import networkx as nx
import numpy as np
import sympy as sp




dataEdges = open('TraverseObservations.csv')                                         
for t in range(0,1):
    dataEdges.readline()

    G = nx.DiGraph()                                                       #creating network with nodes and edges 
    
for line in dataEdges:
    s = line.split(',')
    node0 = s[0]
    node1 = s[1]
    dist = float(s[2])
    D = float(s[3])
    M = float(s[4])
    S = float(s[5])
    dirn = np.deg2rad(D + M/60 + S/3600)                        
    attribs = {'distance': (dist), 'direction': (dirn)}                         #adding edge data

    G.add_edge(node0, node1, attribs)

edges = G.edges()


dataNodes = open('TraverseControl.csv')                                         
for t in range(0,1):
    dataNodes.readline()
                                                   
for line in dataNodes:
    s = line.split(',')
    node = s[0]
    y = float(s[1])
    x = float(s[2])
    code = int(s[3])
    attribs = {'y': y, 'x': x, 'code':code}               
    G.node[node] = attribs
   
 

traverseU = []
for a in edges:
    data = G.get_edge_data(a[0],a[1])
    if G.out_degree(a[0]) > 0 and data['distance'] > 0:                         #this excludes orientatin rays since orientation rays have out_degree = 0 and they don't have distances so their ['distance'] = 0.-narrows search for start point
        codes = G.node[a[0]]['code']                                                #setting the start point for the bfs to get the initial coords. the start point will be the [0]node in the edge and will obviously be a fixed point - ['code'] = 1
        if codes == 1:
            start = a[0]

arranged = list(nx.bfs_edges(G,start))                                          #defines traverse route, but includes orientation rays

for k in arranged:
    data = G.get_edge_data(k[0],k[1])
    if G.out_degree(k[0]) > 0 and data['distance'] > 0:                        #exclusion of orientation rays to calc intitial coords.
        traverseU.append(k)                                                     #appending all other edges - this includes all the edges that have distance and direction which means that they are through traverse points and are not orientation observations. orientation observations willl be dealt with soon 
       

#print(traverseU)