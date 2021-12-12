# Tom Gause
# CS302 Group Programming Project
# Kruskal's with Path Compression and Union by Rank

import sys
import random
from graphics import *
import math
import argparse
import datetime
from distutils.util import strtobool
import csv

class Graph:
    def __init__(self, num_vert, edgelist, Anim) :
        self.num_vert = num_vert
        self.edgelist = edgelist # contains Edge classes
        self.mst = []
        self.parent = []
        self.rank = []

        # animation-related variables
        if Anim:
            self.win = GraphWin("My Window", 750, 750, autoflush=False)
            self.win.setBackground(color_rgb(100, 100, 100))
            self.pts, self.edges = init_graphics(self.win, self.edgelist, num_vert)
            self.speed = 20 / len(edgelist)

    def FindParent (self, vert) : # has path compression
        if vert != self.parent[vert] :
            self.parent[vert] = self.FindParent(self.parent[vert])
        return self.parent[vert]

    def Kruskal (self, Anim) :
        # Sort edges by weight
        self.edgelist.sort(key = lambda Edge : Edge.weight)

        self.parent = [None] * self.num_vert
        self.rank   = [None] * self.num_vert

        for n in range(self.num_vert) :
            self.parent[n] = n # start w every vertex as its own parent
            self.rank[n] = 0 # start w rank 0

        for edge in self.edgelist :
            root1 = self.FindParent(edge.src)
            root2 = self.FindParent(edge.dst)

            # if parents are in different subsets, add the edge to the spanning tree
            if root1 != root2 :
               if Anim:
                   self.anim(edge, True) # animate for MST edge
               self.mst.append(edge)

               # union by rank
               if self.rank[root1] < self.rank[root2] :
                    self.rank[root2] += 1
                    self.parent[root1] = root2
               else:
                    self.rank[root1] += 1
                    self.parent[root2] = root1
            else:
                if Anim:
                    self.anim(edge, False) # animate for non-MST edge

        cost = 0
        for edge in self.mst :
            cost += edge.weight

        if Anim:
            txt = Text(Point(375, 700), "Calculated MST Weight: " + str(cost))
            txt.setSize(20)
            txt.draw(self.win)
            txt.setFill('White')
            self.win.update()
            time.sleep(10)
            self.win.close()

        return cost

    def anim(self, edge, MST):
        a, b = edge.src, edge.dst
        self.pts[a].setFill('Green')
        self.pts[a].setOutline('Green')
        self.pts[a].setWidth(10)
        self.win.update()

        txt, txt2 = None, None
        if MST:
            txt = Text(Point(375, 700), "Edge " + str(a) + "---" + str(b) + " chosen")
            txt.setSize(20)
            txt.setTextColor('White')
            txt.draw(self.win)
            txt2 = Text(Point(375, 720), "Weight " + str(edge.weight))
            txt2.setSize(15)
            txt2.setTextColor('White')
            txt2.draw(self.win)
        else:
            txt = Text(Point(375, 700), "Edge " + str(a) + "---" + str(b) + " not chosen")
            txt.setSize(20)
            txt.setTextColor('White')
            txt.draw(self.win)
            txt2 = Text(Point(375, 720), "Weight " + str(edge.weight))
            txt2.setSize(15)
            txt2.setTextColor('White')
            txt2.draw(self.win)

        self.edges[a][b].setFill('Blue')
        self.pts[b].setFill('Green')
        self.pts[b].setOutline('Green')
        self.pts[b].setWidth(10)

        x, y = edge.src, edge.dst

        if MST:
            self.edges[x][y].setFill('Blue')
            self.edges[x][y].setWidth(3)
        else:
            self.edges[x][y].setFill('Red')
            self.edges[x][y].setWidth(3)

        self.win.update()
        time.sleep(self.speed)

        txt.undraw()
        txt2.undraw()

class Edge:
    def __init__(self, source, destination, w):
        self.src = source
        self.dst = destination
        self.weight = w

def readfile(path):
    #print("reading file...")
    edgelist = []
    with open(path, 'r') as datafile:
        file = datafile.readlines()
    length = len(file)
    edgecount, vertices, edges = 0, 0, 0

    for position, line in enumerate(file):
        if position == 0:
            vertices, edges = line.split()
            #print(vertices + " vertices and " + edges + " edges")
            edges = int(edges)
            vertices = int(vertices)
            edgecount = edges

        elif position < (length - 1):
            l = line.split()
            i = 0
            while i < 3:
                if 'Real' in path and i == 2:
                    l[i] = float(l[i])
                else:
                    l[i] = int(l[i])
                i = i + 1
            edgelist.append(l)

        # elif position == (length - 1):
        #     print("sum of MST should equal " + line)

    datafile.close()
    return edgelist, vertices

#Generate animation
def init_graphics(win, edgelist, vertices):
    #print("initiating graphics...")
    n = len(edgelist)
    pts = generate_points(vertices)
    diam = 8

    cirs = [ [] for i in range(vertices) ]
    lines = [ [ None for j in range (n) ] for i in range(n) ]

    for i in range(n):
        v1, v2 = edgelist[i].src, edgelist[i].dst
        p1, p2 = Point(pts[v1][0],pts[v1][1]), Point(pts[v2][0],pts[v2][1])

        lines[v1][v2] = Line(p1,p2)
        lines[v1][v2].setFill('White')
        lines[v2][v1] = lines[v1][v2]
        lines[v1][v2].draw(win)

        p3 = lines[v1][v2].getCenter()

        txt = Text(p3, (edgelist[i].weight))
        txt.setSize(15)
        txt.setTextColor(color_rgb(0,200,200))
        txt.draw(win)

    for i in range(vertices):
        cirs[i] = Circle(Point(pts[i][0],pts[i][1]),diam)
        col1, col2, col3 = 255, 255, 255
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

def generate_points(n):
    #print("generating random points...")
    pts = [ [] for i in range(n)] #list to store coordinates
    for i in range(n):
        x = random.randint(20,740)
        y = random.randint(20,680)
        pts[i].append(x)
        pts[i].append(y)
    return pts

# Kruskal Path Compression and Union by Rank
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-input', '-i', type=str, default='Int-6-10.txt',
                        help='Data input file, Default [Int-6-10.txt]')
    parser.add_argument('-animation', '-a', type=strtobool, default=True)
    args = parser.parse_args()

    filepath = "MST-Test-Files/" + args.input
    edgelist, vertices = readfile(filepath)

    edges = []
    for e in edgelist:
        edges.append(Edge(e[0], e[1], e[2]))

    print("\n", "##### KRUSKAL #####")
    print("INPUT: " + args.input)
    begin = datetime.datetime.now()
    graph = Graph(vertices, edges, args.animation)
    MST = graph.Kruskal(args.animation)
    print("MST: " + str(MST))
    total_time = datetime.datetime.now() - begin
    print("RUNTIME: " + str(total_time))

    with open('tests.csv', 'a', newline='') as csvfile:
        test = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        test.writerow(['kruskal', args.input, total_time])

if __name__ == "__main__" :
    main()