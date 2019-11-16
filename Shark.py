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
        fishx, fishy = fishList[(self.chasing-1)*5], fishList[(self.chasing-1)*5+1]
        for i in range(2):
            self.calculatePath(fishx, fishy)

            if fishx == self.x and fishy == self.y:
                fishList[(self.chasing-1)*5+4] = True
                break

        return self.getSharkList(), fishList


    def getPosition(self):
        return self.x, self.y


    def getChasing(self):
        return self.chasing


    def getSharkList(self):
        return [self.x, self.y, self.dir, self.chasing]


    # Shark Class helper methods, isn't part of API because they shouldn't be called outside of this class
    def calculateFishChasing(self, fishList):
        lowFishDist, closeFish, randomFish = 1000.0, self.chasing, 1
        for i in range(3):
            fishx, fishy = fishList[i*5], fishList[i*5+1]
            fishDist = ((self.x - fishx) ** 2 + (self.y - fishy) ** 2) ** 1 / 2
            print(fishx, fishy, fishDist)
            if fishDist < lowFishDist and not fishList[i*5+4]:
                lowFishDist, closeFish = fishDist, i+1

            elif fishDist == lowFishDist and not fishList[i*5+4] and not(self.chasing == i+1) and not(self.chasing == closeFish):
                randomFish+=1

        if randomFish > 1:
            closeFish = random.randrange(1,randomFish+1)

        self.chasing = closeFish


    def calculatePath(self, fishx, fishy):
        moveN = self.x == fishx and self.y > fishy
        moveS = self.x == fishx and self.y < fishy
        moveE = self.x < fishx and self.y == fishy
        moveW = self.x > fishx and self.y == fishy
        moveNE = self.x < fishx and self.y > fishy
        moveSE = self.x < fishx and self.y < fishy
        moveSW = self.x > fishx and self.y < fishy
        moveNW = self.x > fishx and self.y > fishy

        if moveNE: self.move('ne')
        elif moveSE: self.move('se')
        elif moveSW: self.move('sw')
        elif moveNW: self.move('nw')
        elif moveN: self.move('n')
        elif moveS: self.move('s')
        elif moveE: self.move('e')
        elif moveW: self.move('w')


    def move(self, dir):
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
