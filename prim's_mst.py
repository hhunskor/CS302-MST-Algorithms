import sys
import random
from graphics import *
import math

filepath = 'Int-40-80 copy.txt'    
    
#Prim's algorithm
def prim(filepath):
    
    file = readfile(filepath)
    
    edgecount = file[0]
    edgelist = file[1]
    vertices = file[2]
    
    mx = adjmx(edgelist, edgecount)
    
    mst = [ [0 for i in range (edgecount)] for j in range(edgecount)]
     
    visited = [0 for i in range (edgecount)]
    
    start = 0 #start from first vertex
    
    visited[5] = 1
    
    vis = 0
    
    pts,edges,win = init_graphics(edgelist, edgecount, vertices, mx)
    
    while vis < edgecount:
        
        minval = sys.maxsize
        inf = sys.maxsize
        
        vert1 = -1
        vert2 = -1
        
        viewed = []
        
        
        for i in range (edgecount):
            
            if visited[i] == 1:
                
                for j in range(edgecount): 
                    
                    if(mx[i][j] != 0) and visited[j] != 1: #if an edge exists, and if visiting j won't create a loop
                        
                        ij = [i, j]
                        
                        viewed.append(ij)
                        
                        if mx[i][j] < minval:
                            minval = mx[i][j]
                            vert1 = i
                            vert2 = j
                            
        sel = [vert1,vert2]
        
                            
        #prim_anim(pts,edges,win,viewed,sel)
        #<><><><><>
        for i in range(len(viewed)):
            a = viewed[i][0]
            b = viewed[i][1]
            
            edges[a][b].setFill('Red')
            edges[a][b].setWidth(3)
            pts[a].setFill('Blue')
            pts[b].setFill('Blue')
        
        win.update()
        time.sleep(0.25)
        
        for i in range(len(viewed)):
            a = viewed[i][0]
            b = viewed[i][1]
            
            if [a,b] != sel:
                
                if visited[a] == 1:
                    pts[a].setFill('Green')
                else:
                    pts[a].setFill('White')
                if visited[b] == 1:
                    pts[b].setFill('Green')
                else:
                    pts[b].setFill('White')
                    
                edges[a][b].setFill('White')
                edges[a][b].setWidth(1)
                
                
                
            elif [a,b] == sel:
                pts[a].setFill('Green')
                pts[b].setFill('Green')
                edges[a][b].setFill('Red')
                edges[a][b].setWidth(1)
        
        win.update()
        time.sleep(0.25)
        #<><><><><><>
                
        if minval == inf:
            mst[vert1][vert2] = 0.0
        
        else:
            mst[vert1][vert2] = minval
            mst[vert2][vert1] = minval
            
        visited[vert2] = 1
        
        vis+=1
         
    #print(visited)
    
    treesum = 0
    
    for i in range (edgecount):
        for j in range(edgecount):
            treesum += (mst[i][j])
    
    print(treesum/2.0)
    
    
    
    
    return mst, edgelist

#Creating Adjacency Matrix
def adjmx(edgelist, edgecount):
    mx = [ [0 for i in range (edgecount)] for j in range (edgecount)] #creating array to store edge adjacency
    
    count = 0 #variable to track how many matrix slots have been filled
    
    while count < edgecount:
        
        cur_edge = edgelist[count]
        
        e1 = cur_edge[0]
        e2 = cur_edge[1]
        cost = cur_edge[2]
        
        mx[e1][e2] = float(cost)
        mx[e2][e1] = float(cost)
        
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
            print("sum of MST = " + line)
            
    datafile.close()
    
    return edgecount, edgelist, vertices

#Generate animation
def init_graphics(edgelist, edgecount, vertices, mx):
    
    n = len(edgelist)
    
    pts = generate_points(vertices)
    
    win = GraphWin("My Window", 750,750, autoflush = False)
    win.setBackground(color_rgb(100,100,100))
    
    diam = 8
    
    cirs = [ [] for i in range(vertices) ]
    lines = [ [ None for j in range (n) ] for i in range(n) ]
    
    for i in range(n):
        v1 = edgelist[i][0]
        v2 = edgelist[i][1]
        
        p1 = Point(pts[v1][0],pts[v1][1])
        p2 = Point(pts[v2][0],pts[v2][1])
        
        lines[v1][v2] = Line(p1,p2)
        lines[v1][v2].setFill(color_rgb(255,200,100))
        lines[v2][v1] = lines[v1][v2]
        lines[v1][v2].draw(win)
        
        p3 = lines[v1][v2].getCenter()
        
        txt = Text(p3, (edgelist[i][2]))
        txt.setSize(15)
        txt.setTextColor('white')
        txt.draw(win)
        
    for i in range(vertices):
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
    
    return(cirs,lines,win)
        
    


def generate_points(n):
    
    pts = [ [] for i in range(n)] #list to store coordinates
    
    for i in range(n):
        x = random.randint(0,750)
        y = random.randint(0,750)
        
        pts[i].append(x)
        pts[i].append(y)
    
    return pts
    


prim(filepath)
        
    
    


