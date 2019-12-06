#File: SharkRunnerWorking.py

from SharkGUI import *
from Fish import *
from Shark import *

#to do
#win conditions for 3 fish (APZ)
#fish collide, head on collision

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
            fishObject.wallSetDirection()
            fishObject.move(2)

        #if the fish hits the wall and is in flee mode, the fish will flip across the grid
            
        elif fishObject.getWallHitting() ==  True and fishObject.getFlee() == True:
            fishObject.reversePos()

def collisionScenario(fishListObjects):

    #collisions scenario, use list to cycle between fish combinations. For loop cycles between combination 1,3 - 1,2 - 2,3 in that order
    #tests if the coordinates of each fish match. If the fish have alternate directions (are fleeing from a corner), the fish moves back
    #switches to the alternate direction, and then moves in that direction. Otherwise, the fish stays in its original position.

    for fishObjectInt in range(0,3):

        if fishListObjects[fishObjectInt - 1].getAlive() == True and fishListObjects[fishObjectInt].getAlive() == True:
            
            if fishListObjects[fishObjectInt - 1].getX() == fishListObjects[fishObjectInt].getX() and fishListObjects[fishObjectInt - 1].getY() == fishListObjects[fishObjectInt].getY():
                if fishListObjects[fishObjectInt].getFlee() == True and fishListObjects[fishObjectInt].getAltDirection() == True:
                    collideMove(fishListObjects[fishObjectInt])
                elif fishListObjects[fishObjectInt - 1].getFlee() == True and fishListObjects[fishObjectInt - 1].getAltDirection() == True:
                    collideMove(fishListObjects[fishObjectInt - 1])
                else:
                    if fishListObjects[fishObjectInt - 1].getDirection() == fishListObjects[fishObjectInt].getDirection():
                        fishListObjects[fishObjectInt].move(-1)
                        fishListObjects[fishObjectInt - 1].move(-1)
                    else:
                        fishListObjects[fishObjectInt].move(-1)

