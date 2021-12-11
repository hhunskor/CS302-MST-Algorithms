import sys
import random
from graphics import *
import math
import datetime
from tqdm import tqdm

#filepath = 'Int-6-10.txt'
#filepath = 'Int-40-80 copy.txt'
#filepath = 'Real-500-dense copy.txt'
filepath = 'Int-500-dense copy.txt'
#filepath = 'Real-50-100 copy.txt'
#filepath = 'Real-1000-dense copy.txt'

#Prim's algorithm
def prim(filepath,Anim):

    file = readfile(filepath)

    edgecount = file[0]
    edgelist = file[1]
    vertices = file[2]

    mx = adjmx(edgelist, edgecount,vertices)

    mst = [ [0 for i in range (vertices)] for j in range(vertices)]

    visited = [0 for i in range (vertices)]

    start = 0 #start from first vertex

    visited[0] = 1

    treesum = 0


    while 0 in visited:
        minval = sys.maxsize
        inf = sys.maxsize

        vert1 = -1
        vert2 = -1

        viewed = []


        for i in tqdm(range (vertices)):

            if visited[i] == 1:

                for j in range(vertices):

                    if(mx[i][j] != 0) and visited[j] != 1: #if an edge exists, and if visiting j won't create a loop

                        ij = [i, j]

                        viewed.append(ij)

                        if mx[i][j] < minval:
                            minval = mx[i][j]
                            vert1 = i
                            vert2 = j

        sel = [vert1,vert2]


        if minval == inf:
            mst[vert1][vert2] = 0.0

        else:
            mst[vert1][vert2] = minval
            mst[vert2][vert1] = minval

        visited[vert2] = 1

        treesum += minval


    print("Calculated MST weight: " + str(treesum))



    return mst, edgelist

#Creating Adjacency Matrix
def adjmx(edgelist, edgecount, vertices):
    mx = [ [0 for i in range (vertices)] for j in range (vertices)] #creating array to store edge adjacency

    count = 0 #variable to track how many matrix slots have been filled

    while count < edgecount:

        cur_edge = edgelist[count]

        e1 = cur_edge[0]
        e2 = cur_edge[1]
        cost = cur_edge[2]

        mx[e1][e2] = cost
        mx[e2][e1] = cost

        count += 1

    return(mx)

#Read in file
def readfile(path):
    edgelist = []
    edgecount = 0

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
                if 'Real' in path and i == 2:
                    l[i] = float(l[i])
                else:
                    l[i] = int(l[i])

                i = i+1

            edgelist.append(l)

        elif position == (length - 1):
            print("sum of MST should equal " + line)

    datafile.close()

    return edgecount, edgelist, vertices




begin = datetime.datetime.now()

prim(filepath, False)

tot_time = (datetime.datetime.now() - begin)

print("Runtime: " + str(tot_time))
