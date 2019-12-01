#File: SharkRunner.py

from SharkGUI import *
from Fish import *
from Shark import *
import math

def setFlee(sharkX,sharkY,fish1,fish2,fish3):

    fish1.setFlee(sharkX,sharkY)
    fish2.setFlee(sharkX,sharkY)
    fish3.setFlee(sharkX,sharkY)

def setDirection(sharkX,sharkY,fish1,fish2,fish3):

    fish1.setDirection(sharkX,sharkY)
    fish2.setDirection(sharkX,sharkY)
    fish3.setDirection(sharkX,sharkY)

def move(distance,fish1,fish2,fish3):

    fish1.move(distance)
    fish2.move(distance)
    fish3.move(distance)

def getFishList(fish1,fish2,fish3):

    return [fish1.getX(),fish1.getY(),fish1.getDirection(),fish1.getFlee(),fish1.getAlive(),fish2.getX(),fish2.getY(),fish2.getDirection(),fish2.getFlee(),fish2.getAlive(),fish3.getX(),fish3.getY(),fish3.getDirection(),fish3.getFlee(),fish3.getAlive()]

def wallHitting(distance,fish1,fish2,fish3,sharkX,sharkY):

    #wall situation

    if fish1.getWallHitting() ==  True and fish1.getFlee() == False:
        fish1.directionReverse()
        fish1.move(1)
    elif fish1.getWallHitting() ==  True and fish1.getFlee() == True:
        fish1.reversePos()
        fish1.setFlee(sharkX,sharkY)

    if fish2.getWallHitting() ==  True and fish2.getFlee() == False:
        fish2.directionReverse()
        fish2.move(1)
    elif fish2.getWallHitting() ==  True and fish2.getFlee() == True:
        fish2.reversePos()
        fish2.setFlee(sharkX,sharkY)

    if fish3.getWallHitting() ==  True and fish3.getFlee() == False:
        fish3.directionReverse()
        fish3.move(1)
    elif fish3.getWallHitting() ==  True and fish3.getFlee() == True:
        fish3.reversePos()
        fish3.setFlee(sharkX,sharkY)

def collideMove(fish):
    fish.directionReverse()
    fish.move(1)
    fish.collideSetDirection()
    fish.move(1)
    

def collisions(fish1,fish2,fish3):

    if fish1.getX() == fish2.getX() and fish1.getY() == fish2.getY():
        if fish1.getFlee() == True and fish1.getAltDirection() == True:
            collideMove(fish1)
        elif fish2.getFlee() == True and fish2.getAltDirection() == True:
            collideMove(fish2)
        if fish1.getAltDirection() == False and fish2.getAltDirection() == False: #CHECK THIS AGAINST SPECS
            fish1.move(1)

    if fish1.getX() == fish3.getX() and fish1.getY() == fish3.getY():
        if fish1.getFlee() == True and fish1.getAltDirection() == True:
            collideMove(fish1)
        elif fish3.getFlee() == True and fish3.getAltDirection() == True:
            collideMove(fish2)
        if fish1.getAltDirection() == False and fish2.getAltDirection() == False: #CHECK THIS AGAINST SPECS
            fish1.move(1)

    if fish3.getX() == fish2.getX() and fish3.getY() == fish2.getY():

        if fish3.getFlee() == True and fish3.getAltDirection() == True:
            collideMove(fish3)
        elif fish2.getFlee() == True and fish2.getAltDirection() == True:
            collideMove(fish2)
        if fish3.getAltDirection() == False and fish2.getAltDirection() == False: #CHECK THIS AGAINST SPECS
            fish2.move(1)

    


def main():

    GUI = SharkGUI()

    GUIList = GUI.gatherUserInput()

    fish1 = Fish(GUIList[0],GUIList[1],"west",False,True,False,"DNE")
    fish2 = Fish(GUIList[5],GUIList[6],"west",False,True,False,"DNE")
    fish3 = Fish(GUIList[10],GUIList[11],"west",False,True,False,"DNE")
    
    shark = Shark()

    sharkX,sharkY = shark.getPosition()

    setFlee(sharkX,sharkY,fish1,fish2,fish3)

    fishList = getFishList(fish1,fish2,fish3)
    
    GUI.updateFish(fishList)
    GUI.updateFish(fishList)

    while True:

        buttonClicked = GUI.isClicked()

        fishList = getFishList(fish1,fish2,fish3)
        
        if buttonClicked == "fish":

            sharkList = shark.getSharkList()
            sharkX,sharkY = shark.getPosition()

            setFlee(sharkX,sharkY,fish1,fish2,fish3)
            setDirection(sharkX,sharkY,fish1,fish2,fish3)
            move(1,fish1,fish2,fish3)

            wallHitting(1,fish1,fish2,fish3,sharkX,sharkY)
            collisions(fish1,fish2,fish3)
            
            fishList = getFishList(fish1,fish2,fish3)
            
            GUI.updateFish(fishList)
            GUI.nextTurn()

        elif buttonClicked == "shark":

            fishList = getFishList(fish1,fish2,fish3)

            placeHolderList = shark.sharkTurn(fishList)
            sharkList = shark.getSharkList()
            sharkX,sharkY = shark.getPosition()

            if sharkX == fish1.getX() and sharkY == fish1.getY() and fish1.getAlive() == True:
                fish1.eat()
            elif sharkX == fish2.getX() and sharkY == fish2.getY() and fish2.getAlive() == True:
                fish2.eat()
            elif sharkX == fish3.getX() and sharkY == fish3.getY() and fish3.getAlive() == True:
                fish3.eat()

            GUI.updateShark(sharkList)
            GUI.updateFish(fishList)
            GUI.nextTurn()

            if fish1.getAlive() == False and fish2.getAlive() == False and fish3.getAlive() == False:

                pass #display game over message at this pt.

        elif buttonClicked == "quit":

            GUI.endGame()
            break

main()
