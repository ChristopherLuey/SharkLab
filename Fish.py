#File: Fish.py

import math
from random import randrange

class Fish:

    def __init__(self,x,y,direction,flee,alive,wallHitting,altDirection):

        #convert to self. form

        self.fishXCoord = x
        self.fishYCoord = y
        self.fishDirection = direction
        self.fishFleeStatus = flee
        self.fishAliveStatus = alive
        self.fishWallHittingStatus = wallHitting
        self.fishAltDirection = altDirection

        self.directionInt = randrange(1,5)

        if self.directionInt == 1:
            self.fishDirection = "west"
        elif self.directionInt == 2:
            self.fishDirection = "east"
        elif self.directionInt == 3:
            self.fishDirection = "north"
        elif self.directionInt == 3:
            self.fishDirection = "south"

    #accessors

    def getAltDirection(self):
        if self.fishAltDirection != "DNE":
            return True
        else:
            return False

    def getCoords(self):
        return self.fishXCoord,self.fishYCoord

    def getX(self):
        return self.fishXCoord

    def getY(self):
        return self.fishYCoord

    def getDirection(self):
        return self.fishDirection

    def getFlee(self):
        return self.fishFleeStatus

    def getAlive(self):
        return self.fishAliveStatus

    def getWallHitting(self):

        if ((self.fishXCoord < 0 or self.fishXCoord > 9) or (self.fishYCoord < 0 or self.fishYCoord > 9)):
            self.fishWallHittingStatus = True
        else:
            self.fishWallHittingStatus = False

        return self.fishWallHittingStatus

    #mutators
        
    def eat(self):
        self.fishAliveStatus = False

    def reversePos(self):

        """if the fish is in flee mode and hits a barrier, reversePos
        flips the fish across the grid"""

        if self.fishFleeStatus == True:

            if self.fishXCoord < 0:
                self.fishXCoord = 9
                self.fishDirection = "west"

            elif self.fishXCoord > 9:
                self.fishXCoord = 0
                self.fishDirection = "east"

            elif self.fishYCoord < 0:
                self.fishYCoord = 9
                self.fishDirection = "north"

            elif self.fishYCoord > 9:
                self.fishYCoord = 0
                self.fishDirection = "south"

        self.fishFleeStatus = False

    def setFlee(self,sharkX,sharkY):
        
        self.sharkXCoord = sharkX
        self.sharkYCoord = sharkY

        if (0 <= abs(self.sharkXCoord - self.fishXCoord) <= 3) and (0 <= abs(self.sharkYCoord - self.fishYCoord) <= 3):
            self.fishFleeStatus = True

        else:
            self.fishFleeStatus = False
            
    def setCoords(self,x,y):
        self.fishXCoord = x
        self.fishYCoord = y

        self.anchorPoint = Point(self.fishXCoord,self.fishYCoord)

    def setInputDirection(self,direction):
        self.fishDirection = direction

    def setWallHitting(self):
        
        if (self.fishXCoord < 0 or self.fishXCoord > 9) or (self.fishYCoord < 0 or self.fishYCoord > 9):
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

    def wallSetDirection(self):

        if self.fishYCoord < 0:
            self.fishDirection = "south"
            
        elif self.fishYCoord > 9:
            self.fishDirection = "north"
            
        elif self.fishXCoord < 0:
            self.fishDirection = "east"
            
        elif self.fishXCoord > 9:
            self.fishDirection = "west"


    def setDirection(self,sharkX,sharkY):

        self.sharkXCoord = sharkX
        self.sharkYCoord = sharkY

        if self.sharkXCoord == self.fishXCoord and self.sharkYCoord == self.fishYCoord:
            self.fishAliveStatus = False

        if self.fishAliveStatus == True and self.fishFleeStatus == True:

            if self.fishYCoord == self.sharkYCoord:                                         
                if self.fishXCoord > self.sharkXCoord:
                    self.fishDirection,self.fishAltDirection = "east","DNE"
                elif self.fishXCoord < self.sharkXCoord:
                    self.fishDirection,self.fishAltDirection = "west","DNE"
                    
            elif self.fishXCoord == self.sharkXCoord:                    
                if self.fishYCoord > self.sharkYCoord:
                    self.fishDirection,self.fishAltDirection = "south","DNE"
                elif self.fishYCoord < self.sharkYCoord:
                    self.fishDirection,self.fishAltDirection = "north","DNE"

            else:

                self.fishDirectionInt = randrange(1,3)

                self.XDistance = abs(self.sharkXCoord - self.fishXCoord)
                self.YDistance = abs(self.sharkYCoord - self.fishYCoord)

                if (self.fishYCoord > self.sharkYCoord) and (self.fishXCoord > self.sharkXCoord):
                    directionList = ["south","east"]
                elif (self.fishYCoord > self.sharkYCoord) and (self.fishXCoord < self.sharkXCoord):
                    directionList = ["south","west"]
                elif (self.fishYCoord < self.sharkYCoord) and (self.fishXCoord < self.sharkXCoord):
                    directionList = ["north","west"]
                elif (self.fishYCoord < self.sharkYCoord) and (self.fishXCoord > self.sharkXCoord):
                    directionList = ["north","east"]

                if self.XDistance < self.YDistance:
                    self.fishDirection,self.fishAltDirection = directionList[0],"DNE"
                elif self.XDistance > self.YDistance:
                    self.fishDirection,self.fishAltDirection = directionList[1],"DNE"
                else:
                    if self.fishDirection != directionList[0] and self.fishDirection != directionList[1]:
                        if self.fishDirectionInt == 1:
                            self.fishDirection,self.fishAltDirection = directionList[0],directionList[1]
                        elif self.fishDirectionInt == 2:
                            self.fishDirection,self.fishAltDirection = directionList[1],directionList[0]
                            
                    elif self.fishDirection == directionList[0]:
                        self.fishDirection,self.fishAltDirection = directionList[0],directionList[1]
                    elif self.fishDirection == directionList[1]:
                        self.fishDirection,self.fishAltDirection = directionList[1],directionList[0]

    def move(self,distance):

        self.moveDistance = distance

        if self.fishAliveStatus == True:

            #translate direction into coordinate movement.

            if self.fishDirection == "east":
                self.fishXCoord += self.moveDistance
                self.fishYCoord += 0
                
            elif self.fishDirection == "north":
                self.fishXCoord += 0
                self.fishYCoord += -self.moveDistance
                
            elif self.fishDirection == "west":
                self.fishXCoord += -self.moveDistance
                self.fishYCoord += 0

            elif self.fishDirection == "south":
                self.fishXCoord += 0
                self.fishYCoord += self.moveDistance

    def collideSetDirection(self):

        if self.fishAltDirection != "DNE" and self.fishFleeStatus == True:

            self.fishDirection,self.fishAltDirection = self.fishAltDirection,self.fishDirection

        
