#File: Fish.py

from graphics import *

class Fish:

    def __init__(self,x,y,direction,flee,alive,wallHitting,win):

        #convert to self. form

        self.xCoord = x
        self.yCoord = y
        self.fishDirection = direction
        self.fishFleeStatus = flee
        self.fishAliveStatus = alive
        self.fishWallHittingStatus = wallHitting
        self.window = win

        self.anchorPoint = Point(self.xCoord,self.yCoord)

    def getCoords(self):
        return Point(self.xCoord,self.yCoord)

    def getDirection(self):
        return self.fishDirection

    def getFlee(self):
        return self.fishFleeStatus

    def getAlive(self):
        return self.fishAliveStatus

    def getWallHitting(self):
        return self.fishWallHittingStatus






        
