# File: SharkRunner.py
# Written by: Andreas Petrou-Zeniou
# Date: 12/10/19
# executes movement of fish and shark, communicates with GUI to draw on 10x10 grid

from Fish import *
from Shark import *
from SharkGUI import *
import time


def directionRel(fish1, fish2):
    # function directionRel returns the relationship of the directions of two fish, whether they are opposite of each other or the same,
    # and whether the fish are moving on the x or y axis.

    fish1direction = fish1.getDirection()
    fish2direction = fish2.getDirection()

    if fish1direction == fish2direction:
        return "same", ""

    else:
        if fish1direction == "west":
            if fish2direction == "east":
                return "opposite", "x"

        elif fish1direction == "east":
            if fish2direction == "west":
                return "opposite", "x"

        elif fish1direction == "north":
            if fish2direction == "south":
                return "opposite", "y"

        elif fish1direction == "south":
            if fish2direction == "north":
                return "opposite", "y"

    # if no special relation, returns empty strings

    return "", ""


def getDistance(fish1, fish2):
    # returns the distance between two fish

    distance = abs(fish1.getX() - fish2.getX()) + abs(fish1.getY() - fish2.getY())


def getFishList(fish1, fish2, fish3):
    # returns a list of fish data to be inputed into the GUI, which updates the graphic representations of fish
    return [fish1.getX(), fish1.getY(), fish1.getDirection(), fish1.getFlee(), fish1.getAlive(), fish2.getX(),
            fish2.getY(), fish2.getDirection(), fish2.getFlee(), fish2.getAlive(), fish3.getX(), fish3.getY(),
            fish3.getDirection(), fish3.getFlee(), fish3.getAlive()]


def collideMove(fish):
    # sequence of movements if fish has two movement options (on a diagonal with the shark) in case fish collides

    fish.directionReverse()
    fish.move(1)
    fish.collideSetDirection()
    fish.move(1)


def wallHitting(fishObject, sharkX, sharkY):
    # wall hitting scenario. If in flee, fish flips across grid. Otherwise, initiates wall bump sequence.

    # if the fish hits the wall and is not in flee mode, the fish will reverse direction and move one square in the GUI

    if fishObject.getWallHitting() == True and fishObject.getFlee() == False:
        fishObject.wallSetDirection()
        fishObject.move(2)

    # if the fish hits the wall and is in flee mode, the fish will flip across the grid

    elif fishObject.getWallHitting() == True and fishObject.getFlee() == True:
        fishObject.reversePos()


def collisionScenario(fish1, fish2, fish3, roundFish):
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


def getAliveList(fish1, fish2, fish3):
    # test each fish for alive status, and if so, add them to a list of alive fish. fishWin tracks the status of the fish winning throughout the module

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

    return deadNumber, aliveFishList


