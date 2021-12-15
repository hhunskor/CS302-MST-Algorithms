#Code by Wright Frost
#Group project w/Hayden Hunskor & Tom Gause
#Prim's list implementation using Adjacency Matrix

import sys
import random
from graphics import *
import math
import datetime
from tqdm import tqdm #package to add progress bar
import argparse
from distutils.util import strtobool
import csv


#Prim's algorithm
def prim(filepath,Anim):

    edgecount,edgelist,vertices = readfile(filepath)

    mx = adjmx(edgelist, edgecount, vertices) #generates adjacency matrix (2D array that stores weights of edges between connected vertices)
    mst = [ [0 for i in range(vertices)] for j in range(vertices)] #2D Array to store final tree

    win = None #Initializing variables to use with animation
    pts = None
    edges = None

    if Anim == True: #Sets up window to use in animation if "Anim" parameter = True
        win = GraphWin("My Window", 750,750, autoflush = False)
        win.setBackground(color_rgb(100,100,100))

        pts,edges = init_graphics(win,edgelist, edgecount, vertices, mx)

    visited = [None for i in range(vertices)] #At start, no vertices have been visited
    unvisited = [1 for i in range(vertices)] #so it makes sense that all vertices are marked 'unvisited'

    visited[0] = 1 #start by visiting vertex 0
    unvisited[0] = None

    treesum = 0

    for i in tqdm(range(1,vertices)): #one vertex has already been added, so we need to add n-1 more
        viewed = []
        vert1 = -1
        vert2 = -1
        minval = sys.maxsize

        for i in range(vertices): #consider every path from visited vertices to unvisited vertices
            if(unvisited[i] == 1):
                tempval,v1, checked = calculatemin(mx[i],visited, i) #calculatemin returns both the minimum value excluding zeros of an input array, the index of that value in the array, and all of the edges that were considered

                if Anim == True: #update animation
                    viewed = viewed + checked

                if tempval < minval and visited[v1] == 1: #if current edge weight is less than previous min, update variables
                    minval = tempval
                    vert2 = i
                    vert1 = v1

        visited[vert2] = 1 #end vertex of min-weight edge from this step is marked visited
        unvisited[vert2] = None #vert2 is no longer unvisited

        treesum += minval

        mst[vert1][vert2] = minval
        mst[vert2][vert1] = minval

        sel = [vert1,vert2]

        if Anim == True: #If animation is on, update animation with latest step
            prim_anim(pts,edges,win,viewed,visited,sel,mx)

    if Anim == True: #Close out animation by displaying final tree weight
        txt = Text(Point(375,700), "Calculated MST Weight: " + str(treesum))
        txt.setSize(20)
        txt.draw(win)
        txt.setFill('White')
        win.update()
        time.sleep(3)
        win.close()

    print(treesum)
    return mst #Returns final minimum spanning tree matrix (tree can be recreated from this 2D array)


def calculatemin(list,visited, parent):
    viewed = [] #empty array - edges that are considered will be added
    minval = sys.maxsize
    index = 0
    for i in range(len(list)):
        if visited[i] != None and list[i] != 0:
            viewed.append([parent,i]) #edge has now been considered
            if list[i] < minval:
                minval = list[i]
                index = i

    return minval,index, viewed

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

