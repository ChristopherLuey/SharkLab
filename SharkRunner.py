#File: SharkRunnerWorking.py

from SharkGUI import *
from Fish import *
from Shark import *

#to do
#win conditions for 2 fish (APZ)
#south facing fish

def getFishList(fish1,fish2,fish3):
    #returns a list of fish data to be inputed into the GUI, which updates the graphic representations of fish
    return [fish1.getX(),fish1.getY(),fish1.getDirection(),fish1.getFlee(),fish1.getAlive(),fish2.getX(),fish2.getY(),fish2.getDirection(),fish2.getFlee(),fish2.getAlive(),fish3.getX(),fish3.getY(),fish3.getDirection(),fish3.getFlee(),fish3.getAlive()]

def collideMove(fish):

    #sequence of movements if fish has two movement options (on a diagonal with the shark) in case fish collides
    
    fish.directionReverse()
    fish.move(1)
    fish.collideSetDirection()
    fish.move(1)

def wallHitting(fishListObjects,sharkX,sharkY):

    #wall hitting scenario. If in flee, fish flips across grid. Otherwise, initiates wall bump sequence.

    for fishObject in fishListObjects:

        #if the fish hits the wall and is not in flee mode, the fish will reverse direction and move one square in the GUI

        if fishObject.getWallHitting() ==  True and fishObject.getFlee() == False:
            fishObject.directionReverse()
            fishObject.move(2)

        #if the fish hits the wall and is in flee mode, the fish will flip across the grid
            
        elif fishObject.getWallHitting() ==  True and fishObject.getFlee() == True:
            fishObject.reversePos()
            fishObject.setFlee(sharkX,sharkY)

def collisionScenario(fishListObjects):

    #collisions scenario, use list to cycle between fish combinations. For loop cycles between combination 1,3 - 1,2 - 2,3 in that order
    #tests if the coordinates of each fish match. If the fish have alternate directions (are fleeing from a corner), the fish moves back
    #switches to the alternate direction, and then moves in that direction. Otherwise, the fish stays in its original position.

    for fishObjectInt in range(0,3):
            
        if fishListObjects[fishObjectInt - 1].getX() == fishListObjects[fishObjectInt].getX() and fishListObjects[fishObjectInt - 1].getY() == fishListObjects[fishObjectInt].getY():
            if fishListObjects[fishObjectInt].getFlee() == True and fishListObjects[fishObjectInt].getAltDirection() == True:
                collideMove(fishListObjects[fishObjectInt])
            elif fishListObjects[fishObjectInt - 1].getFlee() == True and fishListObjects[fishObjectInt - 1].getAltDirection() == True:
                collideMove(fishListObjects[fishObjectInt - 1])
            else:
                fishListObjects[fishObjectInt].move(-1)

def fishWinTest(fish1,fish2,fish3,sharkX,sharkY):

    fishWin = False

    deadNumber = 0

    aliveFishList = []

    if fish1.getAlive() == False:
        deadNumber += 1
    else:
        aliveFishList.append(fish1)
        
    if fish2.getAlive() == False:
        deadNumber += 1
    else:
        aliveFishList.append(fish2)
        
    if fish3.getAlive() == False:
        deadNumber += 1
    else:
        aliveFishList.append(fish3)

    if deadNumber == 2:
        if aliveFishList[0].getX() == sharkX:
            if abs(aliveFishList[0].getY() - sharkY) > 4:
                fishWin = True
        elif aliveFishList[0].getY() == sharkY:
            if abs(aliveFishList[0].getX() - sharkX) > 4:
                fishWin = True
                
    elif deadNumber == 1:
        if aliveFishList[0].getX() == sharkX or aliveFishList[1].getX() == sharkX or aliveFishList[0].getY() == sharkY or aliveFishList[1].getY() == sharkY:
            if aliveFishList[0].getX() == sharkX or aliveFishList[0].getY() == sharkY and (aliveFishList[1].getY() != sharkY and aliveFishList[1].getX() != sharkX):
                aliveFishList[0],aliveFishList[1] = aliveFishList[0],aliveFishList[1]
                
            elif aliveFishList[1].getX() == sharkX or aliveFishList[1].getY() == sharkY and (aliveFishList[0].getY() != sharkY and aliveFishList[0].getX() != sharkX):
                aliveFishList[1],aliveFishList[0] = aliveFishList[0],aliveFishList[1]

            if aliveFishList[0].getX() == sharkX:
                if aliveFishList[0].getY() == aliveFishList[1].getY():
                    if abs(aliveFishList[0].getY() - sharkY) > 4:
                        fishWin = True
                                
            elif aliveFishList[0].getY() == sharkY:
                if aliveFishList[0].getX() == aliveFishList[1].getX():
                    if abs(aliveFishList[0].getX() - sharkX) > 4:
                        fishWin = True

    return fishWin

