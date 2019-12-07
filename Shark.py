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
        # Return the fish list because some fish may have been killed
        return fishList

    def getPosition(self):
        return self.x, self.y

    def getSharkList(self):
        return [self.x, self.y, self.dir]

    # Shark Helper Methods - Not Included in API Since They Should Not Be Called Outside of This Class
    def calculateFishChasing(self, fishList):
        # Save the lowest fish distance, closest fish index, and how many fish need to be randomly chosen to pursue
        lowestFishDist, closeFishIndex, randomFishChooser = 1000.0, self.chasing, []
        for i in range(3):
            fishx, fishy, alive = fishList[i*5], fishList[i*5+1], fishList[i*5+4]
            dx, dy = abs(self.x - fishx), abs(self.y - fishy)
            fishDist = abs(dx+dy) - min([dx,dy])

            if fishDist < lowestFishDist and alive:
                lowestFishDist, closeFishIndex = fishDist, i+1
            elif fishDist == lowestFishDist and alive and not(self.chasing == i+1) and not(self.chasing == closeFishIndex):
                randomFishChooser.append(i+1)

        if bool(randomFishChooser):
            randomFishChooser.append(closeFishIndex)
            closeFishIndex = randomFishChooser[randrange(0,len(randomFishChooser))]

        self.chasing = closeFishIndex

    def move(self, fishx, fishy):
        dir = ""
        if self.y > fishy:
            dir = "North"
            self.y -= 1
        elif self.y < fishy:
            dir = "South"
            self.y += 1
        if self.x > fishx:
            dir+="West"
            self.x -= 1
        elif self.x < fishx:
            dir+="East"
            self.x += 1
        self.dir = dir
