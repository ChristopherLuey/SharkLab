#File: Fish.py
#Written By: Andreas Petrou-Zeniou
#Date: 12/12/19
#Handles all individual fish movement (collision interactions are handled
#within SharkRunner.) Handles movement on a theoretical 10x10 plane.

import math
from random import randrange

class Fish:

    def __init__(self,x,y):

        #convert to self. form

        self.fishXCoord = x
        self.fishYCoord = y
        self.fishDirection = "DNE"
        self.fishFleeStatus = False
        self.fishAliveStatus = True
        self.fishWallHittingStatus = False
        self.fishAltDirection = "DNE"

        #use to randomly assign direction at beginning of game

        self.directionInt = randrange(1,4)

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

        #returns alternate direction in diagonal flee situation
        
        if self.fishAltDirection != "DNE":
            return True
        else:
            return False

    def getCoords(self):
        
        #returns coordinates
        
        return self.fishXCoord,self.fishYCoord

    def getX(self):

        #returns xCoord
        
        return self.fishXCoord

    def getY(self):

        #return yCoord
        
        return self.fishYCoord

    def getDirection(self):

        #returns direction fish is facing
        
        return self.fishDirection

    def getFlee(self):

        #returns fish Flee Status
        
        return self.fishFleeStatus

    def getAlive(self):

        #returns whether or not a fish is alive
        
        return self.fishAliveStatus

    def getWallHitting(self):

        #detects if a fish is hitting a wall, if so, return True, else, return False

        if ((self.fishXCoord < 0 or self.fishXCoord > 9) or (self.fishYCoord < 0 or self.fishYCoord > 9)):
            self.fishWallHittingStatus = True
        else:
            self.fishWallHittingStatus = False

        return self.fishWallHittingStatus

    #mutators
        
    def eat(self,sharkX,sharkY):

        #kills the fish after detecting whether it shares its coordinates with a shark

        self.sharkXCoord = sharkX
        self.sharkYCoord = sharkY

        if self.fishXCoord == self.sharkXCoord and self.fishYCoord == self.sharkYCoord:
        
            self.fishAliveStatus = False
            self.setCoords(11,11)

    def reversePos(self):

        #reversePos flips the fish across the grid.
        #useful when the fish is in flee mode and
        #has to flip across the grid in a wall
        #hitting situation


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

        #detects distance to shark. If less than or equal to three squares (there is 7 x 7 square zone
        #where flee occurs, centered around the shark), fish enters flee mode. Additionally, fish
        #will exit a head on collision if they enter flee mode.
    
        self.sharkXCoord = sharkX
        self.sharkYCoord = sharkY

        if (0 <= abs(self.sharkXCoord - self.fishXCoord) <= 3) and (0 <= abs(self.sharkYCoord - self.fishYCoord) <= 3):
            self.fishFleeStatus = True

        else:
            self.fishFleeStatus = False
            
    def setCoords(self,x,y):

        #allows tester to manually set the coordinates of fish in sharkRunner.
        
        self.fishXCoord = x
        self.fishYCoord = y

    def setInputDirection(self,direction):

        #allows tester to manually set the direction of fish in sharkRunner.
        
        self.fishDirection = direction

    def directionReverse(self):

        #reverses fish direction

        if self.fishDirection == "east":
            self.fishDirection = "west"

        elif self.fishDirection == "north":
            self.fishDirection = "south"

        elif self.fishDirection == "west":
            self.fishDirection = "east"

        elif self.fishDirection == "south":
            self.fishDirection = "north"

    def setDirection(self,sharkX,sharkY):

        #detects if fish is in flee mode, selects appropriate direction as such.

        self.sharkXCoord = sharkX
        self.sharkYCoord = sharkY
        
        if self.fishAliveStatus == True and self.fishFleeStatus == True:

            #fish direction if fish is on same axis as shark. IF the fish, for example, is above
            #the shark on the frid, its direction will set to north

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

                #situation if fish is in flee, and not on an axis with the shark

                #use this line for random assignment of direction

                self.fishDirectionInt = randrange(1,3)

                #calculate distance between fish and shark on different axes. 

                self.XDistance = abs(self.sharkXCoord - self.fishXCoord)
                self.YDistance = abs(self.sharkYCoord - self.fishYCoord)

                #calculate fish' quadrant based on relationship of fish to shark. for example, if the fish is north
                #and east of the shark, it is in the first quadrant, and the two directions it can possibly move are
                #north and east. These two directions are stored in 

                if (self.fishYCoord > self.sharkYCoord) and (self.fishXCoord > self.sharkXCoord):
                    self.directionList = ["south","east"]
                elif (self.fishYCoord > self.sharkYCoord) and (self.fishXCoord < self.sharkXCoord):
                    self.directionList = ["south","west"]
                elif (self.fishYCoord < self.sharkYCoord) and (self.fishXCoord < self.sharkXCoord):
                    self.directionList = ["north","west"]
                elif (self.fishYCoord < self.sharkYCoord) and (self.fishXCoord > self.sharkXCoord):
                    self.directionList = ["north","east"]

                #calculate which side of the quadrant it is. To carry on with the previous example, the fish has two options
                #north and east. if the fish is further from the shark on the X axis, it will move east. Otherwise, it moves
                #north.

                if self.XDistance < self.YDistance:
                    self.fishDirection,self.fishAltDirection = self.directionList[0],"DNE"
                elif self.XDistance > self.YDistance:
                    self.fishDirection,self.fishAltDirection = self.directionList[1],"DNE"

                #diagonal situation
                else:

                    #if fish is not facing in the flee direction, and must change, direction is randomly assigned.
                    
                    if self.fishDirection != self.directionList[0] and self.fishDirection != self.directionList[1]:
                        if self.fishDirectionInt == 1:
                            self.fishDirection,self.fishAltDirection = self.directionList[0],self.directionList[1]
                        elif self.fishDirectionInt == 2:
                            self.fishDirection,self.fishAltDirection = self.directionList[1],self.directionList[0]

                    #otherwise, it defaults to its original direction.
                            
                    elif self.fishDirection == self.directionList[0]:
                        self.fishDirection,self.fishAltDirection = self.directionList[0],self.directionList[1]
                    elif self.fishDirection == self.directionList[1]:
                        self.fishDirection,self.fishAltDirection = self.directionList[1],self.directionList[0]

    def move(self,distance):

        self.moveDistance = distance

        if self.fishAliveStatus == True:

            #translate direction into coordinate movement.

            if self.fishDirection == "east":
                self.fishXCoord += self.moveDistance
                
            elif self.fishDirection == "north":
                self.fishYCoord += -self.moveDistance
                
            elif self.fishDirection == "west":
                self.fishXCoord += -self.moveDistance

            elif self.fishDirection == "south":
                self.fishYCoord += self.moveDistance

    def collideSetDirection(self):

        #replace altDirection with direction. Use in case a fish is on a diagonal, and collides upon flee movement.
        #this allows the fish to switch directions to its alternate.

        if self.fishAltDirection != "DNE" and self.fishFleeStatus == True:

            self.fishDirection,self.fishAltDirection = self.fishAltDirection,self.fishDirection

    def collideMove(self):

        #sequence of movements if fish has two movement options (on a diagonal with the shark) in case fish collides

        self.directionReverse()
        self.move(1)
        self.collideSetDirection()
        self.move(1)

    def wallHitting(self,sharkX,sharkY,string):

        self.string = string

        #wall hitting scenario. If in flee, fish flips across grid. Otherwise, initiates wall bump sequence.

        #if the fish hits the wall and is not in flee mode, the fish will reverse direction and move one square in the GUI

        if self.getWallHitting() ==  True and self.getFlee() == False and self.string != "flipped":
            self.directionReverse()
            self.move(2)
            return("notFlipped")

        #if the fish hits the wall and is in flee mode, the fish will flip across the grid
            
        elif self.getWallHitting() ==  True and self.getFlee() == True:
            self.reversePos()
            return("flipped")

        #use these lines to flip fish back across the board if it is in a collision scenario
        
        if self.string == "flipped" and self.getWallHitting() == True:
            self.reversePos()
            self.setFlee(sharkX,sharkY)
            self.setDirection(sharkX,sharkY)
            return("")



  
