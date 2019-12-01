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

    #set up GUI, gather user input to feed into fish object constructor

    GUI = SharkGUI()
    GUIList = GUI.gatherUserInput()
    fish1 = Fish(GUIList[0],GUIList[1],"west",False,True,False,"DNE")
    fish2 = Fish(GUIList[5],GUIList[6],"west",False,True,False,"DNE")
    fish3 = Fish(GUIList[10],GUIList[11],"west",False,True,False,"DNE")

    fishListObjects = [fish1,fish2,fish3] #use this to efficiently cycle through fish
    
    shark = Shark()
    sharkX,sharkY = shark.getPosition()

    for fishObject in fishListObjects:
        fishObject.setFlee(sharkX,sharkY)
    
    fishList = getFishList(fish1,fish2,fish3)
    GUI.updateFish(fishList)
    GUI.updateFish(fishList)

    while True:

        buttonClicked = GUI.isClicked()

        fishList = getFishList(fish1,fish2,fish3)
        
        if buttonClicked == "fish":

            sharkList = shark.getSharkList()
            sharkX,sharkY = shark.getPosition()

            for fishObject in fishListObjects:
                fishObject.setFlee(sharkX,sharkY)
                
            for fishObject in fishListObjects:
                fishObject.setDirection(sharkX,sharkY)
                
            for fishObject in fishListObjects:
                fishObject.move(1)

            for fishObject in fishListObjects:

                if fishObject.getWallHitting() ==  True and fishObject.getFlee() == False:
                    fishObject.directionReverse()
                    fishObject.move(1)
                elif fishObject.getWallHitting() ==  True and fishObject.getFlee() == True:
                    fishObject.reversePos()
                    fishObject.setFlee(sharkX,sharkY)

            #collisions scenario
                    
            if fish1.getX() == fish2.getX() and fish1.getY() == fish2.getY():
                if fish1.getFlee() == True and fish1.getAltDirection() == True:
                    collideMove(fish1)
                elif fish2.getFlee() == True and fish2.getAltDirection() == True:
                    collideMove(fish2)
                else: #CHECK THIS AGAINST SPECS
                    fish1.move(1)

            if fish1.getX() == fish3.getX() and fish1.getY() == fish3.getY():
                if fish1.getFlee() == True and fish1.getAltDirection() == True:
                    collideMove(fish1)
                elif fish3.getFlee() == True and fish3.getAltDirection() == True:
                    collideMove(fish2)
                else: #CHECK THIS AGAINST SPECS
                    fish1.move(1)

            if fish3.getX() == fish2.getX() and fish3.getY() == fish2.getY():

                if fish3.getFlee() == True and fish3.getAltDirection() == True:
                    collideMove(fish3)
                elif fish2.getFlee() == True and fish2.getAltDirection() == True:
                    collideMove(fish2)
                else: #CHECK THIS AGAINST SPECS
                    fish2.move(1)
            
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
