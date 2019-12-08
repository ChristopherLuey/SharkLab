# File: Shark.py
# Date: 11/14/19
# Written By: Christopher Luey
# Shark class that calculates shark position relative to fish

from random import randrange

class Shark:

    def __init__(self):
        self.x, self.y, self.dir, self.chasing = 7, 2, 'East', 0

    def sharkTurn(self, fishList):
        # Find the fish the shark is chasing
        self.calculateFishChasing(fishList)
        # Find the x, y of the fish the shark is chasing in the fish list
        fishx, fishy = fishList[(self.chasing-1)*5], fishList[(self.chasing-1)*5+1]
        # Shark can move 2 spaces, so loop twice
        for i in range(2):
            self.move(fishx, fishy)
            # Check if shark has eaten the fish it's pursuing
            if fishx == self.x and fishy == self.y:
                # Set the fish to dead
                fishList[(self.chasing-1)*5+4] = False
                # Shark cannot move anymore after eating, so break out
                break

    def getPosition(self): return self.x, self.y

    def getSharkList(self): return [self.x, self.y, self.dir]

    # Shark Helper Methods - Not Included in API Since They Should Not Be Called Outside of This Class
    def calculateFishChasing(self, fishList):
        # Save the lowest fish distance, closest fish index, and how many fish need to be randomly chosen to pursue
        lowestFishDist, closeFishIndex, randomFishChooser = 1000, self.chasing, []
        for i in range(3):
            # Gather fish data
            fishx, fishy, alive = fishList[i*5], fishList[i*5+1], fishList[i*5+4]

            # Calculate dx and dy to fish and see how many tiles away the fish is (considering diagonals too)
            fishDist = abs(self.x - fishx)+abs(self.y - fishy) - min([abs(self.y - fishy),abs(self.x - fishx)])

            if fishDist < lowestFishDist and alive:
                # Set this fish as the closest
                lowestFishDist, closeFishIndex, randomFishChooser = fishDist, i+1, []

            elif fishDist == lowestFishDist and alive:
            #not(self.chasing == i+1) and not(self.chasing == closeFishIndex):
                randomFishChooser.append(i+1)

        # Check if the list has fish to be randomly chosen
        if bool(randomFishChooser):
            randomFishChooser.append(closeFishIndex)
            # Chose a random fish to chase
            closeFishIndex = randomFishChooser[randrange(0,len(randomFishChooser))]
        self.chasing = closeFishIndex

    def move(self, fishx, fishy):
        dir = ""
        for i in [0,1]:
            if self.y > fishy:
                dir, self.y = dir+["North", "South"][i], self.y-1
            fishy, self.y = fishy*-1, self.y*-1
        for i in [0,1]:
            if self.x > fishx:
                dir, self.x = dir+["West", "East"][i], self.x-1
            fishx, self.x = fishx*-1, self.x*-1
        self.dir = dir
