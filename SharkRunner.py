#File: SharkRunner.py
#Written by: Andreas Petrou-Zeniou
#Date: 12/10/19
#executes movement of fish and shark, communicates with GUI to draw on 10x10 grid

from SharkGUI import *
from Fish import *
from Shark import *

def directionRel(fish1,fish2):

    #function directionRel returns the relationship of the directions of two fish, whether they are opposite of each other or the same,
    #and whether the fish are moving on the x or y axis.

    fish1direction = fish1.getDirection()
    fish2direction = fish2.getDirection()

    #if the direction is the same, returns same
    
    if fish1direction == fish2direction:
        return "same",""

    #returns if fish are opposite each other, and the axis they are on

    else:
        if fish1direction == "west" and fish2direction == "east" or fish1direction == "east" and fish2direction == "west":
                return "opposite","x"

        elif fish1direction == "north" and fish2direction == "south" or fish1direction == "south" and fish2direction == "north":
                return "opposite","y"

    #if no special relation, returns empty strings

    return "",""

def getFishList(fish1,fish2,fish3):
    #returns a list of fish data to be inputed into the GUI, which updates the graphic representations of fish
    return [fish1.getX(),fish1.getY(),fish1.getDirection(),fish1.getFlee(),fish1.getAlive(),fish2.getX(),fish2.getY(),fish2.getDirection(),fish2.getFlee(),fish2.getAlive(),fish3.getX(),fish3.getY(),fish3.getDirection(),fish3.getFlee(),fish3.getAlive()]

def collideMove(fish):

    #sequence of movements if fish has two movement options (on a diagonal with the shark) in case fish collides
    
    fish.directionReverse()
    fish.move(1)
    fish.collideSetDirection()
    fish.move(1)

def wallHitting(fishObject,sharkX,sharkY,string):

    #wall hitting scenario. If in flee, fish flips across grid. Otherwise, initiates wall bump sequence.

    #if the fish hits the wall and is not in flee mode, the fish will reverse direction and move one square in the GUI

    if fishObject.getWallHitting() ==  True and fishObject.getFlee() == False and string != "flipped":
        fishObject.directionReverse()
        fishObject.move(2)
        return("notFlipped")

    #if the fish hits the wall and is in flee mode, the fish will flip across the grid
        
    elif fishObject.getWallHitting() ==  True and fishObject.getFlee() == True:
        fishObject.reversePos()
        return("flipped")
    
    if string == "flipped" and fishObject.getWallHitting() == True:
        fishObject.reversePos()
        return("")

def collisionScenario(fish1,fish2,fish3,roundFish):

    if roundFish.getAlive() == True:

        #generate list of alive fish that are not the roundFish (the fish that is moving)

        oldFishList = [fish1,fish2,fish3]
        fishList = []

        for fish in oldFishList:
            if fish != roundFish and fish.getAlive() == True:
                fishList.append(fish)

        #use collisionRound to test whether fish is in a flee diagonal and is blocked in both directions

        collisionRound = 0

        #iterate through each alive fish, check if there is a collision, check if the fish has an alternate direction,
        #and then move accordingly. If in flee diagonal, fish chooses altDirection. Otherwise, it moves back one spot.

        for collideFish in fishList:

            if roundFish.getX() == collideFish.getX() and roundFish.getY() == collideFish.getY():

                if roundFish.getFlee() == True and roundFish.getAltDirection() == True and collisionRound != 0:
                    collideMove(roundFish)
                    collisionRound += 1
                else:
                    roundFish.move(-1)
                    
