# Hayden Hunskor
# CS 302 - Group Implementation Programming Project
# Prim's Algorithm: Min Heap Priority Queue Implementation

import heapq
import datetime

import sys
import random
from graphics import *
import math
import argparse
from distutils.util import strtobool
import csv

#This method reads from a .txt file
def fileRead(filename):
    
    file = open(filename)
    
    arr = []
    
    #Iterate through each line in the file
    for line in file:
        edge = []
        for val in line.split():
            try:
                edge.append(int(val)) #Try to make val an int
            except ValueError:
                edge.append(float(val)) #If not an int, make a float

        arr.append(edge) #Add edge to an array
        
    return(arr)

#This method executes Prims algorithm and, if anim == True, will animate it
def prims(filename, anim):
    
    #Read file
    arr = fileRead(filename)
    
    #Initialize variables
    n_vertices = arr[0][0]
    n_edges = arr[0][1]
    
    #If we want to animate, set up window and all the points and edges
    if anim == True:
        win = GraphWin("My Window", 750,750, autoflush = False)
        win.setBackground(color_rgb(100,100,100))
        
        txt3 = Text(Point(80,40),"Total weight of MST: ")
        txt3.setSize(15)
        txt3.setTextColor('White')
        txt3.draw(win)
        
        txt4 = Text(Point(155,40), str(0))
        txt4.setSize(15)
        txt4.setTextColor('White')
        txt4.draw(win)
    
        points, lines = init_graphics(win, arr[1:-1], n_vertices)
        
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
    
    #If we are animating, set source vertex to green (to show it was selected)
    if anim == True:
        points[0].setFill('Green')
        points[0].setOutline('Green')
        points[0].setWidth(9)
        win.update()
        time.sleep(1)
    
    #Iterate through all of the edges coming from source vertex and add to heap
    for i in range(1, len(adj_list[0])):
        heapq.heappush(pq, (adj_list[0][i][0], 0, adj_list[0][i][1]))
        
        #Set color of all lines being considered to blue
        if anim == True:
            line = lines[0][adj_list[0][i][1]]
            line.setFill('Blue')
            line.setWidth(2)
    
    #Update
    if anim == True: 
        win.update()
        time.sleep(1)
    
    #Iterate through n_vertices - 1 number of edges
    for i in range(n_vertices-1):
        min_edge = heapq.heappop(pq)
        
        #If the min_edge destination vertex has already been visited
        while min_edge[2] in visited:
            min_edge = heapq.heappop(pq)
        
        #If we are animating, color the min edge red and update text on the screen
        if anim == True:
            line = lines[min_edge[1]][min_edge[2]]
            line.setFill('Red')
            win.update()
            points[min_edge[2]].setFill('Green')
            points[min_edge[2]].setOutline('Green')
            points[min_edge[2]].setWidth(9)
            
            #Update text
            txt = Text(Point(375,700),"Edge " + str(min_edge[1]) + " == " + str(min_edge[2]) + " chosen")
            txt.setSize(20)
            txt.setTextColor('White')
            txt.draw(win)
            
            txt2 = Text(Point(375,720),"Weight " + str(min_edge[0]))
            txt2.setSize(15)
            txt2.setTextColor('White')
            txt2.draw(win)
            
        if anim == True:
            win.update()
            time.sleep(1.5)
            txt.undraw()
            txt2.undraw()
            
        #Add the weight of the edge to the total weight of the MST
        total_weight += min_edge[0]
        
        if anim == True:
            txt4.undraw()
            txt4 = Text(Point(155,40), str(total_weight))
            txt4.setSize(15)
            txt4.setTextColor('White')
            txt4.draw(win)
        
        
        next_v = min_edge[2]
        visited.append(next_v) #Add the destination vertex to the visited list
        MST.append((min_edge[1], next_v)) #Add the edge to the MST
        
        #Iterate through each of the edges extending from the min edge destination vertex
        for j in range(1, len(adj_list[next_v])):
            edge = adj_list[next_v][j]
            
            #If the edge hasn't been visited, add it to the queue
            if edge[1] not in visited:
                heapq.heappush(pq, (edge[0], next_v, edge[1]))
                
                #Color edges under consideration blue
                if anim == True:
                    next_line = lines[next_v][edge[1]]
                    next_line.setFill('Blue')
                    next_line.setWidth(2)
            
        if anim == True:
            win.update()
            time.sleep(1)
    
    #At the very end, color all the edges that weren't selected white to make the visual better
    if anim == True:
        for i in range(1, n_edges + 1):
            edge = (arr[i][0], arr[i][1])
            edge2 = (arr[i][1], arr[i][0])
            if edge not in MST and edge2 not in MST:
                line = lines[arr[i][0]][arr[i][1]]
                line.setFill('White')
        win.update()
        time.sleep(2)
    
    return total_weight

#This method is responsible for initializing all the vertices and edges of the graph in a graphics window 
def init_graphics(win, edge_list, vertices):
    points = []
    weights = []
    diam = 8
    
    circles = []
    lines = [[ None for i in range(len(edge_list)) ] for i in range(len(edge_list))]
    
    #Generate random Point objects within the frame
    for i in range(vertices):
        x = random.randint(20, 740)
        y = random.randint(60, 680)
        points.append(Point(x, y))
    
    #Generate Line objects that connect vertices, and add weight text
    for i in range(len(edge_list)):
        p1 = points[edge_list[i][0]]
        p2 = points[edge_list[i][1]]
        weight = edge_list[i][2]
        
        line = Line(p1, p2)
        line.setFill('White')
        line.draw(win)
        
        p3 = line.getCenter()

        txt = Text(p3, weight)
        txt.setSize(15)
        txt.setTextColor(color_rgb(0,200,200))
        txt.draw(win)
        
        lines[edge_list[i][0]][edge_list[i][1]] = line
        lines[edge_list[i][1]][edge_list[i][0]] = line
    
    #Draw actual vertices using list of Point objects
    for i in range(vertices):
        circle = Circle(points[i],diam)

        col1 = 255
        col2 = 255
        col3 = 255

        circle.setFill(color_rgb(col1,col2,col3))
        circle.setOutline(color_rgb(col1,col2,col3))
        circle.draw(win)

        txt = Text(points[i], i)
        txt.setSize(12)
        txt.setTextColor(color_rgb(255,100,100))
        txt.draw(win)
        circles.append(circle)
        
    win.update()
    
    return(circles, lines)

#Main method that ensures this program can run from the command line in Terminal
#Note: the default test file is a sample .txt file called 'Int-6-10.txt' that was created by Wright
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-input', '-i', type=str, default='Int-6-10.txt',
                        help='Data input file, Default [Int-6-10.txt]')
    parser.add_argument('-animation', '-a', type=strtobool, default=True)
    args = parser.parse_args()

    print("\n", "##### PRIM MINHEAP #####")
    print("INPUT: " + args.input)
    begin = datetime.datetime.now()
    MST = prims("MST-Test-Files/" + args.input, args.animation)
    print("MST: " + str(MST))
    total_time = datetime.datetime.now() - begin
    print("TIME: " + str(total_time))

    with open('tests.csv', 'a', newline='') as csvfile:
        test = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        test.writerow(['prim_minheap', args.input, total_time])

if __name__ == "__main__" :
    main()
