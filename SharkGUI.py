# File: SharkGUI.py
# Date: 11/14/19
# Written By: Christopher Luey
# Manages all GUI events for SharkRunner.py

from Button import *
import time

class SharkGUI:
    def __init__(self):
        self.color = [color_rgb(26, 117, 208), 'white', color_rgb(28,69,135)]
        self.createWin()

    def gatherUserInput(self):
        if not self.win.isClosed():
            self.updateShark([7,2,'East',0])
            self.start.toggleActivation()
            p = self.win.getMouse()
            while not self.quitButton.isClicked(p):
                if self.start.isClicked(p):

                    self.entry1.setFill(color_rgb(26, 188, 156))
                    self.entry2.setFill(color_rgb(26, 188, 156))
                    self.entry3.setFill(color_rgb(26, 188, 156))

                    # Gather user entries
                    fishList, entry1, entry2, entry3 = [], self.entry1.getText(), self.entry2.getText(), self.entry3.getText()

                    # For each entry
                    for i in range(3):
                        # Check if it is properly formatted with m,n
                        # This means entry must be 3 chars long, must include a comma at the second char, and the first and third chars must be from 0-9
                        if len(entry1) == 3 and entry1[1] == "," and 48<=ord(entry1[0])<=57 and 48<=ord(entry1[2])<=57:
                            # Add this to the fish attributes list which will be passed into updateFish()
                            fishList.extend([int(entry1[0]), int(entry1[2]), 'east', False, True])
                            # Set the entry to green
                            self.entry1.setFill(color_rgb(26, 188, 156))
                        else:
                            # Set the entry to red
                            self.entry1.setFill(color_rgb(192, 57, 43))
                            # Inform user of incorrect formatting of coords
                            self.instructionsText.setText("Your inputted points are formatted\nincorrectly. Please try again.")

                        # Swap values so every entry is checked
                        entry1, entry2, entry3, self.entry1, self.entry2, self.entry3 = entry2, entry3, entry1, self.entry2, self.entry3, self.entry1

                    # If the list has 15 items, every fish coord must have been valid
                    if len(fishList) == 15:
                        # Check for any overlapping coords
                        invalid = False
                        # Store all 3 fishes x,y
                        f1x, f2x, f3x = fishList[0], fishList[5], fishList[10]
                        f1y, f2y, f3y = fishList[1], fishList[6], fishList[11]
                        for i in range(3):
                            # Compare all fish coords to each other and shark
                            if (f1x == f2x and f1y == f2y) or (f1x == 7 and f1y == 2):
                                self.entry1.setFill(color_rgb(192, 57, 43))
                                self.entry2.setFill(color_rgb(192, 57, 43))
                                self.entry3.setFill(color_rgb(192, 57, 43))
                                self.instructionsText.setText("Your inputted fish points overlap\nwith other fish or the shark.\nPlease try again.")
                                invalid = True
                            # Swap values so everything is checked
                            f1x, f2x, f3x = f2x, f3x, f1x
                            f1y, f2y, f3y = f2y, f3y, f1y

                        if not invalid:
                            # Display fish and shark on the board
                            self.fishButton.toggleActivation()
                            self.storedFish = fishList
                            self.entry1.undraw()
                            self.entry2.undraw()
                            self.entry3.undraw()
                            self.enterFish1.undraw()
                            self.enterFish2.undraw()
                            self.enterFish3.undraw()
                            self.start.undraw()
                            self.instructionsText.setText("Click on the fish button to move\nthe fish")
                            self.anim(1035, 220, self.instructionsText.getAnchor().getX(), self.instructionsText.getAnchor().getY(), self.instructionsText)
                            self.anim(1035, 180, self.instructionsTitle.getAnchor().getX(), self.instructionsTitle.getAnchor().getY(), self.instructionsTitle)
                            self.updateFish(fishList)
                            self.updateShark([7,2,'East', 0])
                            # Turn off start button
                            self.start.toggleActivation()
                            # Return the entered fish locations
                            return fishList

                if not self.win.isClosed():
                    p = self.win.getMouse()

        # User quits so close window and return empty list
        self.win.close()
        return []

    def isClicked(self):
        # Wait for user input
        if not self.win.isClosed():
            p = self.win.getMouse()
            while True:
                # Check which button, if any is clicked
                if self.quitButton.isClicked(p): break
                elif self.start.isClicked(p): return 'start'
                elif self.fishButton.isClicked(p): return 'fish'
                elif self.sharkButton.isClicked(p): return 'shark'
                else: return 'none'
            return 'quit'

    def updateFish(self, fishList):
        # Draws the fish at the specified locations
        for i in range(3):
            self.fish1, self.fish2, self.fish3 = self.fish2, self.fish3, self.fish1
            self.fish1.undraw()

            fishx, fishy, fishD, fishf, isAlive = fishList[i*5], fishList[i*5+1], fishList[i*5+2], fishList[i*5+3],  fishList[i*5+4]

            # https://media.giphy.com/media/cRKRjNNmYCqUPK8leA/giphy.gif
            flee = ''
            if fishf: flee = 'Flee'
            image = 'fish' + fishD.capitalize() + flee +'.gif'

            if type(self.fish1) == Point: currentX, currentY = self.fish1.getX(), self.fish1.getY()
            else: currentX, currentY = self.fish1.getAnchor().getX(), self.fish1.getAnchor().getY()
            self.fish1 = Image(Point(currentX, currentY), image)

            if isAlive: self.fish1.draw(self.win)
            else:
                if not isAlive == self.storedFish[i*5+4]:
                    self.ripFishCounter += 1
                    self.instructionsText.setText("Fish " + str(i) + " has been killed!\nWhat a tragedy! Oh No!")
                    self.ripFish.setText("Dead Fish Counter: " + str(self.ripFishCounter))

            self.anim(75 * fishx + 57, fishy * 75 + 57, currentX, currentY,self.fish1)
        self.storedFish = fishList

    def updateShark(self, sharkList):
        self.shark.undraw()
        # https://www.animatedimages.org/cat-sharks-516.htm
        image = 'shark' + sharkList[2] + '.gif'

        if type(self.shark) == Point: currentX, currentY = self.shark.getX(), self.shark.getY()
        else: currentX, currentY = self.shark.getAnchor().getX(), self.shark.getAnchor().getY()
        self.shark = Image(Point(currentX, currentY), image).draw(self.win)

        self.anim(75 * sharkList[0] + 57, sharkList[1] * 75 + 57, currentX, currentY, self.shark)


    def nextTurn(self):
        self.sharkButton.toggleActivation()
        self.fishButton.toggleActivation()
        if self.fishButton.isActive(): self.instructionsText.setText("Click on the fish button to move\nthe fish")
        else: self.instructionsText.setText("Click on the shark button to move\nthe shark")

    def endGame(self):
        self.win.close()

    def winner(self, winner):
        if self.fishButton.isActive(): self.fishButton.toggleActivation()
        if self.sharkButton.isActive(): self.sharkButton.toggleActivation()

        listOfConfetti = []
        for i in range(2):
            for j in range(3):
                listOfConfetti.append(Image(Point(i * 700, j * 500), 'confetti.gif').draw(self.win))

        if winner == 'fish':
            self.instructionsText.setText("The fish have won!\nShark died of starvation!\nPlay Again!")
        elif winner == 'shark':
            self.instructionsText.setText("The shark has won!\nAll the fish were eaten!\nPlay Again!")

        popup = GraphWin("Play Again?", 400, 400)
        popup.setBackground(color_rgb(52, 152, 219))
        for i in range(2):
            for j in range(3):
                Image(Point(i * 700, j * 500), 'confetti.gif').draw(popup)
        playAgain = Text(Point(200,300), "The " + winner + "has won!\nWould you like to play again?\nClick on the start button!").draw(popup)
        playAgain.setTextColor('white')
        playAgain.setSize(25)
        playAgainButton = Button(200,140,200,60,10,'light green', "Play Again", 'white', 20, popup)
        playAgainButton.toggleActivation()
        quitButton = Button(50,30,100,50,5,'red', "Quit", 'white', 20,popup)
        quitButton.toggleActivation()

        for k in listOfConfetti: k.undraw()
        self.win.close()

        p = popup.getMouse()
        while not quitButton.isClicked(p):
            if playAgainButton.isClicked(p):
                self.createWin()
                popup.close()
                fishList = self.gatherUserInput()
                return fishList
            if not popup.isClosed():
                p = popup.getMouse()

        popup.close()
        return []

    # Helper function: should not be called outside of this class
    def formatGUI(self):
        self.enterFish1 = Text(Point(960, 150), "Daddy Coordinate(x,y): ").draw(self.win)
        self.enterFish2 = Text(Point(955, 200), "Mommy Coordinate(x,y): ").draw(self.win)
        self.enterFish3 = Text(Point(955, 250), "Granny Coordinate(x,y): ").draw(self.win)

        self.instructionsText.setSize(20)
        self.instructionsText.setTextColor(color_rgb(236, 240, 241))
        self.instructionsTitle.setSize(23)
        self.instructionsTitle.setStyle('bold')
        self.instructionsTitle.setTextColor('white')

        title = Text(Point(1035, 100), "Shark Game").draw(self.win)
        title.setSize(25)
        title.setTextColor('white')
        title.setStyle('bold')

        self.ripFish.setSize(20)
        self.ripFish.setTextColor("white")

        for i in range(11):
            l = Line(Point(75*i + 25,25), Point(75*i + 25, 775)).draw(self.win)
            l.setWidth(5)
            l.setFill('white')
            l = Line(Point(25, i*75 + 25), Point(775, i*75 + 25)).draw(self.win)
            l.setWidth(5)
            l.setFill('white')

        for i in range(3):
            self.entry1, self.entry2, self.entry3 = self.entry2, self.entry3, self.entry1
            self.entry1.setSize(25)
            self.entry1.setFill(color_rgb(26, 188, 156))
            self.entry1.setStyle('bold')
            self.entry1.setTextColor('white')

        for i in range(3):
            self.enterFish1, self.enterFish2, self.enterFish3 = self.enterFish2, self.enterFish3, self.enterFish1
            self.enterFish1.setSize(20)
            self.enterFish1.setTextColor('white')

    def createWin(self):
        # Create the window
        self.win = GraphWin("Shark Game", 1300, 800, True)
        self.win.setBackground(self.color[0])
        mover, moveg, moveb = 28-26, 117-40, 208-100
        for i in range(102):
            l = Line(Point(0,i*8), Point(1300, i*8))
            l.setFill(color_rgb(int(26+mover*i/102), int(117 - moveg*i/102), int(208 - moveb*i/102)))
            l.setOutline(color_rgb(int(26+mover*i/102), int(117 - moveg*i/102), int(208 - moveb*i/102)))
            l.setWidth(8)
            l.draw(self.win)

        r = Rectangle(Point(800, 60), Point(1275, 780)).draw(self.win)
        r.setFill(color_rgb(41, 128, 185))
        r.setOutline(color_rgb(41, 128, 185))

        # Create the buttons
        self.quitButton = Button(1245, 25, 100, 40, 10, color_rgb(231, 76, 60), 'Quit', 'white', 20, self.win)
        self.start = Button(1035, 325, 200, 50, 10, color_rgb(46, 204, 113), 'Start', 'white', 25, self.win)
        self.sharkButton = Button(1035, 650, 400, 50, 10, color_rgb(142, 68, 173), 'Move Shark', 'white', 25, self.win)
        self.fishButton = Button(1035, 725, 400, 50, 10, color_rgb(243, 156, 18), 'Move Fish', 'white', 25, self.win)

        # Create the fish coord entries
        self.entry1, self.entry2, self.entry3 = Entry(Point(1145, 150), 10).draw(self.win), Entry(Point(1145, 200),10).draw(self.win), Entry(Point(1145, 250), 10).draw(self.win)
        self.instructionsText = Text(Point(1035, 450),"Enter the coordinates of the\nthree fish above.\nMake sure you don't enter the shark\nor any other fish coordinates").draw(self.win)
        self.ripFish = Text(Point(1035, 580), "Dead Fish Counter: 0\n").draw(self.win)
        self.ripFishCounter = 0

        self.instructionsTitle = Text(Point(1500, 180), "Instructions:").draw(self.win)

        self.formatGUI()

        self.fish1, self.fish2, self.fish3, self.shark = Point(0, 0).draw(self.win), Point(0, 0).draw(self.win), Point(0, 0).draw(self.win), Point(0, 0).draw(self.win)
        # Draw the shark on the board
        self.updateShark([7, 2, 'East', 0])
        self.storedFish = []

        # Finally activate quit button
        self.quitButton.toggleActivation()

    def anim(self, futureX, futureY, currentX, currentY, graphics):
        moveX, moveY = futureX - currentX, futureY - currentY
        if moveX != 0.0 or moveY != 0.0:
            for i in range(10):
                graphics.move(moveX / 10, moveY / 10)
                time.sleep(0.001)
