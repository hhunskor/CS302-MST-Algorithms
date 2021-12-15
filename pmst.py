#Code by Wright Frost
#Group project w/Hayden Hunskor & Tom Gause
#Prim's list implementation using Adjacency Matrix

import sys
import random
import math
import datetime
from tqdm import tqdm #package to add progress bar
import numpy as np

#filepath = 'Int-6-10.txt' #easy way to update filepath
#filepath = 'Int-40-80 copy.txt'
filepath = 'Int-500-dense copy.txt'
#filepath = 'Int-1000-dense copy.txt'

#Prim's algorithm
def prim(filepath,Anim):

    edgecount,edgelist,vertices = readfile(filepath)
    mx = adjmx(edgelist, edgecount, vertices) #generates adjacency matrix (2D array that stores weights of edges between connected vertices)
    mst = [ [0 for i in range(vertices)] for j in range(vertices)]

    visited = [None for i in range(vertices)]
    unvisited = [1 for i in range(vertices)]

    visited[0] = 1
    unvisited[0] = None

    treesum = 0
    viscount = 0

    for i in tqdm(range(1,vertices)):
        viewed = []
        vert1 = -1
        vert2 = -1
        minval = sys.maxsize

        for i in range(vertices):
            if(visited[i] == 1):
                tempval,v2 = calculatemin(mx[i],unvisited)
                if tempval < minval and unvisited[v2] == 1:
                    minval = tempval
                    vert1 = i
                    vert2 = v2

        visited[vert2] = 1
        unvisited[vert2] = None

        treesum += minval

        mst[vert1][vert2] = minval

        viscount += 1

    print(treesum)
    return mst #Returns final minimum spanning tree matrix (tree can be recreated from this 2D array)


def calculatemin(list,unvisited):
    minval = sys.maxsize
    index = 0
    for i in range(len(list)):
        if unvisited[i] != None:
            if list[i] < minval and list[i] != 0:
                minval = list[i]
                index = i

    return minval,index

#Creating Adjacency Matrix
def adjmx(edgelist, edgecount, vertices):
    mx = [[0 for i in range(vertices)] for j in range(vertices)]#creating array to store edge adjacency (weights of edges connecting vertices)

    count = 0 #variable to track how many matrix slots have been filled

    while count < edgecount:

        cur_edge = edgelist[count]

        e1 = int(cur_edge[0])
        e2 = int(cur_edge[1])

        cost = cur_edge[2]

        mx[e1][e2] = cost #Adj matrix is symmetrical – value from i to j will be the same as value from j to i
        mx[e2][e1] = cost

        count += 1

    return(mx)

#Read in file
def readfile(path):
    edgecount = 0 #variable to store total number of edges
    edgelist = []

    with open(path,'r') as datafile:
        file = datafile.readlines()

    length = len(file)

    vertices = 0
    edges = 0

    for position, line in enumerate(file):
        if position == 0:
            vertices, edges = line.split()
            print(vertices + " vertices and " + edges + " edges")
            edges = int(edges)
            vertices = int(vertices)
            edgecount = edges

        elif position < (length - 1):
            l = (line.split())

            i = 0

            while i < 3:
                if 'Real' in path:
                    l[i] = float(l[i])
                else:
                    l[i] = int(l[i])

                i = i+1

            edgelist.append(l)

        elif position == (length - 1):
            print("sum of MST should equal " + line)

    datafile.close()

    return edgecount, edgelist, vertices

#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><

begin = datetime.datetime.now()

prim(filepath, False) #runs fxn; if boolean is set to "True," will run w/animation

tot_time = (datetime.datetime.now() - begin)

print("Runtime: " + str(tot_time))
