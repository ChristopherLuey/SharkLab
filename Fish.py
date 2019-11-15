#File: Fish.py

from graphics import *
import math
from random import randrange

class Fish:

    def __init__(self,x,y,direction,flee,alive,wallHitting,win):

        #convert to self. form

        self.fishXCoord = x
        self.fishYCoord = y
        self.fishDirection = direction
        self.fishFleeStatus = flee
        self.fishAliveStatus = alive
        self.fishWallHittingStatus = wallHitting
        self.window = win

        self.anchorPoint = Point(self.fishXCoord,self.fishYCoord)

    #accessors

    def getCoords(self):
        return Point(self.fishXCoord,self.fishYCoord)

    def getDirection(self):
        return self.fishDirection

    def getFlee(self):
        return self.fishFleeStatus

    def getAlive(self):
        return self.fishAliveStatus

    def getWallHitting(self):
        return self.fishWallHittingStatus

    #mutators

    def setFlee(self,sharkX,sharkY):
        
        self.sharkXCoord = sharkX
        self.sharkYCoord = sharkY

        if (0 < abs(self.sharkXCoord - self.fishXCoord) <= 3) and (0 < abs(self.sharkYCoord - self.fishYCoord) <= 3):
            self.fishFleeStatus = True

        else:
            self.fishFleeStatus = True
            
    def setCoords(self,x,y):
        self.fishXCoord = x
        self.fishYCoord = y

        self.anchorPoint = Point(self.fishXCoord,self.fishYCoord)

    def setDirection(self,direction):
        self.fishDirection = direction

    def setWallHitting(self):
        
        if (self.fishXCoord < 0 and self.fishXCoord > 9) or (self.fishYCoord < 0 and self.fishYCoord > 9):
            self.fishWallHittingStatus = True
        else:
            self.fishWallHittingStatus = False

    def directionReverse(self):

        if self.fishDirection == "east":
            self.fishDirection = "west"

        elif self.fishDirection == "north":
            self.fishDirection = "south"

        elif self.fishDirection == "west":
            self.fishDirection = "east"

        elif self.fishDirection == "south":
            self.fishDirection = "north"

    def move(self,sharkX,sharkY,distance):

        self.sharkXCoord = sharkX
        self.sharkYCoord = sharkY
        self.moveDistance = distance

        if self.fishFleeStatus == False:

            if self.fishDirection == "east":
                self.xCoord += self.moveDistance
                self.yCoord += 0
                
            elif self.fishDirection == "north":
                self.xCoord += 0
                self.yCoord += self.moveDistance
                
            elif self.fishDirection == "west":
                self.xCoord += -self.moveDistance
                self.yCoord += 0

            elif self.fishDirection == "south":
                self.xCoord += 0
                self.yCoord += -self.moveDistance

        elif self.fishFleeStatus == True:

            if self.fishYCoord == self.sharkYCoord:
                if self.fishXCoord > self.sharkXCoord:
                    
                    self.fishDirectionInt = randrange(1,4)

                    if self.fishDirectionInt == 1:
                        self.fishDirection = "north"
                    elif self.fishDirectionInt == 2:
                        self.fishDirection = "east"
                    elif self.fishDirectionInt == 3:
                        self.fishDirection = "south"

                    

                if self.fishXCoord < self.sharkXCoord:
                    
                    self.fishDirectionInt = randrange(1,4)

                    if self.fishDirectionInt == 1:
                        self.fishDirection = "north"
                    elif self.fishDirectionInt == 2:
                        self.fishDirection = "east"
                    elif self.fishDirectionInt == 3:
                        self.fishDirection = "south"

                
                    

            

            
            

        

    






        
