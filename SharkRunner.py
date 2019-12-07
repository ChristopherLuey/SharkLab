#File: SharkRunnerWorking.py

from SharkGUI import *
from Fish import *
from Shark import *

#to do
#win conditions for 3 fish (APZ)
#fish collide, head on collision

def directionRel(fish1,fish2):

    fish1direction = fish1.getDirection()
    fish2direction = fish2.getDirection()

    if fish1direction == fish2direction:
        return "same",""

    else:
        if fish1direction == "west":
            if fish2direction == "east":
                return "opposite","x"
            
        elif fish1direction == "east":
            if fish2direction == "west":
                return "opposite","x"

        elif fish1direction == "north":
            if fish2direction == "south":
                return "opposite","y"

        elif fish1direction == "south":
            if fish2direction == "north":
                return "opposite","y"

    return "",""
            

def getDistance(fish1,fish2):

    #returns the distance between two fish

    distance = abs(fish1.getX() - fish2.getX()) + abs(fish1.getY() - fish2.getY())

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
                        if directionRel(fishListObjects[fishObjectInt],fishListObjects[fishObjectInt - 1]) == "opposite":
                            fishListObjects[fishObjectInt].move(-1)
                            fishListObjects[fishObjectInt].setHeadOnStatus(True)
                            fishListObjects[fishObjectInt - 1].setHeadOnStatus(True)

                        else:
                            fishListObjects[fishObjectInt].move(-1)

            opposite,axis =  directionRel(fishListObjects[fishObjectInt],fishListObjects[fishObjectInt - 1])   

            if opposite == "opposite":
                if (axis == "x" and abs(fishListObjects[fishObjectInt - 1].getX() - fishListObjects[fishObjectInt].getX()) == 1) and fishListObjects[fishObjectInt].getY() == fishListObjects[fishObjectInt - 1].getY():

                    fishListObjects[fishObjectInt].move(-1)
                    fishListObjects[fishObjectInt - 1].move(-1)

                    #if after movement, they are not longer in a headon collision, move again
                    
                    if not(abs(fishListObjects[fishObjectInt - 1].getX() - fishListObjects[fishObjectInt].getX()) == 1):
                        fishListObjects[fishObjectInt].move(1)
                        fishListObjects[fishObjectInt - 1].move(1)

                elif (axis == "y" and abs(fishListObjects[fishObjectInt - 1].getY() - fishListObjects[fishObjectInt].getY()) == 1) and fishListObjects[fishObjectInt].getX() == fishListObjects[fishObjectInt - 1].getX():

                    ishListObjects[fishObjectInt].move(-1)
                    fishListObjects[fishObjectInt - 1].move(-1)

                    #if after movement, they are not longer in a headon collision, move again
                    
                    if not(abs(fishListObjects[fishObjectInt - 1].getY() - fishListObjects[fishObjectInt].getY()) == 1):
                        fishListObjects[fishObjectInt].move(1)
                        fishListObjects[fishObjectInt - 1].move(1)

