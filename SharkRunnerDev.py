#File: SharkRunnerDev.py

from Fish import *
from Shark import *
import time
from random import randrange

def genList():

    directionList = ["north","south","west","east"]

    allFishSituationList = []

    #randGen

    noLists = 0

    while noLists < 1000:

        smallFishSituationList = []

        fish1x = randrange(10)
        fish1y = randrange(10)

        if not(fish1x == 7 and fish1y == 2):
            smallFishSituationList.append(fish1x)
            smallFishSituationList.append(fish1y)
            fish1dir = directionList[randrange(4)]
            smallFishSituationList.append(fish1dir)

        fish2x = randrange(10)
        fish2y = randrange(10)

        if not(fish2x == 7 and fish2y == 2):
            if not (fish2x == fish1x and fish2y == fish1y):
                smallFishSituationList.append(fish2x)
                smallFishSituationList.append(fish2y)
                fish2dir = directionList[randrange(4)]
                smallFishSituationList.append(fish2dir)

        fish3x = randrange(10)
        fish3y = randrange(10)

        if not(fish3x == 7 and fish3y == 2):
            if not (fish3x == fish1x and fish3y == fish1y) and not(fish3x == fish2x and fish3y == fish2y):
                smallFishSituationList.append(fish3x)
                smallFishSituationList.append(fish3y)
                fish3dir = directionList[randrange(4)]
                smallFishSituationList.append(fish3dir)
                
        if len(smallFishSituationList) == 9:
            allFishSituationList.append(smallFishSituationList)
            noLists += 1

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


def main():

    sharkWins = 0
    fishWins = 0

    fish1Win = 0
    fish2Win = 0
    fish3Win = 0

    fish1SingleWin = 0
    fish2SingleWin = 0
    fish3SingleWin = 0

    statusList = []

    bigFishList = genList()
    print("list generation complete")
    print(str(len(bigFishList)))

    a = input("yes")

    combos = len(bigFishList)

    noRoundsOverall = 0

    a = time.time()

    for smallFishList in bigFishList:

        noRoundsOverall += 1
        print(noRoundsOverall)

        if noRoundsOverall == 1000:
            b = time.time()
            print(b - a)

        fish1 = Fish(smallFishList[0],smallFishList[1],"west",False,True,False,"DNE")
        fish2 = Fish(smallFishList[3],smallFishList[4],"west",False,True,False,"DNE")
        fish3 = Fish(smallFishList[6],smallFishList[7],"west",False,True,False,"DNE")
        fishListObjects = [fish1,fish2,fish3] #use this list to efficiently cycle through fish objects in repetitive sequences, order is 1, 2, 3

        fish1.setInputDirection(smallFishList[2])
        fish2.setInputDirection(smallFishList[5])
        fish3.setInputDirection(smallFishList[8])
        
        
        #construct shark, gather coordinates to set flee status of each fish, then set direction as well
        
        shark = Shark()
        sharkX,sharkY = shark.getPosition()

        for fishObject in fishListObjects:
            fishObject.setFlee(sharkX,sharkY)
            fishObject.setDirection(sharkX,sharkY)

        noRounds = 0

        looping = True

        while looping == True:

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

            #fish Win situation, fishWin delays display of fish victory

            if fishWinTest(fish1,fish2,fish3,sharkX,sharkY,statusList) == True:
                
                fishWins += 1

                deadNumber,fishAliveList = getAliveList(fish1,fish2,fish3)

                if deadNumber == 1:
                    fish1Win += 1

                    if fishAliveList[0] == fish1:
                        fish1SingleWin += 1

                    elif fishAliveList[0] == fish2:
                        fish2SingleWin += 1

                    elif fishAliveList[0] == fish3:
                        fish3SingleWin += 1

                elif deadNumber == 2:
                    fish2Win += 1

                elif deadNumber == 3:
                    fish3Win += 1

                looping = False

            #move shark

            fishList = getFishList(fish1,fish2,fish3)

            shark.sharkTurn(fishList)
            sharkList = shark.getSharkList()
            sharkX,sharkY = shark.getPosition()

            #eat fish

            for fishObject in fishListObjects:
                if sharkX == fishObject.getX() and sharkY == fishObject.getY() and fishObject.getAlive() == True:
                    fishObject.eat()
                    fishObject.setCoords(11,11) #use to avoid collisions after fish death

            #shark win situation

            if fish3.getAlive() == False and fish1.getAlive() == False and fish2.getAlive() == False:

                sharkWins += 1

                looping = False

            noRounds += 1

            if noRounds > 1000:

                print("following stalemate")
                print(fish1.getCoords(),fish1.getDirection())
                print(fish2.getCoords(),fish2.getDirection())
                print(fish3.getCoords(),fish3.getDirection())
                print("initial coords")
                for thing in smallFishList:
                    print(thing,end=" ")

                looping = False

    print("there are this many combinations:",combos)
    print("shark wins this many times:",sharkWins)
    print("fish wins this many times:",fishWins)
    print("there are this many single fish wins:",fish1Win)
    print("there are this many double fish wins:",fish2Win)
    print("there are this many triple fish wins:",fish3Win)
    print("fish 1 is the single winner this many times:",fish1SingleWin)
    print("fish 2 is the single winner this many times:",fish2SingleWin)
    print("fish 3 is the single winner this many times:",fish3SingleWin)
        
main()