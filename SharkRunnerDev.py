#File: SharkRunnerDev.py

from Fish import *
from Shark import *

def genList():

    directionList = ["north","south","west","east"]

    allFishSituationList = []

    for fish1x in range(10):
        fishIndivSituationList = []
        for fish1y in range(10):
            if (fish1x != 7 and fish1y !=2):
                fishIndivSituationList.append(fish1x)
                fishIndivSituationList.append(fish1y)
                for fish1dir in directionList:
                    fishIndivSituationList.append(fish1dir)
                    
                    for fish2x in range(10):
                        for fish2y in range(10):
                            if (fish2x != fish1x or fish2y != fish1y) and (fish2x != 7 and fish2y !=2):
                                fishIndivSituationList.append(fish2x)
                                fishIndivSituationList.append(fish2y)
                                for fish2dir in directionList:
                                    fishIndivSituationList.append(fish2dir)

                                    for fish3x in range(10):
                                        for fish3y in range(10):
                                            if (fish3x != fish2x or fish3x != fish1x) and (fish3y != fish2y or fish3y != fish1y) and (fish3x != 7 and fish3y !=2):
                                                fishIndivSituationList.append(fish3x)
                                                fishIndivSituationList.append(fish3y)
                                                for fish3dir in directionList:
                                                    fishIndivSituationList.append(fish3dir)

                                                    allFishSituationList.append(fishIndivSituationList)


    return allFishSituationList

    

def directionRel(fish1,fish2):

    #function directionRel returns the relationship of the directions of two fish, whether they are opposite of each other or the same, and whether the fish are moving on the x or y axis.

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

def wallHitting(fishObject,sharkX,sharkY):

    #wall hitting scenario. If in flee, fish flips across grid. Otherwise, initiates wall bump sequence.

    #if the fish hits the wall and is not in flee mode, the fish will reverse direction and move one square in the GUI

    if fishObject.getWallHitting() ==  True and fishObject.getFlee() == False:
        fishObject.wallSetDirection()
        fishObject.move(2)

    #if the fish hits the wall and is in flee mode, the fish will flip across the grid
        
    elif fishObject.getWallHitting() ==  True and fishObject.getFlee() == True:
        fishObject.reversePos()

def collisionScenario(fish1,fish2,fish3,roundFish):

    if roundFish.getAlive() == True:

        fishList = []

        if roundFish == fish1:
            if fish2.getAlive() == True:
                fishList.append(fish2)
            if fish3.getAlive() == True:
                fishList.append(fish3)
        elif roundFish == fish2:
            if fish1.getAlive() == True:
                fishList.append(fish1)
            if fish3.getAlive() == True:
                fishList.append(fish3)
        elif roundFish == fish3:
            if fish1.getAlive() == True:
                fishList.append(fish1)
            if fish2.getAlive() == True:
                fishList.append(fish2)

        collisionRound = 0

        for collideFish in fishList:

            if roundFish.getX() == collideFish.getX() and roundFish.getY() == collideFish.getY():

                if roundFish.getFlee() == True and collisionRound != 0:
                    collideMove(roundFish)
                    collisionRound += 1
                else:
                    roundFish.move(-1)

def getAliveList(fish1,fish2,fish3):

    #test each fish for alive status, and if so, add them to a list of alive fish. fishWin tracks the status of the fish winning throughout the module

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

    return deadNumber,aliveFishList 

