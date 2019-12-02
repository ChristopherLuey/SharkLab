#File: SharkRunnerWorking.py

from SharkGUI import *
from Fish import *
from Shark import *
import math

def getFishList(fish1,fish2,fish3):
    return [fish1.getX(),fish1.getY(),fish1.getDirection(),fish1.getFlee(),fish1.getAlive(),fish2.getX(),fish2.getY(),fish2.getDirection(),fish2.getFlee(),fish2.getAlive(),fish3.getX(),fish3.getY(),fish3.getDirection(),fish3.getFlee(),fish3.getAlive()]

def collideMove(fish):
    fish.directionReverse()
    fish.move(1)
    fish.collideSetDirection()
    fish.move(1)

def main():

    #set up GUI, gather user input to feed into subsequent fish object constructor

    GUI = SharkGUI()
    GUIList = GUI.gatherUserInput()
    
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

            for fishObject in fishListObjects:

                if fishObject.getWallHitting() ==  True and fishObject.getFlee() == False:
                    fishObject.directionReverse() #this should be done next round
                    fishObject.move(1)
                elif fishObject.getWallHitting() ==  True and fishObject.getFlee() == True:
                    fishObject.reversePos()
                    fishObject.setFlee(sharkX,sharkY)

            #collisions scenario, use list to cycle between fish combinations. For loop cycles between combination 1,3 - 1,2 - 2,3 in that order
            #tests if the coordinates of each fish match. If the fish have alternate directions (are fleeing from a corner), the fish moves back
            #switches to the alternate direction, and then moves in that direction. Otherwise, the fish stays in its original position.

            for fishObjectInt in range(0,3):
                    
                if fishListObjects[fishObjectInt - 1].getX() == fishListObjects[fishObjectInt].getX() and fishListObjects[fishObjectInt - 1].getY() == fishListObjects[fishObjectInt].getY():
                    if fishListObjects[fishObjectInt].getFlee() == True and fishListObjects[fishObjectInt].getAltDirection() == True:
                        collideMove(fishListObjects[fishObjectInt])
                    elif fishListObjects[fishObjectInt - 1].getFlee() == True and fishListObjects[fishObjectInt - 1].getAltDirection() == True:
                        collideMove(fishListObjects[fishObjectInt - 1])
                    else: #CHECK THIS AGAINST SPECS
                        fishListObjects[fishObjectInt].move(-1)
            
            fishList = getFishList(fish1,fish2,fish3)
            GUI.updateFish(fishList)
            GUI.nextTurn()

        elif buttonClicked == "shark":

            fishList = getFishList(fish1,fish2,fish3)

            placeHolderList = shark.sharkTurn(fishList)
            sharkList = shark.getSharkList()
            sharkX,sharkY = shark.getPosition()

            for fishObject in fishListObjects:
                if sharkX == fishObject.getX() and sharkY == fishObject.getY() and fishObject.getAlive() == True:
                    fishObject.eat()

            GUI.updateShark(sharkList)
            GUI.updateFish(fishList)
            GUI.nextTurn()

            if fish1.getAlive() == False and fish2.getAlive() == False and fish3.getAlive() == False:

                pass #display game over message at this pt.

        elif buttonClicked == "quit":

            GUI.endGame()
            break
        
main()
