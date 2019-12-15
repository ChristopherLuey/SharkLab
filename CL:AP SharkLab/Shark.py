# File: Shark.py
# Date: 11/14/19
# Written By: Christopher Luey
# Shark class that calculates shark position relative to fish

from random import randrange

class Shark:
    """This class creates a "shark" which stores the theoretical positions and states,
    while following the requirements and design specifications.
    The shark calculates how it should change positions based on inputted theoretical fish coordinates and states.
    It initializes at theoretical coordinates of 7, 2.

    Attributes:
        self.x: current theoretical x position of shark
        self.y: current theoretical y position of shark
        self.dir: theoretical direction the shark is facing
        self.chasing: current theoretical fish the shark is chasing (0=noFishChasing, 1=chasingFish1, 2=chasingFish2, 3=chasingFish3)
    """

    def __init__(self):
        """Function creates the "shark" object which stores the position and state of the shark, while altering the position
        in relation to inputted fish coordinates."""
        self.x, self.y, self.dir, self.chasing = 7,2, 'East', 0


    def sharkTurn(self, fishList):
        """Function alters the x and y position of the shark in order to move the shark.
        New position is stored in shark object as self.x and self.y.

        Args:
            fishList: list of fish positions and states in format [f1x, f1y, f1dir, f1flee, f1alive, f2x, f2y, ...]

        Returns:
            sharkList: list of shark position and state in format [sharkx, sharky, dir, chasing]
        """
        # Find the fish the shark is chasing
        self.calculateFishChasing(fishList)

        # Find the x, y of the fish the shark is chasing in the fish list
        fishx, fishy = fishList[(self.chasing-1)*5], fishList[(self.chasing-1)*5+1]

        # Shark can move 2 spaces, so loop twice
        for i in ["Run", "Twice"]:
            self.move(fishx, fishy)

            # Check if shark has eaten the fish it's pursuing
            if fishx == self.x and fishy == self.y:
                fishList[(self.chasing-1) * 5 + 4] = False
                # Shark cannot move anymore after eating, so break out
                break

        return [self.x, self.y, self.dir, self.chasing]


    def getPosition(self):
        """Function returns the current theoretical position of the shark.

        Returns:
            x: x position of the shark
            y: y position of the shark
        """
        return self.x, self.y


    # Shark Helper Methods - Not Included in API Since They Should Not Be Called Outside of This Class
    def calculateFishChasing(self, fishList):
        """Function calculates which fish the shark should be chasing.

        Args:
            fishList: List of fish attributes in format [fish1x, fish1y, fish1dir, fish1flee, fish1IsAlive, fish2x, ...]
        """
        # Save the lowest fish distance, closest fish index, and how many fish need to be randomly chosen to pursue
        lowestFishDist, closeFishIndex, randomFishChooser = 1000, self.chasing, []

        for i in range(3):
            # Gather fish data
            fishx, fishy, alive = fishList[i*5], fishList[i*5+1], fishList[i*5+4]

            # Calculate dx and dy to fish and see how many tiles away the fish is
            # (considering diagonals by subtracting the smallest distance of the two axis distances)
            dx, dy, min = abs(self.x - fishx), abs(self.y - fishy), abs(self.x - fishx)
            if dy < dx: min = dy
            fishDist = dx+dy-min

            if fishDist < lowestFishDist and alive:
                # Set this fish as the closest
                lowestFishDist, closeFishIndex, randomFishChooser = fishDist, i+1, []

            elif fishDist == lowestFishDist and alive:
                randomFishChooser.append(i+1)

        randomFishChooser.append(closeFishIndex)
        for fish in randomFishChooser:
            # Check whether the fish the shark is currently chasing is in the list
            if fish == self.chasing:
                closeFishIndex = fish
                break
            else:
                # Randomly choose the fish the shark is chasing
                closeFishIndex = randomFishChooser[randrange(0, len(randomFishChooser))]
        self.chasing = closeFishIndex


    def move(self, fishx, fishy):
        """Function changes the shark position to swim to the fish.

        Args:
            fishx: Closest fish x-position
            fishy: Closest fish y-position
        """
        # Check for the direction that the shark should move in relation to the closest fish
        # Flip the inequality sign and swap variables to test for all 4 directions
        dir = ""
        for i in [0,1,2,3]:
            if self.x > fishx:
                dir, self.x = dir+["West", "South", "East", "North"][i], self.x-1
            fishx, fishy, self.x, self.y, self.dir = fishy*-1, fishx,self.y*-1, self.x, dir