def fishWinTest(fish1,fish2,fish3,sharkX,sharkY):

    #test each fish for alive status, add them to a list of alive fish

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

    #if 2 fish are dead, test that the last fish is on the same axis. If on the same axis, test distance from shark. Shark cannot be too close to edge.

    if deadNumber == 2:
        if aliveFishList[0].getX() == sharkX:
            if sharkX <= 7 or sharkX >= 2:
                if abs(aliveFishList[0].getY() - sharkY) > 4 and abs(aliveFishList[0].getY() - sharkY) != 6:
                    fishWin = True
                            
        elif aliveFishList[0].getY() == sharkY:
            if sharkY <= 7 or sharkY >= 2:
                if abs(aliveFishList[0].getX() - sharkX) > 4 and abs(aliveFishList[0].getY() - sharkY) != 6:
                    fishWin = True

    #if 1 fish is dead, test which fish is on the same axis as the shark, and put that in index 0. Test if directions are the same, and then test distance to shark
                
    elif deadNumber == 1:
        if aliveFishList[0].getX() == sharkX or aliveFishList[1].getX() == sharkX or aliveFishList[0].getY() == sharkY or aliveFishList[1].getY() == sharkY:

            if aliveFishList[0].getX() == sharkX or aliveFishList[0].getY() == sharkY and (aliveFishList[1].getY() != sharkY and aliveFishList[1].getX() != sharkX):
                aliveFishList[0],aliveFishList[1] = aliveFishList[0],aliveFishList[1]
                
            elif aliveFishList[1].getX() == sharkX or aliveFishList[1].getY() == sharkY and (aliveFishList[0].getY() != sharkY and aliveFishList[0].getX() != sharkX):
                aliveFishList[1],aliveFishList[0] = aliveFishList[0],aliveFishList[1]

            if aliveFishList[0].getDirection() == aliveFishList[1].getDirection():

                if aliveFishList[0].getX() == sharkX:
                    if aliveFishList[0].getY() == aliveFishList[1].getY():
                        if sharkX <= 7 or sharkX >= 2:
                            if abs(aliveFishList[0].getY() - sharkY) > 5:
                                fishWin = True
                                    
                elif aliveFishList[0].getY() == sharkY:
                    if aliveFishList[0].getX() == aliveFishList[1].getX():
                        if sharkY <= 7 or sharkY >= 2:
                            if abs(aliveFishList[0].getX() - sharkX) > 5:
                                fishWin = True
                                
        elif deadNumber == 0:
            if aliveFishList[0].getX() == sharkX or aliveFishList[1].getX() == sharkX or aliveFishList[2].getX() == SharkX or aliveFishList[0].getY() == sharkY or aliveFishList[1].getY() == sharkY or aliveFishList[2].getY() == sharkY:

                if aliveFishList[0].getX() == sharkX or aliveFishList[0].getY() == sharkY and (aliveFishList[1].getY() != sharkY and aliveFishList[1].getX() != sharkX and aliveFishList[2].getX() != SharkX and aliveFishList[2].getY() == SharkY):
                    aliveFishList[0],aliveFishList[1],aliveFishList[2] = aliveFishList[0],aliveFishList[1],aliveFishList[2]
                
                elif aliveFishList[1].getX() == sharkX or aliveFishList[1].getY() == sharkY and (aliveFishList[0].getY() != sharkY and aliveFishList[0].getX() != sharkX and aliveFishList[2].getX() != SharkX and aliveFishList[2].getY() == SharkY):
                    aliveFishList[1],aliveFishList[0],aliveFishList[2] = aliveFishList[0],aliveFishList[1],aliveFishList[2]

                elif aliveFishList[2].getX() == sharkX or aliveFishList[2].getY() == sharkY and (aliveFishList[0].getY() != sharkY and aliveFishList[0].getX() != sharkX and aliveFishList[1].getX() != SharkX and aliveFishList[1].getY() == SharkY):
                    aliveFishList[2],aliveFishList[0],aliveFishList[1] = aliveFishList[0],aliveFishList[1],aliveFishList[2]

                if aliveFishList[0].getDirection() == aliveFishList[1].getDirection() == aliveFishList[2].getDirection():
                    if aliveFishList[0].getX() == sharkX:
                        if aliveFishList[0].getY() == aliveFishList[1].getY() == aliveFishList[2].getY():
                            if sharkX <= 7 or sharkX >= 2:
                                if abs(aliveFishList[0].getY() - sharkY) > 5:
                                    fishWin = True
                                        
                    elif aliveFishList[0].getY() == sharkY:
                        if aliveFishList[0].getX() == aliveFishList[1].getX() == aliveFishList[2].getX():
                            if sharkY <= 7 or sharkY >= 2:
                                if abs(aliveFishList[0].getX() - sharkX) > 5:
                                    fishWin = True
                                    
    return fishWin

def main():

    #set up GUI, gather user input to feed into subsequent fish object constructor
        
    GUI = SharkGUI()
    GUIList = GUI.gatherUserInput()

    looping = True

    while looping == True:

        fishWins = 0 # use this variable to delay fish win message

        if GUIList == []: #use this if statement to ensure that quit does not lead to error if start is not clicked
            looping = False
            break

        elif GUIList != []:
        
            fish1 = Fish(GUIList[0],GUIList[1],"west",False,True,False,"DNE")
            fish2 = Fish(GUIList[5],GUIList[6],"west",False,True,False,"DNE")
            fish3 = Fish(GUIList[10],GUIList[11],"west",False,True,False,"DNE")

            fish1.setInputDirection("west")
            fish2.setInputDirection("west")
            fish3.setInputDirection("west")

            fishListObjects = [fish1,fish2,fish3] #use this list to efficiently cycle through fish objects in repetitive sequences, order is 1, 2, 3

            print(fish1.getCoords(),fish2.getCoords(),fish3.getCoords())

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

                    #fish Win situation, fishWin delays display of fish victory

                    if fishWinTest(fish1,fish2,fish3,sharkX,sharkY) == True:
                        fishWins += 1
                        if fishWins == 3:
                            GUIList = GUI.winner("fish")
                            break
                            if GUIList == []:
                                looping = False


                elif buttonClicked == "shark":

                    fishList = getFishList(fish1,fish2,fish3)

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
                        if GUIList == []:
                            looping = False

                elif buttonClicked == "quit":

                    GUI.endGame()
                    looping = False
                    break
        
main()