#Initializes graph window w/vertices and edges
def init_graphics(win, edgelist, edgecount, vertices, mx):
    n = len(edgelist)

    pts = generate_points(vertices)

    diam = 8

    cirs = [ [] for i in range(vertices) ]
    lines = [ [ None for j in range (n) ] for i in range(n) ]

    for i in (range(n)):
        v1 = int(edgelist[i][0])
        v2 = int(edgelist[i][1])

        p1 = Point(pts[v1][0],pts[v1][1])

        p2 = Point(pts[v2][0],pts[v2][1])

        lines[v1][v2] = Line(p1,p2)
        lines[v1][v2].setFill('White')
        lines[v2][v1] = lines[v1][v2]
        lines[v1][v2].draw(win)

        p3 = lines[v1][v2].getCenter() #pt in center of edge

        txt = Text(p3, (edgelist[i][2])) #display weight of edge
        txt.setSize(15)
        txt.setTextColor(color_rgb(0,200,200))
        txt.draw(win)

    for i in (range(vertices)):
        cirs[i] = Circle(Point(pts[i][0],pts[i][1]),diam)

        col1 = 255
        col2 = 255
        col3 = 255

        cirs[i].setFill(color_rgb(col1,col2,col3))
        cirs[i].setOutline(color_rgb(col1,col2,col3))
        cirs[i].draw(win)

        txt = Text(Point(pts[i][0],pts[i][1]), i)
        txt.setSize(12)
        txt.setTextColor(color_rgb(255,100,100))
        txt.draw(win)


    update()
    time.sleep(2)

    return(cirs,lines)

#fxn animates each step of prim's alg, showing which edges are considered, which is selected, and which vertices are added
def prim_anim(pts,edges,win,viewed,visited,sel,mx):
    if not None in edges:
        a = sel[0]
        b = sel[1]
        pts[a].setFill('Green')
        pts[a].setOutline('Green')
        pts[a].setWidth(10)
        win.update()

        for i in range(len(viewed)):
            x = viewed[i][0]
            y = viewed[i][1]

            edges[x][y].setFill('Red')
            edges[x][y].setWidth(3)

        win.update()
        time.sleep(1)

        txt = None
        txt2 = None

        if edges[a][b] != None:
            txt = Text(Point(375,700),"Edge " + str(a) + " == " + str(b) + " chosen")
            txt.setSize(20)
            txt.setTextColor('White')
            txt.draw(win)

            txt2 = Text(Point(375,720),"Weight " + str(mx[a][b]))
            txt2.setSize(15)
            txt2.setTextColor('White')
            txt2.draw(win)

        win.update()

        ct = 0

        while ct < 10 and edges[a][b] != None:
            edges[a][b].setFill('Red')
            win.update()
            time.sleep(0.1)
            edges[a][b].setFill('Blue')
            win.update()
            time.sleep(0.1)
            ct+=1


        pts[b].setFill('Green')
        pts[b].setOutline('Green')
        pts[b].setWidth(10)

        win.update()
        time.sleep(1)

        for i in range(len(viewed)):
            x = viewed[i][0]
            y = viewed[i][1]

            if [y,x] != sel:
                edges[x][y].setWidth(1)
                edges[x][y].setFill('White')

        if edges[a][b] != None:
            txt.undraw()
            txt2.undraw()

        win.update()
        time.sleep(2)

#Randomly generates points to display vertices
def generate_points(n):

    pts = [ [] for i in range(n)] #list to store coordinates of vertices

    for i in (range(n)):
        x = random.randint(20,740)
        y = random.randint(20,680)

        pts[i].append(x)
        pts[i].append(y)

    return pts

#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><
#Main method that ensures this program can run from the command line in Terminal
#Note: the default test file is a sample .txt file called 'Int-6-10.txt' that was created by Wright
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-input', '-i', type=str, default='Int-6-10.txt',
                        help='Data input file, Default [Int-6-10.txt]')
    parser.add_argument('-animation', '-a', type=strtobool, default=True)
    args = parser.parse_args()

    print("\n", "##### PRIM ARRAYS #####")
    print("INPUT: " + args.input)
    begin = datetime.datetime.now()
    MST = prim("MST-Test-Files/" + args.input, args.animation)
    print("MST: " + str(MST))
    total_time = datetime.datetime.now() - begin
    print("TIME: " + str(total_time))

    with open('tests.csv', 'a', newline='') as csvfile:
        test = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        test.writerow(['prim_arrays', args.input, total_time])

if __name__ == "__main__" :
    main()
