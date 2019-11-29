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
        self.fishAliveStatus == False

    def reversePos(self):

        """if the fish is in flee mode and hits a barrier, reversePos
        flips the fish across the grid"""

        if self.fishFleeStatus == True:

            if self.fishXCoord < 0:
                self.fishXCoord = 9

            elif self.fishXCoord > 9:
                self.fishXCoord = 0

            elif self.fishYCoord < 0:
                self.fishYCoord = 9

            elif self.fishYCoord > 9:
                self.fishYCoord = 0

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

    def setDirection(self,direction):
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

    def setDirection(self,sharkX,sharkY):

        self.sharkXCoord = sharkX
        self.sharkYCoord = sharkY

        if self.fishXCoord == self.sharkXCoord and self.fishYCoord == self.sharkYCoord:
            self.fishAliveStatus = False

        if self.fishAliveStatus == True:

            if self.fishFleeStatus == True:

                if self.fishYCoord == self.sharkYCoord:
                                            
                    if self.fishXCoord > self.sharkXCoord:
                        self.fishDirection,self.fishAltDirection = "east","DNE"

                    elif self.fishXCoord < self.sharkXCoord:
                        self.fishDirection,self.fishAltDirection = "west","DNE"

                elif self.fishXCoord == self.sharkXCoord:
                                            
                    if self.fishYCoord > self.sharkYCoord:
                        self.fishDirection,self.fishAltDirection = "north","DNE"

                    elif self.fishYCoord < self.sharkYCoord:
                        self.fishDirection,self.fishAltDirection = "south","DNE"

                else:

                    self.fishDirectionInt = randrange(1,3)

                    self.XDistance = abs(self.sharkXCoord - self.fishXCoord)
                    self.YDistance = abs(self.sharkYCoord - self.fishYCoord)

                    if (self.fishYCoord > self.sharkYCoord) and (self.fishXCoord > self.sharkXCoord):
                        #1st quadrant relative to shark, must move north or east

                        if self.XDistance < self.YDistance:
                            self.fishDirection,self.fishAltDirection = "north","DNE"
                        elif self.XDistance > self.YDistance:
                            self.fishDirection,self.fishAltDirection = "east","DNE"
                        else:                   
                            if self.fishDirectionInt == 1:
                                self.fishDirection,self.fishAltDirection = "north","east"
                            elif self.fishDirectionInt == 2:
                                self.fishDirection,self.fishAltDirection = "east","north"

                    elif (self.fishYCoord > self.sharkYCoord) and (self.fishXCoord < self.sharkXCoord):
                        #2nd quadrant relative to shark, must move north or west

                        if self.XDistance < self.YDistance:
                            self.fishDirection,self.fishAltDirection = "north","DNE"
                        elif self.XDistance > self.YDistance:
                            self.fishDirection,self.fishAltDirection = "west","DNE"
                        else:
                            if self.fishDirectionInt == 1:
                                self.fishDirection,self.fishAltDirection = "north","west"
                            elif self.fishDirectionInt == 2:
                                self.fishDirection,self.fishAltDirection = "west","north"

                    elif (self.fishYCoord < self.sharkYCoord) and (self.fishXCoord < self.sharkXCoord):
                        #3rd quadrant relative to shark, must move south or west

                        if self.XDistance < self.YDistance:
                            self.fishDirection,self.fishAltDirection = "south","DNE"
                        elif self.XDistance > self.YDistance:
                            self.fishDirection,self.fishAltDirection = "west","DNE"
                        else:
                            if self.fishDirectionInt == 1:
                                self.fishDirection,self.fishAltDirection = "south","west"
                            elif self.fishDirectionInt == 2:
                                self.fishDirection,self.fishAltDirection = "west","south"

                    elif (self.fishYCoord < self.sharkYCoord) and (self.fishXCoord > self.sharkXCoord):
                        #4th quadrant relative to shark, must move south or east

                        if self.XDistance < self.YDistance:
                            self.fishDirection,self.fishAltDirection = "south","DNE"
                        elif self.XDistance > self.YDistance:
                            self.fishDirection,self.fishAltDirection = "east","DNE"
                        else:
                            if self.fishDirectionInt == 1:
                                self.fishDirection,self.fishAltDirection = "south","east"
                            elif self.fishDirectionInt == 2:
                                self.fishDirection,self.fishAltDirection = "east","south"

    def move(self,distance):

        self.moveDistance = distance

        if self.fishAliveStatus == True:

            #translate direction into coordinate movement.

            if self.fishDirection == "east":
                self.fishXCoord += self.moveDistance
                self.fishYCoord += 0
                
            elif self.fishDirection == "north":
                self.fishXCoord += 0
                self.fishYCoord += self.moveDistance
                
            elif self.fishDirection == "west":
                self.fishXCoord += -self.moveDistance
                self.fishYCoord += 0

            elif self.fishDirection == "south":
                self.fishXCoord += 0
                self.fishYCoord += -self.moveDistance

    def collideSetDirection(self):

        if self.fishAltDirection != "DNE" and self.fishFleeStatus == True:

            self.fishDirection,self.fishAltDirection = self.fishAltDirection,self.fishDirection

        
