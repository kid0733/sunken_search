'''Part 1: Importing Modules'''
import sys
import random
import itertools
import numpy as np
import cv2 as cv

#Creating Global Scope Var
MAP_FILE= 'cape_python.png'

#SA=SearchArea | UL=UpperLeft || LR=BottomLeft | 
SA1_CORNERS=(130,265,180,315) #(UL-x, UL-y, LR-x, LR-y)
SA2_CORNERS=(80,255,130,305) #(UL-x, UL-y, LR-x, LR-y)
SA3_CORNERS=(105,205,155,255) #(UL-x, UL-y, LR-x, LR-y)

'''Part 2: Search Functions'''
#Search Class:
class Search():
    '''Bayesian Search & Rescue game with 3 search areas.'''

    def __init__(self,name):
        self.name=name

        self.img=cv.imread(MAP_FILE, cv.IMREAD_COLOR)
        #error handle: if file NULL
        if self.img is None:
            print('Could not load map map file {}'.format(MAP_FILE),file=sys.stderr)
            sys.exit(1)
        '''Location when found'''
        
        self.area_actual=0 #This is the number of the search area (SA box)
        self.sailor_actual=[0,0] #This is the co-ordinates of the sailor
    
        '''Search Area Default Values'''
        self.sa1=self.img[
            SA1_CORNERS[1]:SA1_CORNERS[2], #index relative to the placeholder tuple above
            SA1_CORNERS[0]:SA1_CORNERS[3]
        ]
        self.sa2=self.img[
            SA2_CORNERS[1]:SA2_CORNERS[2],
            SA2_CORNERS[0]:SA2_CORNERS[3]
        ]
        self.sa3=self.img[
            SA3_CORNERS[1]:SA3_CORNERS[2],
            SA3_CORNERS[0]:SA3_CORNERS[3]
        ]

        self.p1=0.2
        self.p2=0.5
        self.p3=0.3

        self.sep1=0
        self.sep2=0
        self.sep3=0

    def draw_map(self,last_known):
        '''Display basemap with: scale | last known (x,y) location | search areas'''
        cv.line(self.img(20,370),(70,370), (0, 0, 0), 2)
        cv.putText(self.img, '0', (8,370), cv.FONT_HERSHEY_PLAIN, 1, (0,0,0))
        cv.putText(self.img,'50 Nautical Miles',(71,370), cv.FONT_HERSHEY_PLAIN, 1, (0,0,0))
        #First Search box + search box text
        cv.rectangle(self.img, (SA1_CORNERS[1], SA1_CORNERS[2],SA1_CORNERS[0],SA1_CORNERS[3]),(0,0,0),1)
        cv.putText(self.img, '1',(SA1_CORNERS[0]+3,SA1_CORNERS[1]+15),cv.FONT_HERSHEY_PLAIN,1,0)
        #Second Search box + search box text
        cv.rectangle(self.img, (SA2_CORNERS[1], SA2_CORNERS[2],SA2_CORNERS[0],SA2_CORNERS[3]),(0,0,0),1)
        cv.putText(self.img, '1',(SA2_CORNERS[0]+3,SA2_CORNERS[1]+15),cv.FONT_HERSHEY_PLAIN,1,0)
        #Third Search box + search box text
        cv.rectangle(self.img, (SA3_CORNERS[1], SA3_CORNERS[2],SA3_CORNERS[0],SA3_CORNERS[3]),(0,0,0),1)
        cv.putText(self.img, '1',(SA3_CORNERS[0]+3,SA3_CORNERS[1]+15),cv.FONT_HERSHEY_PLAIN,1,0)

        #Displaying last known position cross (CV has BGR color Format)
        cv.putText(self.img, '+', (last_known),cv.FONT_HERSHEY_PLAIN,1,(0,0,255))
        
        #Displaying Symbol Legend
        cv.putText(self.img, '+ : Last Known Position', (274,355),cv.FONT_HERSHEY_PLAIN,1,(0,0,255))
        cv.putText(self.img, '* : Actual Postion', (275, 370),cv.FONT_HERSHEY_PLAIN,1,(255,0,0))

        cv.imshow('Search Area', self.img)
        cv.moveWindow('Search Area', 750, 10)
        cv.waitKey(500)