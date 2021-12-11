# Hayden Hunskor
# CS 302 - Group Implementation Programming Project
# Prim's Algorithm: Min Heap Priority Queue Implementation

import heapq
import datetime

import sys
import random
from graphics import *
import math

def fileRead(filename):
    
    file = open(filename, encoding = 'utf-8')
    
    arr = []
    
    for line in file:
        edge = []
        for val in line.split():
            try:
                edge.append(int(val)) #Try to make val an int
            except ValueError:
                edge.append(float(val)) #If not an int, make a float

        arr.append(edge)
        
    return(arr)

def prims(filename):
    
    #Read file
    arr = fileRead(filename)
    
    #Initialize variables
    n_vertices = arr[0][0]
    n_edges = arr[0][1]
        
    #Initialize and populate adjacency list
    adj_list = [[i] for i in range(n_vertices)]
    
    for i in range(1, n_edges + 1):
        edge = arr[i]
        adj_list[edge[0]].append((edge[2], edge[1]))
        adj_list[edge[1]].append((edge[2], edge[0]))
    
    #Initialize min-heap priority queue
    pq = []
    
    #Initialize empty MST
    MST = []
    
    #Initialize variable to store total weight
    total_weight = 0
    
    #Algorithm:
    visited = [0] #Start with source vertex (0)
    
    for i in range(1, len(adj_list[0])):
        heapq.heappush(pq, (adj_list[0][i][0], 0, adj_list[0][i][1]))
    
    heapq.heapify(pq)
    
    for i in range(n_vertices-1):
        min_edge = heapq.heappop(pq)
        
        while min_edge[2] in visited:
            min_edge = heapq.heappop(pq)
            
        total_weight += min_edge[0]
        next_v = min_edge[2]
        visited.append(next_v)
        MST.append((min_edge[1], next_v)) 
         
        for j in range(1, len(adj_list[next_v])):
            edge = adj_list[next_v][j]
            if edge[1] not in visited:
                heapq.heappush(pq, (edge[0], next_v, edge[1]))
         
        heapq.heapify(pq)
    
    return total_weight

begin = datetime.datetime.now()
print(prims('Int-40-80.txt'))
total_time = datetime.datetime.now() - begin
print(str(total_time))