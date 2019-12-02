

if (self.fishYCoord > self.sharkYCoord) and (self.fishXCoord > self.sharkXCoord):
    directionList = ["north","east"]
elif (self.fishYCoord > self.sharkYCoord) and (self.fishXCoord < self.sharkXCoord):
    directionList = ["north","west"]
elif (self.fishYCoord < self.sharkYCoord) and (self.fishXCoord < self.sharkXCoord):
    directionList = ["south","west"]
elif (self.fishYCoord < self.sharkYCoord) and (self.fishXCoord > self.sharkXCoord):
    directionList = ["south","east"]

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

"""if (self.fishYCoord > self.sharkYCoord) and (self.fishXCoord > self.sharkXCoord):
        #1st quadrant relative to shark, must move north or east

        if self.XDistance < self.YDistance:
            self.fishDirection,self.fishAltDirection = "north","DNE"
        elif self.XDistance > self.YDistance:
            self.fishDirection,self.fishAltDirection = "east","DNE"
        else:
            if self.fishDirection != "north" and self.fishDirection != "east":
                if self.fishDirectionInt == 1:
                    self.fishDirection,self.fishAltDirection = "north","east"
                elif self.fishDirectionInt == 2:
                    self.fishDirection,self.fishAltDirection = "east","north"
                    
            elif self.fishDirection == "north":
                self.fishDirection,self.fishAltDirection = "north","east"
            elif self.fishDirection == "east":
                self.fishDirection,self.fishAltDirection = "east","north"

    elif (self.fishYCoord > self.sharkYCoord) and (self.fishXCoord < self.sharkXCoord):
        #2nd quadrant relative to shark, must move north or west

        if self.XDistance < self.YDistance:
            self.fishDirection,self.fishAltDirection = "north","DNE"
        elif self.XDistance > self.YDistance:
            self.fishDirection,self.fishAltDirection = "west","DNE"
        else:
            if self.fishDirection != "north" and self.fishDirection != "west":
                if self.fishDirection == "north" or self.fishDirectionInt == 1:
                    self.fishDirection,self.fishAltDirection = "north","west"
                elif self.fishDirection == "west" or self.fishDirectionInt == 2:
                    self.fishDirection,self.fishAltDirection = "west","north"

            elif self.fishDirection == "north":
                self.fishDirection,self.fishAltDirection = "north","west"
            elif self.fishDirection == "west":
                self.fishDirection,self.fishAltDirection = "west","north"

    elif (self.fishYCoord < self.sharkYCoord) and (self.fishXCoord < self.sharkXCoord):
        #3rd quadrant relative to shark, must move south or west

        if self.XDistance < self.YDistance:
            self.fishDirection,self.fishAltDirection = "south","DNE"
        elif self.XDistance > self.YDistance:
            self.fishDirection,self.fishAltDirection = "west","DNE"
        else:
            if self.fishDirection != "south"and self.fishDirection != "west":
                if self.fishDirectionInt == 1:
                    self.fishDirection,self.fishAltDirection = "south","west"
                elif self.fishDirectionInt == 2:
                    self.fishDirection,self.fishAltDirection = "west","south"
                    
            elif self.fishDirection == "south":
                self.fishDirection,self.fishAltDirection = "south","west"
            elif self.fishDirection == "west":
                self.fishDirection,self.fishAltDirection = "west","south"
                
    elif (self.fishYCoord < self.sharkYCoord) and (self.fishXCoord > self.sharkXCoord):
        #4th quadrant relative to shark, must move south or east

        if self.XDistance < self.YDistance:
            self.fishDirection,self.fishAltDirection = "south","DNE"
        elif self.XDistance > self.YDistance:
            self.fishDirection,self.fishAltDirection = "east","DNE"
        else:
            if self.fishDirection != "south"and self.fishDirection != "east":
                if self.fishDirectionInt == 1:
                    self.fishDirection,self.fishAltDirection = "south","east"
                elif self.fishDirectionInt == 2:
                    self.fishDirection,self.fishAltDirection = "east","south"
                    
            elif self.fishDirection == "south":
                self.fishDirection,self.fishAltDirection = "south","east"
            elif self.fishDirection == "east":
                self.fishDirection,self.fishAltDirection = "east","south"""""

for fishObjectInt in range(0,3):
                    
    if fishListObjects[fishObjectInt - 1].getX() == fishListObjects[fishObjectInt].getX() and fishListObjects[fishObjectInt - 1].getY() == fishListObjects[fishObjectInt].getY():
        if fishListObjects[fishObjectInt].getFlee() == True and fishListObjects[fishObjectInt].getAltDirection() == True:
            collideMove(fishListObjects[fishObjectInt])
        elif fishListObjects[fishObjectInt - 1].getFlee() == True and fishListObjects[fishObjectInt - 1].getAltDirection() == True:
            collideMove(fishListObjects[fishObjectInt - 1])
        else: #CHECK THIS AGAINST SPECS
            fishListObjects[fishObjectInt].move(-1)

"""if fish1.getX() == fish3.getX() and fish1.getY() == fish3.getY():
    if fish1.getFlee() == True and fish1.getAltDirection() == True:
        collideMove(fish1)
    elif fish3.getFlee() == True and fish3.getAltDirection() == True:
        collideMove(fish2)
    else: #CHECK THIS AGAINST SPECS
        fish1.move(-1)

if fish3.getX() == fish2.getX() and fish3.getY() == fish2.getY():

    if fish3.getFlee() == True and fish3.getAltDirection() == True:
        collideMove(fish3)
    elif fish2.getFlee() == True and fish2.getAltDirection() == True:
        collideMove(fish2)
    else: #CHECK THIS AGAINST SPECS
        fish2.move(-1)"""




