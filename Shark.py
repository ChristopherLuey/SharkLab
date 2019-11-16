# File: Shark.py
# Date: 11/14/19
# Written By: Christopher Luey
# Shark class for SharkRunner.py

import random

class Shark:

    def __init__(self):
        self.x = 7
        self.y = 2
        self.dir = 'e'
        self.chasing = 0
        self.attributes = self.getSharkList()


    def sharkTurn(self, fishList):
        self.calculateFishChasing(fishList)

        # Find the x, y of the fish the shark is chasing in the fish list
        fishx, fishy = fishList[(self.chasing-1)*5], fishList[(self.chasing-1)*5+1]

        # Shark can move 2 times, so loop twice
        for i in range(2):
            self.calculatePath(fishx, fishy)

            # Check if shark has eaten the fish it's pursuing
            if fishx == self.x and fishy == self.y:
                # Set the fish to dead
                fishList[(self.chasing-1)*5+4] = True
                # Shark cannot move, so break out
                break

        # Return the fish list because some fish may have been killed
        return fishList


    def getPosition(self):
        return self.x, self.y


    def getChasing(self):
        return self.chasing


    def getSharkList(self):
        return [self.x, self.y, self.dir, self.chasing]


    # Shark Helper Methods - Not Included in API Since They Should Not Be Called Outside of This Class
    def calculateFishChasing(self, fishList):
        # Save the lowest fish distance, closest fish index, and how many fish need to be
        lowestFishDist, closeFishIndex, randomFishChooser = 1000.0, self.chasing, []
        for i in range(3):
            fishx, fishy, dead = fishList[i*5], fishList[i*5+1], fishList[i*5+4]
            fishDist = ((self.x - fishx) ** 2 + (self.y - fishy) ** 2) ** 1 / 2

            if fishDist < lowestFishDist and not dead:
                lowestFishDist, closeFishIndex = fishDist, i+1

            elif fishDist == lowestFishDist and not dead and not(self.chasing == i+1) and not(self.chasing == closeFishIndex):
                randomFishChooser.append(i+1)

        if bool(randomFishChooser):
            randomFishChooser.append(closeFishIndex)
            closeFishIndex = randomFishChooser[random.randrange(0,len(randomFishChooser))]

        self.chasing = closeFishIndex


    def calculatePath(self, fishx, fishy):
        # Determine fish position relative to shark
        moveN = self.x == fishx and self.y > fishy
        moveS = self.x == fishx and self.y < fishy
        moveE = self.x < fishx and self.y == fishy
        moveW = self.x > fishx and self.y == fishy
        moveNE = self.x < fishx and self.y > fishy
        moveSE = self.x < fishx and self.y < fishy
        moveSW = self.x > fishx and self.y < fishy
        moveNW = self.x > fishx and self.y > fishy

        # Run move commands to swim closer to fish
        if moveNE: self.move('ne')
        elif moveSE: self.move('se')
        elif moveSW: self.move('sw')
        elif moveNW: self.move('nw')
        elif moveN: self.move('n')
        elif moveS: self.move('s')
        elif moveE: self.move('e')
        elif moveW: self.move('w')


    def move(self, dir):
        # Change the x, y position of the shark depending on direction desired
        if dir == 'n': self.y -= 1
        elif dir == 'e': self.x += 1
        elif dir == 's': self.y += 1
        elif dir == 'w': self.x -= 1

        elif dir == 'ne':
            self.y -= 1
            self.x += 1
        elif dir == 'se':
            self.y += 1
            self.x += 1
        elif dir == 'sw':
            self.y += 1
            self.x -= 1
        elif dir == 'nw':
            self.y -= 1
            self.x -= 1