def main():

    #set up GUI, gather user input to feed into subsequent fish object constructor
        
    GUI = SharkGUI()
    GUIList = GUI.gatherUserInput()
    statusList = [] #pass through fishWinTest in order to detect 3 win situation

    looping = True
    while looping == True:

        fishWins = 0 # use this variable to delay fish win message, accumulator variable

        if GUIList == []: #use this if statement to ensure that quit does not lead to error if start is not clicked
            looping = False
            break

        elif GUIList != []:
        
            fish1 = Fish(GUIList[0],GUIList[1],"west",False,True,False,"DNE")
            fish2 = Fish(GUIList[5],GUIList[6],"west",False,True,False,"DNE")
            fish3 = Fish(GUIList[10],GUIList[11],"west",False,True,False,"DNE")
            fishListObjects = [fish1,fish2,fish3] #use this list to efficiently cycle through fish objects in repetitive sequences, order is 1, 2, 3

            #construct shark, gather coordinates to set flee status of each fish, then set direction as well
            
            shark = Shark()
            sharkX,sharkY = shark.getPosition()

            for fishObject in fishListObjects:
                fishObject.setFlee(sharkX,sharkY)
                fishObject.setDirection(sharkX,sharkY)

            #update GUI to reflect these changes
            
            fishList = getFishList(fish1,fish2,fish3)
            GUI.updateFish(fishList)

            #loop through button clicking

            while True:

                buttonClicked = GUI.isClicked()
                
                if buttonClicked == "fish":

                    sharkList = shark.getSharkList()
                    sharkX,sharkY = shark.getPosition()
                    
                    #move procedure    
                    for fishObject in fishListObjects: 
                        
                        fishObject.setFlee(sharkX,sharkY)
                        fishObject.setDirection(sharkX,sharkY)
                        fishObject.move(1)
                        #wall hitting scenario. If in flee, fish flips across grid. Otherwise, initiates wall bump sequence.
                        inputString = wallHitting(fishObject,sharkX,sharkY,"")
                        #collisions scenario, do after every round to ensure valid order
                        collisionScenario(fish1,fish2,fish3,fishObject)

                        #ensure that fish is not collided when it flips across grid
                        wallHitting(fishObject,sharkX,sharkY,inputString)

                        fishObject.setFlee(sharkX,sharkY)
                        fishObject.setDirection(sharkX,sharkY)

                    fishList = getFishList(fish1,fish2,fish3)
                    GUI.updateFish(fishList)
                    GUI.nextTurn()

                    #fish Win situation, fishWin delays display of fish victory

                    if fishWinTest(fish1,fish2,fish3,sharkX,sharkY,statusList) == True:
                        fishWins += 1
                        if fishWins == 3:
                            GUIList = GUI.winner("fish")
                            break

                elif buttonClicked == "shark":
                    fishList = getFishList(fish1,fish2,fish3)

                    #move shark

                    shark.sharkTurn(fishList)
                    sharkList = shark.getSharkList()
                    sharkX,sharkY = shark.getPosition()

                    #eat fish

                    for fishObject in fishListObjects:
                        if sharkX == fishObject.getX() and sharkY == fishObject.getY() and fishObject.getAlive() == True:
                            fishObject.eat()
                            fishObject.setCoords(11,11) #use to avoid collisions after fish death

                    #update GUI
                            
                    GUI.updateShark(sharkList)
                    GUI.updateFish(fishList)
                    GUI.nextTurn()

                    #shark win situation

                    if fish3.getAlive() == False and fish1.getAlive() == False and fish2.getAlive() == False:
                        GUIList = GUI.winner("shark")
                        break

                #close window if quit is pressed, and cease execution of program via breaks

                elif buttonClicked == "quit":
                    GUI.endGame()
                    looping = False
                    break
        
main()

def getAliveList(fish1,fish2,fish3):

    #test each fish for alive status, and if so, add them to a list of alive fish. fishWin tracks the status of the fish winning throughout the module

    deadNumber = 0
    aliveFishList = []
    allFishList = [fish1,fish2,fish3]

    for fish in allFishList:
        if fish.getAlive() == False:
            deadNumber += 1
        else:
            aliveFishList.append(fish)

    return deadNumber,aliveFishList

def fish2WinTest(aliveFishList,sharkX,sharkY):

    fishWin = False

    gap = False

    if aliveFishList[0].getX() == sharkX or aliveFishList[1].getX() == sharkX or aliveFishList[0].getY() == sharkY or aliveFishList[1].getY() == sharkY:

        #set index of center fish to index 0

        if aliveFishList[0].getX() == sharkX or aliveFishList[0].getY() == sharkY and (aliveFishList[1].getY() != sharkY and aliveFishList[1].getX() != sharkX):
            aliveFishList[0],aliveFishList[1] = aliveFishList[0],aliveFishList[1]
            
        elif aliveFishList[1].getX() == sharkX or aliveFishList[1].getY() == sharkY and (aliveFishList[0].getY() != sharkY and aliveFishList[0].getX() != sharkX):
            aliveFishList[0],aliveFishList[1] = aliveFishList[1],aliveFishList[0]

        #situation where fish are right next to each other, facing the same direction and are both being chased by the shark

        if aliveFishList[0].getDirection() == aliveFishList[1].getDirection():

            if aliveFishList[0].getX() == sharkX:
                if aliveFishList[0].getY() == aliveFishList[1].getY() and abs(aliveFishList[0].getX() - aliveFishList[1].getX()) <= 4:
                    if (aliveFishList[0].getY() == 9 or aliveFishList[0].getY() == 0) and 5 > abs(aliveFishList[0].getY() - sharkY) > 2:
                        fishWin = True
                        gap = False
                                
            elif aliveFishList[0].getY() == sharkY:
                if aliveFishList[0].getX() == aliveFishList[1].getX() and abs(aliveFishList[0].getY() - aliveFishList[1].getY()) <= 4:
                    if (aliveFishList[0].getX() == 9 or aliveFishList[0].getX() == 0) and 5 > abs(aliveFishList[0].getX() - sharkX) > 2:
                        fishWin = True
                        gap = False

        #alternate situation where 1 fish is getting chased, and the other is more than 6 spots away, making it impossible for the shark to switch chasing.

        relation,axis = directionRel(aliveFishList[0],aliveFishList[1])

        if relation == "same" or relation == "opposite":
            if axis == "x":
                if aliveFishList[0].getY() == sharkY:
                    if abs(aliveFishList[0].getY() - aliveFishList[1].getY()) >= 7:
                        if (aliveFishList[0].getX() == 9 or aliveFishList[0].getX() == 0) and 5 > abs(aliveFishList[0].getX() - sharkX) > 2:
                            fishWin = True
                            gap = True

            if axis == "y":
                if aliveFishList[0].getX() == sharkX:
                    if abs(aliveFishList[0].getX() - aliveFishList[1].getX()) >= 7:
                        if (aliveFishList[0].getY() == 9 or aliveFishList[0].getY() == 0) and 5 > abs(aliveFishList[0].getY() - sharkY) > 2:
                            fishWin = True
                            gap = True

    return fishWin,gap

