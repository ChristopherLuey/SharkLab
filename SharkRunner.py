#File: SharkRunner.py

from SharkGUI import *
from Fish import *
from Shark import *
import math

def main():

    GUI = SharkGUI()

    GUIList = GUI.gatherUserInput()

    fish1 = Fish(GUIList[0],GUIList[1],"west",False,True,False) #his name is Bill
    fish2 = Fish(GUIList[5],GUIList[6],"west",False,True,False) #his name is Bill Sr.
    fish3 = Fish(GUIList[10],GUIList[11],"west",False,True,False) #her name is Billie

    shark = Shark()

    sharkX,sharkY = shark.getPosition()

    fish1.setFlee(sharkX,sharkY)
    fish2.setFlee(sharkX,sharkY)
    fish3.setFlee(sharkX,sharkY)

    fishList = [fish1.getX(),fish1.getY(),fish1.getDirection(),fish1.getFlee(),fish1.getAlive(),fish2.getX(),fish2.getY(),fish2.getDirection(),fish2.getFlee(),fish2.getAlive(),fish3.getX(),fish3.getY(),fish3.getDirection(),fish3.getFlee(),fish3.getAlive()]
    
    GUI.updateFish(fishList)
    GUI.updateFish(fishList)

    while True:

        buttonClicked = GUI.isClicked()

        fishList = [fish1.getX(),fish1.getY(),fish1.getDirection(),fish1.getFlee(),fish1.getAlive(),fish2.getX(),fish2.getY(),fish2.getDirection(),fish2.getFlee(),fish2.getAlive(),fish3.getX(),fish3.getY(),fish3.getDirection(),fish3.getFlee(),fish3.getAlive()]
        
        if buttonClicked == "fish":

            sharkList = shark.getSharkList()

            sharkX,sharkY = shark.getPosition()

            fish1.setFlee(sharkX,sharkY)
            fish2.setFlee(sharkX,sharkY)
            fish3.setFlee(sharkX,sharkY)
    
            fish1.move(sharkX,sharkY,1)
            fish2.move(sharkX,sharkY,1)
            fish3.move(sharkX,sharkY,1)

            #wall situation

            if fish1.getWallHitting == True and fish1.getFlee() == False:
                fish1.directionReverse()
                fish1.move(sharkX,sharkY,1)
            elif fish1.getWallHitting == True and fish1.getFlee() == True:
                fish1.reversePos()
                fish1.setFlee(sharkX,sharkY)

            if fish2.getWallHitting == True and fish2.getFlee() == False:
                fish2.directionReverse()
                fish2.move(sharkX,sharkY,1)
            elif fish2.getWallHitting == True and fish2.getFlee() == True:
                fish2.reversePos()
                fish2.setFlee(sharkX,sharkY)

            if fish3.getWallHitting == True and fish3.getFlee() == False:
                fish3.directionReverse()
                fish3.move(sharkX,sharkY,1)
            elif fish3.getWallHitting == True and fish3.getFlee() == True:
                fish3.reversePos()
                fish3.setFlee(sharkX,sharkY)

              
            fishList = [fish1.getX(),fish1.getY(),fish1.getDirection(),fish1.getFlee(),fish1.getAlive(),fish2.getX(),fish2.getY(),fish2.getDirection(),fish2.getFlee(),fish2.getAlive(),fish3.getX(),fish3.getY(),fish3.getDirection(),fish3.getFlee(),fish3.getAlive()]

            print(fishList)
            
            GUI.updateFish(fishList)
            GUI.nextTurn()

        elif buttonClicked == "shark":

            fishList = [fish1.getX(),fish1.getY(),fish1.getDirection(),fish1.getFlee(),fish1.getAlive(),fish2.getX(),fish2.getY(),fish2.getDirection(),fish2.getFlee(),fish2.getAlive(),fish3.getX(),fish3.getY(),fish3.getDirection(),fish3.getFlee(),fish3.getAlive()]

            placeHolderList = shark.sharkTurn(fishList)
            sharkList = shark.getSharkList()

            sharkX,sharkY = shark.getPosition()

            if sharkX == fish1.getX() and sharkY == fish1.getY():
                fish1.eat()

            elif sharkX == fish2.getX() and sharkY == fish2.getY():
                fish2.eat()

            elif sharkX == fish3.getX() and sharkY == fish3.getY():
                fish3.eat()

            GUI.updateShark(sharkList)
            GUI.updateFish(fishList)
            GUI.nextTurn()

            print("shark",sharkList)

            if fish1.getAlive() == False and fish2.getAlive() == False and fish3.getAlive() == False:

                pass #display game over message

        elif buttonClicked == "quit":

            GUI.endGame()
            break

main()