def fishWinTest(fish1, fish2, fish3, sharkX, sharkY):
    fishWin = False  # returns whether stalemate situation has been achieved

    deadNumber, aliveFishList = getAliveList(fish1, fish2, fish3)

    # if 2 fish are dead, test that the last fish is on the same axis. If on the same axis, test whether the fish is just out of the shark's reach.

    if deadNumber == 2:
        if aliveFishList[0].getX() == sharkX:
            if (aliveFishList[0].getY() == 9 or aliveFishList[0].getY() == 0) and 5 > abs(
                    aliveFishList[0].getY() - sharkY) > 2:
                fishWin = True

        elif aliveFishList[0].getY() == sharkY:
            if (aliveFishList[0].getX() == 9 or aliveFishList[0].getX() == 0) and 5 > abs(
                    aliveFishList[0].getX() - sharkX) > 2:
                fishWin = True

    # if 1 fish is dead, test which fish is on the same axis as the shark, and set that fish to index 0. Test if fish directions are the same, and then test distances to shark

    elif deadNumber == 1:
        if aliveFishList[0].getX() == sharkX or aliveFishList[1].getX() == sharkX or aliveFishList[
            0].getY() == sharkY or aliveFishList[1].getY() == sharkY:

            # set index of center fish to index 0

            if aliveFishList[0].getX() == sharkX or aliveFishList[0].getY() == sharkY and (
                    aliveFishList[1].getY() != sharkY and aliveFishList[1].getX() != sharkX):
                aliveFishList[0], aliveFishList[1] = aliveFishList[0], aliveFishList[1]

            elif aliveFishList[1].getX() == sharkX or aliveFishList[1].getY() == sharkY and (
                    aliveFishList[0].getY() != sharkY and aliveFishList[0].getX() != sharkX):
                aliveFishList[0], aliveFishList[1] = aliveFishList[1], aliveFishList[0]

            # situation where fish are right next to each other, facing the same direction and are both being chased by the shark

            if aliveFishList[0].getDirection() == aliveFishList[1].getDirection():

                if aliveFishList[0].getX() == sharkX:
                    if aliveFishList[0].getY() == aliveFishList[1].getY() and abs(
                            aliveFishList[0].getX() - aliveFishList[1].getX()) <= 4:
                        if (aliveFishList[0].getY() == 9 or aliveFishList[0].getY() == 0) and 5 > abs(
                                aliveFishList[0].getY() - sharkY) > 2:
                            fishWin = True

                elif aliveFishList[0].getY() == sharkY:
                    if aliveFishList[0].getX() == aliveFishList[1].getX() and abs(
                            aliveFishList[0].getY() - aliveFishList[1].getY()) <= 4:
                        if (aliveFishList[0].getX() == 9 or aliveFishList[0].getX() == 0) and 5 > abs(
                                aliveFishList[0].getX() - sharkX) > 2:
                            fishWin = True

            # alternate situation where 1 fish is getting chased, and the other is more than 6 spots away, making it impossible for the shark to switch chasing.

            relation, axis = directionRel(aliveFishList[0], aliveFishList[1])

            if relation == "same" or relation == "opposite":
                if axis == "x":
                    if aliveFishList[0].getY() == sharkY:
                        if abs(aliveFishList[0].getY() - aliveFishList[1].getY()) >= 7:
                            if (aliveFishList[0].getX() == 9 or aliveFishList[0].getX() == 0) and 5 > abs(
                                    aliveFishList[0].getX() - sharkX) > 2:
                                fishWin = True

                if axis == "y":
                    if aliveFishList[0].getX() == sharkX:
                        if abs(aliveFishList[0].getX() - aliveFishList[1].getX()) >= 7:
                            if (aliveFishList[0].getY() == 9 or aliveFishList[0].getY() == 0) and 5 > abs(
                                    aliveFishList[0].getY() - sharkY) > 2:
                                fishWin = True

    # no fish are dead

    elif deadNumber == 0:

        if aliveFishList[0].getX() == sharkX or aliveFishList[1].getX() == sharkX or aliveFishList[
            2].getX() == sharkX or aliveFishList[0].getY() == sharkY or aliveFishList[1].getY() == sharkY or \
                aliveFishList[2].getY() == sharkY:
            continueVar = False

            # reassign central fish to index zero

            if aliveFishList[0].getX() == sharkX or aliveFishList[0].getY() == sharkY and (
                    aliveFishList[1].getY() != sharkY and aliveFishList[1].getX() != sharkX and aliveFishList[
                2].getX() != sharkX and aliveFishList[2].getY() != sharkY):
                aliveFishList[0], aliveFishList[1], aliveFishList[2] = aliveFishList[0], aliveFishList[1], \
                                                                       aliveFishList[2]
                continueVar = True

            elif aliveFishList[1].getX() == sharkX or aliveFishList[1].getY() == sharkY and (
                    aliveFishList[0].getY() != sharkY and aliveFishList[0].getX() != sharkX and aliveFishList[
                2].getX() != sharkX and aliveFishList[2].getY() != sharkY):
                aliveFishList[0], aliveFishList[1], aliveFishList[2] = aliveFishList[1], aliveFishList[0], \
                                                                       aliveFishList[2]
                continueVar = True

            elif aliveFishList[2].getX() == sharkX or aliveFishList[2].getY() == sharkY and (
                    aliveFishList[0].getY() != sharkY and aliveFishList[0].getX() != sharkX and aliveFishList[
                1].getX() != sharkX and aliveFishList[1].getY() != sharkY):
                aliveFishList[0], aliveFishList[1], aliveFishList[2] = aliveFishList[2], aliveFishList[1], \
                                                                       aliveFishList[2]
                continueVar = True

            # test if all three fish are on the same direction, on the same axis, and the requisite distance from the shark

            if continueVar == True:  # this variable is used to ensure that only one fish is on the same axis as the shark
                if aliveFishList[0].getDirection() == aliveFishList[1].getDirection() == aliveFishList[
                    2].getDirection():
                    if aliveFishList[0].getX() == sharkX:
                        if aliveFishList[0].getY() == aliveFishList[1].getY() == aliveFishList[2].getY():
                            if (aliveFishList[0].getY() == 9 or aliveFishList[0].getY() == 0) and 5 > abs(
                                    aliveFishList[0].getY() - sharkY) > 0:
                                fishWin = True

                    elif aliveFishList[0].getY() == sharkY:
                        if aliveFishList[0].getX() == aliveFishList[1].getX() == aliveFishList[2].getX():
                            if (aliveFishList[0].getX() == 9 or aliveFishList[0].getX() == 0) and 5 > abs(
                                    aliveFishList[0].getX() - sharkX) > 0:
                                fishWin = True

            relation1, axis1 = directionRel(aliveFishList[0], aliveFishList[1])
            relation2, axis2 = directionRel(aliveFishList[0], aliveFishList[1])

            # test if shark is chasing at the top of the screen, while two fish are at the bottom, or vice versa

            if (relation1 == "same" or relation1 == "opposite") and (relation2 == "same" or relation2 == "opposite"):
                if aliveFishList[0].getX() == sharkX:
                    if (abs(aliveFishList[0].getX() - aliveFishList[1].getX()) >= 7 and abs(
                            aliveFishList[0].getX() - aliveFishList[2].getX()) >= 7) or (
                            abs(aliveFishList[0].getX() - aliveFishList[1].getX()) >= 7 and abs(
                            aliveFishList[0].getX() - aliveFishList[2].getX()) == 1) or (
                            abs(aliveFishList[0].getX() - aliveFishList[1].getX()) == 1 and abs(
                            aliveFishList[0].getX() - aliveFishList[2].getX()) >= 7):
                        if (aliveFishList[0].getY() == 9 or aliveFishList[0].getY() == 0) and 5 > abs(
                                aliveFishList[0].getY() - sharkY) > 2:
                            fishWin = True

                elif aliveFishList[0].getY() == sharkY:
                    if (abs(aliveFishList[0].getY() - aliveFishList[1].getY()) >= 7 and abs(
                            aliveFishList[0].getY() - aliveFishList[2].getY()) >= 7) or (
                            abs(aliveFishList[0].getY() - aliveFishList[1].getY()) >= 7 and abs(
                            aliveFishList[0].getY() - aliveFishList[2].getY()) == 1) or (
                            abs(aliveFishList[0].getY() - aliveFishList[1].getY()) == 1 and abs(
                            aliveFishList[0].getY() - aliveFishList[2].getY()) >= 7):
                        if (aliveFishList[0].getX() == 9 or aliveFishList[0].getX() == 0) and 5 > abs(
                                aliveFishList[0].getX() - sharkX) > 2:
                            fishWin = True

    return fishWin