def fishWinTest(fish1,fish2,fish3,sharkX,sharkY):

    fishWin = False

    deadNumber,aliveFishList = getAliveList(fish1,fish2,fish3)

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
        if aliveFishList[0].getX() == sharkX or aliveFishList[1].getX() == sharkX or aliveFishList[0].getY() == sharkY or aliveFishList[1].getY() == sharkY:

            #set index of center fish to index 0

            if aliveFishList[0].getX() == sharkX or aliveFishList[0].getY() == sharkY and (aliveFishList[1].getY() != sharkY and aliveFishList[1].getX() != sharkX):
                aliveFishList[0],aliveFishList[1] = aliveFishList[0],aliveFishList[1]
                
            elif aliveFishList[1].getX() == sharkX or aliveFishList[1].getY() == sharkY and (aliveFishList[0].getY() != sharkY and aliveFishList[0].getX() != sharkX):
                aliveFishList[1],aliveFishList[0] = aliveFishList[0],aliveFishList[1]

            #situation where fish are right next to each other, facing the same direction and are both being chased by the shark

            if aliveFishList[0].getDirection() == aliveFishList[1].getDirection():

                if aliveFishList[0].getX() == sharkX:
                    if aliveFishList[0].getY() == aliveFishList[1].getY() and abs(aliveFishList[0].getX() - aliveFishList[1].getX()) <= 4:
                        if (aliveFishList[0].getY() == 9 or aliveFishList[0].getY() == 0) and 5 > abs(aliveFishList[0].getY() - sharkY) > 2:
                            fishWin = True
                                    
                elif aliveFishList[0].getY() == sharkY:
                    if aliveFishList[0].getX() == aliveFishList[1].getX() and abs(aliveFishList[0].getY() - aliveFishList[1].getY()) <= 4:
                        if (aliveFishList[0].getX() == 9 or aliveFishList[0].getX() == 0) and 5 > abs(aliveFishList[0].getX() - sharkX) > 2:
                            fishWin = True

            #alternate situation where 1 fish is getting chased, and the other is more than 6 spots away, making it impossible for the shark to switch chasing.

            relation,axis = directionRel(aliveFishList[0],aliveFishList[1])

            if relation == "same" or relation == "opposite":
                if axis == "x":
                    if aliveFishList[0].getX() == sharkX:
                        if abs(aliveFishList[0].getX() - aliveFishList[1].getX()) >= 7:
                            if (aliveFishList[0].getY() == 9 or aliveFishList[0].getY() == 0) and 5 > abs(aliveFishList[0].getY() - sharkY) > 2:
                                fishWin = True

                if axis == "y":  
                    if aliveFishList[0].getY() == sharkY:
                        if abs(aliveFishList[0].getY() - aliveFishList[1].getY()) >= 7:
                            if (aliveFishList[0].getX() == 9 or aliveFishList[0].getX() == 0) and 5 > abs(aliveFishList[0].getX() - sharkX) > 2:
                                fishWin = True

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
                
            if continueVar == True: #this variable is used to ensure that only one fish is on the same axis as the shark
                if aliveFishList[0].getDirection() == aliveFishList[1].getDirection() == aliveFishList[2].getDirection():
                    if aliveFishList[0].getX() == sharkX:
                        if aliveFishList[0].getY() == aliveFishList[1].getY() == aliveFishList[2].getY():
                            if (aliveFishList[0].getY() == 9 or aliveFishList[0].getY() == 0) and 5 > abs(aliveFishList[0].getY() - sharkY) > 0:
                                fishWin = True
                                        
                    elif aliveFishList[0].getY() == sharkY:
                        if aliveFishList[0].getX() == aliveFishList[1].getX() == aliveFishList[2].getX():
                            if (aliveFishList[0].getX() == 9 or aliveFishList[0].getX() == 0) and 5 > abs(aliveFishList[0].getX() - sharkX) > 0:
                                fishWin = True

            relation1,axis1 = directionRel(aliveFishList[0],aliveFishList[1])
            relation2,axis2 = directionRel(aliveFishList[0],aliveFishList[1])

            #test if shark is chasing at the top of the screen, while two fish are at the bottom.

            if (relation1 == "same" or relation1 == "opposite") and (relation2 == "same" or relation2 == "opposite"):
                if aliveFishList[0].getX() == sharkX:
                    if (abs(aliveFishList[0].getX() - aliveFishList[1].getX()) >= 7 and abs(aliveFishList[0].getX() - aliveFishList[2].getX()) >= 7) or (abs(aliveFishList[0].getX() - aliveFishList[1].getX()) >= 7 and abs(aliveFishList[0].getX() - aliveFishList[2].getX()) == 1) or (abs(aliveFishList[0].getX() - aliveFishList[1].getX()) == 1 and abs(aliveFishList[0].getX() - aliveFishList[2].getX()) >= 7):
                        if (aliveFishList[0].getY() == 9 or aliveFishList[0].getY() == 0) and 5 > abs(aliveFishList[0].getY() - sharkY) > 2:
                            fishWin = True
                                    
                elif aliveFishList[0].getY() == sharkY:
                    if (abs(aliveFishList[0].getY() - aliveFishList[1].getY()) >= 7 and abs(aliveFishList[0].getY() - aliveFishList[2].getY()) >= 7) or (abs(aliveFishList[0].getY() - aliveFishList[1].getY()) >= 7 and abs(aliveFishList[0].getY() - aliveFishList[2].getY()) == 1) or (abs(aliveFishList[0].getY() - aliveFishList[1].getY()) == 1 and abs(aliveFishList[0].getY() - aliveFishList[2].getY()) >= 7):
                        if (aliveFishList[0].getX() == 9 or aliveFishList[0].getX() == 0) and 5 > abs(aliveFishList[0].getX() - sharkX) > 2:
                            fishWin = True
                                    
    return fishWin