def fishWinTest(fish1,fish2,fish3,sharkX,sharkY,statusList):

    fishWin = False #returns whether stalemate situation has been achieved
    deadNumber,aliveFishList = getAliveList(fish1,fish2,fish3) #returns number of dead fish, list of alive fish

    #if 2 fish are dead, test that the last fish is on the same axis. If on the same axis, test whether the fish is just out of the shark's reach.

    if deadNumber == 2:
        if aliveFishList[0].getX() == sharkX:
            if (aliveFishList[0].getY() == 9 or aliveFishList[0].getY() == 0) and 5 > abs(aliveFishList[0].getY() - sharkY) > 2:
                fishWin = True
                            
        elif aliveFishList[0].getY() == sharkY:
            if (aliveFishList[0].getX() == 9 or aliveFishList[0].getX() == 0) and 5 > abs(aliveFishList[0].getX() - sharkX) > 2:
                fishWin = True

    #if 1 fish is dead, test which fish is on the same axis as the shark, and set that fish to index 0. Test if fish directions are the same, and then test distances to shark
                
    elif deadNumber == 1:

        fishWin,gap = fish2WinTest(aliveFishList,sharkX,sharkY)
        
    #no fish are dead
                                
    elif deadNumber == 0:

        if aliveFishList[0].getX() == sharkX or aliveFishList[1].getX() == sharkX or aliveFishList[2].getX() == sharkX or aliveFishList[0].getY() == sharkY or aliveFishList[1].getY() == sharkY or aliveFishList[2].getY() == sharkY:
            continueVar = False

            #reassign central fish to index zero

            if aliveFishList[0].getX() == sharkX or aliveFishList[0].getY() == sharkY and (aliveFishList[1].getY() != sharkY and aliveFishList[1].getX() != sharkX and aliveFishList[2].getX() != sharkX and aliveFishList[2].getY() != sharkY):
                aliveFishList[0],aliveFishList[1],aliveFishList[2] = aliveFishList[0],aliveFishList[1],aliveFishList[2]
                continueVar = True
            
            elif aliveFishList[1].getX() == sharkX or aliveFishList[1].getY() == sharkY and (aliveFishList[0].getY() != sharkY and aliveFishList[0].getX() != sharkX and aliveFishList[2].getX() != sharkX and aliveFishList[2].getY() != sharkY):
                aliveFishList[0],aliveFishList[1],aliveFishList[2] = aliveFishList[1],aliveFishList[0],aliveFishList[2]
                continueVar = True

            elif aliveFishList[2].getX() == sharkX or aliveFishList[2].getY() == sharkY and (aliveFishList[0].getY() != sharkY and aliveFishList[0].getX() != sharkX and aliveFishList[1].getX() != sharkX and aliveFishList[1].getY() != sharkY):
                aliveFishList[0],aliveFishList[1],aliveFishList[2] = aliveFishList[2],aliveFishList[1],aliveFishList[2]
                continueVar = True

            if continueVar == True:

                fishWin1,gap1 = fish2WinTest([aliveFishList[0],aliveFishList[1]],sharkX,sharkY)
                fishWin2,gap2 = fish2WinTest([aliveFishList[0],aliveFishList[2]],sharkX,sharkY)

                if fishWin1 == True:
                    statusList.append(fishWin1)
                    statusList.append(gap1)

                if fishWin2 == True:
                    statusList.append(fishWin2)
                    statusList.append(gap2)

                if len(statusList) >=4:

                    if statusList[0] == True and statusList[2] == True:

                        #test if all three are on the same axis, on the same direction
                        
                        if statusList[1] == False and statusList[3] == False:
                            fishWin = True

                        #test if 2 fish are adjacent and there is a gap to ther third
                        elif statusList[1] == False and statusList[3] == True:
                            fishWin = True
                        elif statusList[1] == True and statusList[3] == False:
                            fishWin = True

                        #test if 1 fish is adjacent and there is a gap to both

                        elif statusList[1] == True and statusList[3] == True:
                            fishWin = True
 
    return fishWin