def generateList():
    start = time.time()
    print(start)
    list = [[i,j,dir1,k,u,dir2,p,x,dir3]
            for i in range(10)
            for j in range(10)
            for k in range(10)
            for u in range(10)
            for p in range(10)
            for x in range(10)
            for dir1 in ['north', 'east', 'south', 'west']
            for dir2 in ['north', 'east', 'south', 'west']
            for dir3 in ['north', 'east', 'south', 'west']
            ]
    print((time.time()-start))

    return list
def main():
    # set up GUI, gather user input to feed into subsequent fish object constructor

    #GUI = SharkGUI()
    #GUIList = GUI.gatherUserInput()
    GUIList = generateList()
    print("list complete")
    timeRun = 1
    fishWinsTimes = 0
    staleMateCounter = 0
    sharks = 0
    f = open('data.txt', 'w')
    looping = True

    while looping == True:
        fishWins = 0  # use this variable to delay fish win message, accumulator variable


        for i in range(64000000):
            print(GUIList[timeRun][0], GUIList[timeRun][1], GUIList[timeRun][3], GUIList[timeRun][4],GUIList[timeRun][6], GUIList[timeRun][7])
            print(GUIList[timeRun][2], GUIList[timeRun][5], GUIList[timeRun][8])
            fish1 = Fish(GUIList[timeRun][0], GUIList[timeRun][1], "west", False, True, False, "DNE")
            fish2 = Fish(GUIList[timeRun][3], GUIList[timeRun][4], "west", False, True, False, "DNE")
            fish3 = Fish(GUIList[timeRun][6], GUIList[timeRun][7], "west", False, True, False, "DNE")
            fishListObjects = [fish1, fish2,
                               fish3]  # use this list to efficiently cycle through fish objects in repetitive sequences, order is 1, 2, 3
            fish1.setInputDirection(GUIList[timeRun][2])
            fish2.setInputDirection(GUIList[timeRun][5])
            fish3.setInputDirection(GUIList[timeRun][8])

            # construct shark, gather coordinates to set flee status of each fish, then set direction as well
            shark = Shark()
            sharkX, sharkY = shark.getPosition()

            for fishObject in fishListObjects:
                fishObject.setFlee(sharkX, sharkY)
                fishObject.setDirection(sharkX, sharkY)

            # update GUI to reflect these changes
            fishList = getFishList(fish1, fish2, fish3)
            #GUI.updateFish(fishList)
            iteration = 0
            check = True
            if GUIList[timeRun][0] == GUIList[timeRun][3] and GUIList[timeRun][1] == GUIList[timeRun][4]:
                check = False
            elif GUIList[timeRun][0] == GUIList[timeRun][6] and GUIList[timeRun][1] == GUIList[timeRun][7]:
                check = False
            elif GUIList[timeRun][3] == GUIList[timeRun][6] and GUIList[timeRun][4] == GUIList[timeRun][7]:
                check = False

            if GUIList[timeRun][0] == 7 and GUIList[timeRun][1] == 2:
                check = False

            if GUIList[timeRun][3] == 7 and GUIList[timeRun][4] == 2:
                check = False

            if GUIList[timeRun][6] == 7 and GUIList[timeRun][7] == 2:
                check = False

            while check:
                    sharkList = shark.getSharkList()
                    sharkX, sharkY = shark.getPosition()

                    for fishObject in fishListObjects:
                        fishObject.setFlee(sharkX, sharkY)

                    for fishObject in fishListObjects:
                        fishObject.setDirection(sharkX, sharkY)

                    for fishObject in fishListObjects:
                        fishObject.move(1)

                        # wall hitting scenario. If in flee, fish flips across grid. Otherwise, initiates wall bump sequence.
                        wallHitting(fishObject, sharkX, sharkY)

                        # collisions scenario, do after every round to ensure valid order
                        collisionScenario(fish1, fish2, fish3, fishObject)

                    fishList = getFishList(fish1, fish2, fish3)
                    #GUI.updateFish(fishList)
                    #GUI.nextTurn()

                    # fish Win situation, fishWin delays display of fish victory

                    if fishWinTest(fish1, fish2, fish3, sharkX, sharkY) == True:
                        fishWins += 1
                        if fishWins == 2:
                            #GUIList = GUI.winner("fish")
                            fishWinsTimes +=1
                            print("fish wins: ", fishWinsTimes, "  ", timeRun)
                            break


                    fishList = getFishList(fish1, fish2, fish3)

                    # move shark
                    shark.sharkTurn(fishList)
                    sharkList = shark.getSharkList()
                    sharkX, sharkY = shark.getPosition()

                    # eat fish
                    for fishObject in fishListObjects:
                        if sharkX == fishObject.getX() and sharkY == fishObject.getY() and fishObject.getAlive() == True:
                            fishObject.eat()
                            fishObject.setCoords(11, 11)  # use to avoid collisions after fish death

                    # update GUI
                    #GUI.updateShark(sharkList)
                    #GUI.updateFish(fishList)
                    #GUI.nextTurn()

                    # shark win situation
                    if fish3.getAlive() == False and fish1.getAlive() == False and fish2.getAlive() == False:
                        #GUIList = GUI.winner("shark")
                        sharks+=1
                        print("shark wins: ", sharks, "  ", timeRun)
                        break

                    iteration +=1
                    if iteration > 200:
                        print("Stalemate: ", GUIList[timeRun][0], GUIList[timeRun][1], GUIList[timeRun][3],
                              GUIList[timeRun][4], GUIList[timeRun][6], GUIList[timeRun][7], file=f, end=" ")
                        print(GUIList[timeRun][2], GUIList[timeRun][5], GUIList[timeRun][8], file=f)
                        staleMateCounter+=1
                        break
            timeRun+=1

main()