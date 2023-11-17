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
    #Drawing Game Map
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
    
    def sailor_final_location(self, num_search_areas):
        """Return the actual x,y location of the missing person"""
        #Find sailor coordinates with respect to any search area subarray
        #Find the random generated x value [upper_limit=self.sa1.shape[1]] 
        self.sailor_actual[0]=np.random.choice(self.sa1.shape[1],1)
        #Find the random generated y value [upper_limit=self.sa1.shape[0]] 
        self.sailor_actual[1]=np.random.choice(self.sa1.shape[0],1)

        #We are using triangular distribution to return the location of the sailor
        #since we dont actually know the real-life distribution of thsi scenario
        area=int(random.triangular(1,num_search_areas+1))

        #if area generated = 1
        if area==1:
            x=self.sailor_actual[0]+ SA1_CORNERS[0]
            y=self.sailor_actual[1]+ SA1_CORNERS[1]
            self.area_actual=1
        
        #if area generated = 2
        elif area==2:
            x=self.sailor_actual[0]+ SA2_CORNERS[0]
            y=self.sailor_actual[1]+ SA2_CORNERS[1]
            self.area_actual=2
        elif area==3:
            x=self.sailor_actual[0]+ SA3_CORNERS[0]
            y=self.sailor_actual[1]+ SA3_CORNERS[1]
            self.area_actual=3

        return x,y

    def calc_search_effectiveness(self):
        """Calculate the random SEP """
        self.sep1=random.uniform(0.2,0.9)
        self.sep2=random.uniform(0.2,0.9)
        self.sep3=random.uniform(0.2,0.9)
    
    def conduct_search(self, area_num, area_array, effectiveness_prob):
        """Return search results and list of searched coordinates."""
        local_y_range=range(area_array.shape[0])
        local_x_range=range(area_array.shape[1])
        coords=list(itertools.product(local_x_range,local_y_range))
        random.shuffle(coords)
        coords=coords[:int((len(coords)*effectiveness_prob))]
        loc_actual=(self.sailor_actual[1],self.sailor_actual[0])
        #Case = found area of the sailor
        if area_num==self.area_actual and loc_actual in coords:
            return "Found in area {}".format(area_num), coords
        #Case = Wrong Area
        else:
            return 'Not Found',coords
        
    def revise_target_probs(self):
        """Update area target probabilities based of search effectiveness"""
        denom=self.p1*(1-self.sep1)+self.p2*(1-self.sep2)+self.p3*(1-self.sep3)
        self.p1=self.p1*(1-self.sep1)/denom
        self.p2=self.p2*(1-self.sep2)/denom
        self.p3=self.p3*(1-self.sep3)/denom

    def draw_menu(search_num):
        """Print Menu for Area Searches"""
        print('\nSearch {}'.format(search_num))
        print(
            """
            Choose next areas to search:

            0 - Quit
            1 - Search Area 1 twice
            2 - Search Area 2 twice
            3 - Search Area 3 twice
            4 - Search Areas 1 & 2
            5 - Search Areas 1 & 3
            6 - Search Areas 2 & 3
            7 - Start Over
            """
            )
    def main():
        app=Search('cape_python')
        app.draw_map(last_known=(160,290))
        sailor_x, sailor_y = app.sailor_final_location(num_search_areas=3)
        print("-" * 65)
        print("\nInitial Target (P) Probabilities:")
        print("P1 = {:.3f}, P2 = {:.3f}, P3 = {:.3f}".format(app.p1, app.p2, app.p3))
        search_num = 1
        