def fishWinTest(fish1,fish2,fish3,sharkX,sharkY):

    #test each fish for alive status, and if so, add them to a list of alive fish

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

    #if 2 fish are dead, test that the last fish is on the same axis. If on the same axis, test whether the fish is just out of the shark's reach.

    if deadNumber == 2:
        if aliveFishList[0].getX() == sharkX:
            if (aliveFishList[0].getY() == 9 or aliveFishList[0].getY() == 0) and 5 > abs(aliveFishList[0].getY() - sharkY) > 2:
                fishWin = True
                            
        elif aliveFishList[0].getY() == sharkY:
            if (aliveFishList[0].getX() == 9 or aliveFishList[0].getX() == 0) and 5 > abs(aliveFishList[0].getX() - sharkX) > 2:
                fishWin = True

    #if 1 fish is dead, test which fish is on the same axis as the shark, and set that fish to centerFish. Test if fish directions are the same, and then test distances to shark
                
    elif deadNumber == 1:
        if aliveFishList[0].getX() == sharkX or aliveFishList[1].getX() == sharkX or aliveFishList[0].getY() == sharkY or aliveFishList[1].getY() == sharkY:

            if aliveFishList[0].getX() == sharkX or aliveFishList[0].getY() == sharkY and (aliveFishList[1].getY() != sharkY and aliveFishList[1].getX() != sharkX):
                aliveFishList[0],aliveFishList[1] = aliveFishList[0],aliveFishList[1]
                
            elif aliveFishList[1].getX() == sharkX or aliveFishList[1].getY() == sharkY and (aliveFishList[0].getY() != sharkY and aliveFishList[0].getX() != sharkX):
                aliveFishList[1],aliveFishList[0] = aliveFishList[0],aliveFishList[1]

            if aliveFishList[0].getDirection() == aliveFishList[1].getDirection():

                if aliveFishList[0].getX() == sharkX:
                    if aliveFishList[0].getY() == aliveFishList[1].getY() or abs(aliveFishList[0].getX() - aliveFishList[1].getX()) >= 7:
                        if (aliveFishList[0].getY() == 9 or aliveFishList[0].getY() == 0) and 5 > abs(aliveFishList[0].getY() - sharkY) > 2:
                            fishWin = True
                                    
                elif aliveFishList[0].getY() == sharkY:
                    if aliveFishList[0].getX() == aliveFishList[1].getX() or abs(aliveFishList[0].getY() - aliveFishList[1].getY()) >= 7:
                        if (aliveFishList[0].getX() == 9 or aliveFishList[0].getX() == 0) and 5 > abs(aliveFishList[0].getX() - sharkX) > 2:
                            fishWin = True

    #no fish are dead
                                
    elif deadNumber == 0:

        if aliveFishList[0].getX() == sharkX or aliveFishList[1].getX() == sharkX or aliveFishList[2].getX() == sharkX or aliveFishList[0].getY() == sharkY or aliveFishList[1].getY() == sharkY or aliveFishList[2].getY() == sharkY:

            if aliveFishList[0].getX() == sharkX or aliveFishList[0].getY() == sharkY and (aliveFishList[1].getY() != sharkY and aliveFishList[1].getX() != sharkX and aliveFishList[2].getX() != sharkX and aliveFishList[2].getY() != sharkY):
                centerFish = aliveFishList[0]
            
            elif aliveFishList[1].getX() == sharkX or aliveFishList[1].getY() == sharkY and (aliveFishList[0].getY() != sharkY and aliveFishList[0].getX() != sharkX and aliveFishList[2].getX() != sharkX and aliveFishList[2].getY() != sharkY):
                centerFish = aliveFishList[1]

            elif aliveFishList[2].getX() == sharkX or aliveFishList[2].getY() == sharkY and (aliveFishList[0].getY() != sharkY and aliveFishList[0].getX() != sharkX and aliveFishList[1].getX() != sharkX and aliveFishList[1].getY() != sharkY):
                centerFish = aliveFishList[2]

            if aliveFishList[0].getDirection() == aliveFishList[1].getDirection() == aliveFishList[2].getDirection():
                if centerFish.getX() == sharkX:
                    if centerFish.getY() == aliveFishList[1].getY() == aliveFishList[2].getY() == aliveFishList[0].getY():
                        if (centerFish.getY() == 9 or centerFish.getY() == 0) and 5 > abs(centerFish.getY() - sharkY) > 0:
                            fishWin = True
                                    
                elif centerFish.getY() == sharkY:
                    if centerFish.getX() == aliveFishList[1].getX() == aliveFishList[2].getX() == aliveFishList[0].getX():
                        if (centerFish.getX() == 9 or centerFish.getX() == 0) and 5 > abs(centerFish.getX() - sharkX) > 0:
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

            fish2.setInputDirection("west")
            fish3.setInputDirection("east")
            
            fishListObjects = [fish1,fish2,fish3] #use this list to efficiently cycle through fish objects in repetitive sequences, order is 1, 2, 3

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
                    GUI.nextTurn()
                    GUI.updateFish(fishList)

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
