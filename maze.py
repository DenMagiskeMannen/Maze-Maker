# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 15:05:15 2024

@author: teodo
"""

import pygame
import time
import random
import math
screenie = (1280, 720)

class Cell:
    cells=[]

    def __init__(self,owner,x,y):
        #Self ID
        self.pos=(x,y)
        self.owner=owner
        self.connections=[]
        #print(self.connections)
        self.cells.append(self)
        self.edge=False
        self.lines=[]
        self.lineSize=0
        self.availablecells=[]
        
        
    def connect(self,Other):
        if Other not in self.connections:
            self.connections.append(Other)
        if self not in Other.connections:
            Other.connections.append(self)
        
        #print("connected")

    def drawself(self):
        #pygame.draw.circle(screen,"Dark Green",self.pos,5)
        brehet=2
        for line in self.lines:
            #print(line[1])
            
            xMiddle =line[0][0]
            yMiddle =line[0][1]
            if line[1] == "v":
                Start=(xMiddle-self.lineSize,yMiddle)
                End=(xMiddle+self.lineSize,yMiddle)
                pygame.draw.line(screen,"black",Start,End,width=brehet)
            #pygame.draw.circle(screen,"black",line[0],2)
            if line[1] == "h":
                Start=(xMiddle,yMiddle-self.lineSize)
                End=(xMiddle,yMiddle+self.lineSize)
                pygame.draw.line(screen,"black",Start,End,width=brehet)
        #print(self.pos)
        
    def discoverWalls(self):
        shortestest=[]
        rubrik=0
        while len(shortestest) <4:
            shortest_value=999999
            potentiallyShortest=None
            for each in self.cells:
                xDis=each.pos[0]-self.pos[0]
                yDis=each.pos[1]-self.pos[1]
                hypo=math.sqrt(xDis**2+yDis**2)
                
                if each != self:
                    if each not in shortestest:
                        if hypo <= shortest_value:
                            shortest_value=hypo
                            potentiallyShortest=each
                            if len(shortestest)==0:
                                rubrik=math.sqrt((xDis/2)**2+(yDis/2)**2)
            shortestest.append(potentiallyShortest)
        #print(shortestest)
        #print(rubrik)
        leftovers=[0,0]
        for each in shortestest:
            DistanceX=(each.pos[0]-self.pos[0])/2
            DistanceY=(each.pos[1]-self.pos[1])/2
            #print(DistanceX,DistanceY)
            # Check for diagonaler
            
            if math.sqrt(DistanceX**2+DistanceY**2)-1 > rubrik:
                #print("EEEp")
                pass
            else:
                #print((self.pos[0]+DistanceX,self.pos[1]+DistanceY))

                direction=None
                if DistanceX**2 > DistanceY**2:
                    direction="h"
                else: 
                    direction="v"
                self.lines.append(((self.pos[0]+DistanceX,self.pos[1]+DistanceY),direction,each))
                leftovers[0]-=DistanceX
                leftovers[1]-=DistanceY
                self.availablecells.append(each)
        #print(leftovers)
        if leftovers[0] > 1 or leftovers[0] < -1:
            self.lines.append(((self.pos[0]+leftovers[0],self.pos[1]),"h",None))
        if leftovers[1] > 1 or leftovers[1] < -1:
            self.lines.append(((self.pos[0],self.pos[1]+leftovers[1]),"v",None))
        self.lineSize=rubrik

    
    def checkWalls(self):
        #print("checkin")
        for conec in self.connections:
            #print(len(self.connections))
            #print(conec)
            for each in self.lines:
                #print(each)
                if each[2] != None:
                    #print("Hmm")
                    if conec == each[2]:
                        self.lines.remove(each)
                        #print("popped")
            


class Maze:
    def __init__(self,xamount,yamount,start,stop):
        Xamount=stop[0]-start[0]
        Yamount=stop[1]-start[1]
        Xhop=Xamount/xamount #Okau, bad names, i agree
        Yhop=Yamount/yamount
        self.cells=[]
        self.previousCells=[]
        self.openings=[]
        
        for y in range(yamount):
            for x in range(xamount):
                #print(y,x)
                quare=Cell(self,x*Xhop+Xhop/2+start[0],y*Yhop+Yhop/2+start[1])
                self.cells.append(quare)
        self.currentcell=self.cells[0]
    def drawPoints(self):
        for cell in Cell.cells:
            if cell.owner == self:
                cell.drawself()
                
    def sustainWalls(self):
        for cell in Cell.cells:
            if cell.owner == self:
                cell.checkWalls()
        
    def update(self):
        self.drawPoints()
        self.sustainWalls()
    
    def progress(self):
        #print(len(self.currentcell.availablecells))
        opencell=[]
        for each in self.currentcell.availablecells:
            if len(each.connections) == 0:
                opencell.append(each)
        #print(opencell)
        if len(opencell)!=0:
            choice= random.choice(opencell)
            if len(choice.connections) == 0:
                self.previousCells.append(self.currentcell)
                self.currentcell.connect(choice)
                self.currentcell = choice
        else:
            for cell in reversed(self.previousCells):
                #print(cell)
                for each in cell.availablecells:
                    if len(each.connections) == 0:
                        self.currentcell = cell
                        break
                    
    def makeOpenings(self):
        print(len(self.openings))
        for each in self.openings:
            each[1].lines.append(each[0])
            print("Patched")
            
            #self.openings.remove(each)
        self.openings=[]
        edges=[]
        for cell in Cell.cells:
            for line in cell.lines:
                if line[2] == None:
                    edges.append(line)
        start = random.choice(edges)
        end = random.choice(edges)
        
        for cell in Cell.cells:
            for line in cell.lines:
                if line == start or line == end:
                    self.openings.append((line,cell))
                    cell.lines.remove(line)
        #print(start)
        print("")      
        
pygame.init()


screenie
screen = pygame.display.set_mode(screenie)
clock = pygame.time.Clock()
running = True

r=screenie[1]/2.1
length=40
Thypany=Maze(length,length,(screenie[0]/2 - r, screenie[1]/2 - r),(screenie[0]/2 + r, screenie[1]/2 + r))
#Cell.cells[1].discoverWalls()

for each in Cell.cells:
    each.discoverWalls()
dt = 0

currentTime=time.time()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Button 4 (usually back button on some mice)
                pass
            elif event.button == 5:  # Button 5 (usually forward button on some mice)
                pass
            elif event.button == 1: 
                Thypany.progress()
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        Thypany.progress()
    if keys[pygame.K_e]:
        if time.time()-currentTime >0.3:
            Thypany.makeOpenings()
            currentTime=time.time()
    if keys[pygame.K_r]:
        if time.time()-currentTime >0.3:
            Thypany.makeOpenings()
            currentTime=time.time()
    if keys[pygame.K_w]:
        if time.time()-currentTime >0.3:
            pass
            currentTime=time.time()
            
    
    
    screen.fill("white")
    Thypany.update()
   
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()