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

    if GUI.isClicked() == "start":

        fishList = [fish1.getX(),fish1.getY(),fish1.getDirection(),fish1.getFlee(),fish1.getAlive(),fish2.getX(),fish2.getY(),fish2.getDirection(),fish2.getFlee(),fish2.getAlive(),fish3.getX(),fish3.getY(),fish3.getDirection(),fish3.getFlee(),fish3.getAlive()]

        GUI.updateFish(fishList)

    if GUI.isClicked() == "fish":

        sharkList = shark.getSharkList()

        sharkX,sharkY = shark.getPosition()

        fish1.move(sharkX,sharkY,1)
        fish2.move(sharkX,sharkY,1)
        fish3.move(sharkX,sharkY,1)

        #wall situation

        if (fish1.getX() < 0 or fish1.getX() > 9) or (fish1.getY() < 0 or fish1.getY() > 9):
            fish1.directionReverse()
            fish1.move(sharkX,sharkY,2)

        if (fish2.getX() < 0 or fish2.getX() > 9) or (fish2.getY() < 0 or fish2.getY() > 9):
            fish2.directionReverse()
            fish2.move(sharkX,sharkY,2)

        if (fish3.getX() < 0 or fish3.getX() > 9) or (fish3.getY() < 0 or fish3.getY() > 9):
            fish3.directionReverse()
            fish3.move(sharkX,sharkY,2)                                       
          
        fishList = [fish1.getX(),fish1.getY(),fish1.getDirection(),fish1.getFlee(),fish1.getAlive(),fish2.getX(),fish2.getY(),fish2.getDirection(),fish2.getFlee(),fish2.getAlive(),fish3.getX(),fish3.getY(),fish3.getDirection(),fish3.getFlee(),fish3.getAlive()]

        GUI.updateFish(fishList)

    if GUI.isClicked() == "shark":

        shark.sharkTurn(fishList)
        sharkList = shark.getSharkList()

        

        
        







main()