def main():

    #set up GUI, gather user input to feed into subsequent fish object constructor
        
    GUI = SharkGUI()
    GUIList = GUI.gatherUserInput()

    looping = True

    while looping == True:

        if GUIList == []: #use this if statement to ensure that quit does not lead to error if start is not clicked
            looping = False
            break

        elif GUIList != []:
        
            fish1 = Fish(GUIList[0],GUIList[1],"west",False,True,False,"DNE")
            fish2 = Fish(GUIList[5],GUIList[6],"west",False,True,False,"DNE")
            fish3 = Fish(GUIList[10],GUIList[11],"west",False,True,False,"DNE")

            fishListObjects = [fish1,fish2,fish3] #use this list to efficiently cycle through fish objects in repetitive sequences

            #construct shark, gather coordinates to set flee status of each fish
            
            shark = Shark()
            sharkX,sharkY = shark.getPosition()

            for fishObject in fishListObjects:
                fishObject.setFlee(sharkX,sharkY)

            #update GUI to reflect these changes
            
            fishList = getFishList(fish1,fish2,fish3)
            GUI.updateFish(fishList)

            while True:

                buttonClicked = GUI.isClicked()
                #fishList = getFishList(fish1,fish2,fish3)
                
                if buttonClicked == "fish":

                    sharkList = shark.getSharkList()
                    sharkX,sharkY = shark.getPosition()

                    for fishObject in fishListObjects:
                        fishObject.setFlee(sharkX,sharkY)
                        
                    for fishObject in fishListObjects:
                        fishObject.setDirection(sharkX,sharkY)
                        
                    for fishObject in fishListObjects:
                        fishObject.move(1)

                    #wall hitting scenario. If in flee, fish flips across grid. Otherwise, initiates wall bump sequence.

                    wallHitting(fishListObjects,sharkX,sharkY)

                    #collisions scenario
                    
                    collisionScenario(fishListObjects)

                    fishList = getFishList(fish1,fish2,fish3)
                    GUI.updateFish(fishList)
                    GUI.nextTurn()

                    if fishWinTest(fish1,fish2,fish3,sharkX,sharkY) == True:
                        GUIList = GUI.winner("fish")
                        break
                        if GUIList == []:
                            looping = False


                elif buttonClicked == "shark":

                    fishList = getFishList(fish1,fish2,fish3)

                    shark.sharkTurn(fishList)
                    sharkList = shark.getSharkList()
                    sharkX,sharkY = shark.getPosition()

                    for fishObject in fishListObjects:
                        if sharkX == fishObject.getX() and sharkY == fishObject.getY() and fishObject.getAlive() == True:
                            fishObject.eat()

                    GUI.updateShark(sharkList)
                    GUI.updateFish(fishList)
                    GUI.nextTurn()

                    if fish1.getAlive() == False and fish2.getAlive() == False and fish3.getAlive() == False:

                        GUIList = GUI.winner("shark")
                        break
                        if GUIList == []:
                            looping = False

                elif buttonClicked == "quit":

                    GUI.endGame()
                    looping = False
                    break
        
main()