def main():

    sharkWins = 0
    fishWins = 0

    Fish1Win = 0
    Fish2Win = 0
    Fish3Win = 0

    fish1SingleWin = 0
    fish2SingleWin = 0
    fish3SingleWin = 0

    bigFishList = genList()
    print("list generation complete")

    combos = len(bigFishList)

    for smallFishList in bigFishList:

        try:

            print(smallFishList[0])

            print("x")

            fish1 = Fish(smallFishList[0],smallFishList[1],"west",False,True,False,"DNE")
            fish2 = Fish(smallFishList[3],smallFishList[4],"west",False,True,False,"DNE")
            fish3 = Fish(smallFishList[6],smallFishList[7],"west",False,True,False,"DNE")
            fishListObjects = [fish1,fish2,fish3] #use this list to efficiently cycle through fish objects in repetitive sequences, order is 1, 2, 3

            fish1.setInputDirection(smallFishList[2])
            fish2.setInputDirection(smallFishList[5])
            fish3.setInputDirection(smallFishList[8])

            print(fish1.getCoords(),fish1.getDirection())
            print(fish2.getCoords(),fish2.getDirection())
            print(fish3.getCoords(),fish3.getDirection())
            
            
            #construct shark, gather coordinates to set flee status of each fish, then set direction as well
            
            shark = Shark()
            sharkX,sharkY = shark.getPosition()

            for fishObject in fishListObjects:
                fishObject.setFlee(sharkX,sharkY)
                fishObject.setDirection(sharkX,sharkY)

                noRounds = 0

            while True:

                sharkList = shark.getSharkList()
                sharkX,sharkY = shark.getPosition()

                for fishObject in fishListObjects:
                    fishObject.setFlee(sharkX,sharkY)
                    
                for fishObject in fishListObjects:
                    fishObject.setDirection(sharkX,sharkY)
                    
                for fishObject in fishListObjects:
                    fishObject.move(1)

                    #wall hitting scenario. If in flee, fish flips across grid. Otherwise, initiates wall bump sequence.

                    wallHitting(fishObject,sharkX,sharkY)

                    #collisions scenario, do after every round to ensure valid order
                
                    collisionScenario(fish1,fish2,fish3,fishObject)

                print("d")

                #fish Win situation, fishWin delays display of fish victory

                if fishWinTest(fish1,fish2,fish3,sharkX,sharkY) == True:

                    print("b")
                    
                    fishWins += 1

                    fishAliveList = getAliveList(fish1,fish2,fish3)

                    if len(fishAliveList) == 1:
                        fish1Win += 1

                        if fishAliveList[0] == fish1:
                            fish1SingleWin += 1

                        elif fishAliveList[0] == fish2:
                            fish2SingleWin += 1

                        elif fishAliveList[0] == fish3:
                            fish3SingleWin += 1

                    elif len(fishAliveList) == 2:
                        fish2Win += 1

                    elif len(fishAliveList) == 3:
                        fish3Win += 1

                    break

                #move shark

                shark.sharkTurn(fishList)
                sharkList = shark.getSharkList()
                sharkX,sharkY = shark.getPosition()

                print("c")

                #eat fish

                for fishObject in fishListObjects:
                    if sharkX == fishObject.getX() and sharkY == fishObject.getY() and fishObject.getAlive() == True:
                        fishObject.eat()
                        fishObject.setCoords(11,11) #use to avoid collisions after fish death

                #shark win situation

                if fish3.getAlive() == False and fish1.getAlive() == False and fish2.getAlive() == False:

                    print("a")

                    SharkWins += 1

                    break

                noRounds += 1

        except:

            print(smallFishList,"generates an error")

    print("there are this many combinations:",combos)
    print("shark wins this many times:",sharkWins)
    print("fish wins this many times:",fishWins)
    print("there are this many single fish wins:",fish1win)
    print("there are this many double fish wins:",fish2win)
    print("there are this many triple fish wins:",fish3win)
    print("fish 1 is the single winner this many times:",fish1SingleWin)
    print("fish 2 is the single winner this many times:",fish2SingleWin)
    print("fish 3 is the single winner this many times:",fish3SingleWin)
        
main()
