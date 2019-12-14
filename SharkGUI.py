# File: SharkGUI.py
# Date: 11/14/19
# Written By: Christopher Luey
# Manages all GUI events for SharkRunner.py

from Button import *
import time

class SharkGUI:
    """This class uses John Zelle's Graphics library in order to create a GUI to display the fishes and
    sharks theoretical positions and states.

    Attributes:
        self.win: The Graphics window
        self.fishNameList: List of the names of the fishes
        self.start: Start Button
        self.quitButton: Quit Button
        self.entry1, self.entry2, self.entry3: 3 fish Entry boxes where coordinates of fish are entered
        self.instructionsText: The instructions text
        self.fishButton: Fish move Button
        self.storedFish: The list of current fish states and positions
        self.enterFish1, self.enterFish2, self.enterFish3: The title next to the fish Entry boxes
        self.instructionsTitle: The instructions title text
        self.gameLogTitle: The game log title text
        self.gameLog: The game log text
        self.gameLogMove: The game log moves text
        self.gameLogList: The list of stored game log messages
        self.gameLogListMoves: The list of stored game log moves
        self.sharkButton: The shark move Button
        self.fish1, self.fish2, self.fish3: The 3 graphic fishes drawn on the board
        self.moveCounter: The accumulator for the number of moves of a game
        self.ripFishCounter: The number of fish dead
        self.ripFish: The number of fish dead Text
        self.shark: The drawn shark on the board
        self.sharkChasingVal: The current fish that the shark is chasing
        self.txt: The current text that the game log is displaying
        self.moveTxt: The current text that the game log moves is displaying
        self.previousLines: The current number of game log lines
    """

    def __init__(self):
        """Constructor for SharkGUI object. Creates the window and all window attributes."""
        # Create the window
        self.win = GraphWin("Shark Game", 1300, 800, True)
        self.win.setBackground(color_rgb(26, 117, 208))
        gridList = []

        # Change of colors over time in order to create a gradient
        mover, moveg, moveb = 24, 117 - 40, 208 - 100
        for i in range(102):
            l = Line(Point(0, i * 8), Point(1300, i * 8))
            l.setFill(color_rgb(int(26 + mover * i / 102), int(117 - moveg * i / 102), int(208 - moveb * i / 102)))
            l.setOutline(color_rgb(int(26 + mover * i / 102), int(117 - moveg * i / 102), int(208 - moveb * i / 102)))
            l.setWidth(8)
            gridList.append(l)

        l = Polygon(Point(800, 780), Point(820, 790), Point(1290, 790), Point(1290, 80), Point(1275, 60))
        l.setFill(color_rgb(10, 30, 20))
        l.setOutline(color_rgb(10, 30, 20))
        gridList.append(l)
        l = Polygon(Point(800, 780), Point(820, 790), Point(1290, 790), Point(1275, 780))
        l.setFill(color_rgb(10, 20, 10))
        l.setOutline(color_rgb(10, 20, 10))
        gridList.append(l)
        r = Rectangle(Point(820, 70), Point(1290, 790))
        r.setFill(color_rgb(41, 128, 185))
        r.setOutline(color_rgb(41, 128, 185))
        gridList.append(r)

        for i in range(11):
            l = Line(Point(75 * i + 30, 30), Point(75 * i + 30, 780))
            l.setWidth(7)
            l.setFill(color_rgb(10, 30, 20))
            gridList.append(l)
            l = Line(Point(30, i * 75 + 30), Point(780, i * 75 + 30))
            l.setWidth(7)
            l.setFill(color_rgb(10, 30, 20))
            gridList.append(l)
            l = Line(Point(75*i + 25,25), Point(75*i + 25, 775))
            l.setWidth(5)
            l.setFill('white')
            gridList.append(l)
            l = Line(Point(25, i*75 + 25), Point(775, i*75 + 25))
            l.setWidth(5)
            l.setFill('white')
            gridList.append(l)

        for line in gridList: line.draw(self.win)

        self.fishNameList = ["Mr. Ladd", "Mr. Huntoon", "Mr. Fisher"]
        self.createWin()
        self.anim(1037.5, 420.0, 1055.0, 430.0, r, 10)


    def gatherUserInput(self):
        """Function gathers the inputs of the fish Entry and determines whether they are formatted correctly.

        Returns:
            fishList: List of fish positions and states in format [fish1x, fish1y, fish1dir, fish1flee, fish1alive, fish2x ... ]
                      List if blank if inputted points are formatted incorrectly.
        """
        if not self.win.isClosed():
            self.animText("", "Mr. Ladd Coordinate(x,y): ", self.enterFish1)
            self.animText("", "Mr. Huntoon Coordinate(x,y): ", self.enterFish2)
            self.animText("", "Mr. Fisher Coordinate(x,y): ", self.enterFish3)
            self.animText("", "Enter the coordinates of the\nthree fish above.\nMake sure you don't enter the shark\nor any other fish coordinates", self.instructionsText)
            self.updateShark([7,2,'East',0])
            if not self.start.isActive():
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
                            self.anim(1035, 210, self.instructionsText.getAnchor().getX(), self.instructionsText.getAnchor().getY(), self.instructionsText, 10)
                            self.anim(1035, 165, self.instructionsTitle.getAnchor().getX(), self.instructionsTitle.getAnchor().getY(), self.instructionsTitle, 10)
                            self.anim(1035, 275, self.gameLogTitle.getAnchor().getX(), self.gameLogTitle.getAnchor().getY(), self.gameLogTitle, 10)
                            self.anim(1100, 445, self.gameLog.getAnchor().getX(), self.gameLog.getAnchor().getY(), self.gameLog, 10)
                            self.anim(865, 445, self.gameLogMove.getAnchor().getX(), self.gameLogMove.getAnchor().getY(), self.gameLogMove, 10)

                            for i in range(3):
                                self.gameLogList.append(self.fishNameList[i] + " is at: (" + str(fishList[i*5]) + ", " + str(fishList[i*5+1]) + ")\n")
                                self.gameLogListMoves.append("[Move " + str(self.moveCounter) + "]: \n")

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
        """Function determines which button, if any, has been clicked.

        Returns:
            'quit', 'start', 'fish', 'shark', 'none' depending on the button clicked
        """
        # Wait for user input
        if not self.win.isClosed():
            p = self.win.getMouse()
            # Check which button, if any is clicked
            if self.quitButton.isClicked(p): return 'quit'
            elif self.start.isClicked(p): return 'start'
            elif self.fishButton.isClicked(p): return 'fish'
            elif self.sharkButton.isClicked(p): return 'shark'
            else: return 'none'


    def updateFish(self, fishList):
        """
        Draws the fish at the specified locations.

        Args:
            fishList: List of fish states and positions in format [fish1x, fish1y, fish1dir, fish1flee, fish1alive, fish2x ...]
        """
        moveFishCounter = 0

        for i in range(3):
            self.fish1, self.fish2, self.fish3 = self.fish2, self.fish3, self.fish1
            self.fish1.undraw()
            fishx, fishy, fishD, fishf, isAlive = fishList[i*5], fishList[i*5+1], fishList[i*5+2], fishList[i*5+3],  fishList[i*5+4]

            if isAlive:
                # https://media.giphy.com/media/cRKRjNNmYCqUPK8leA/giphy.gif
                flee = ''
                if fishf:
                    flee = 'Flee'
                    if not self.storedFish[i*5+3]:
                        self.gameLogList.append(self.fishNameList[i] + " senses the shark;\n")
                        self.gameLogList.append("he transforms into flee mode!\n")
                        self.gameLogListMoves.append("[Move " + str(self.moveCounter) + "]: \n")
                        self.gameLogListMoves.append("\n")

                else:
                    if self.storedFish[i * 5 + 3]:
                        self.gameLogList.append(self.fishNameList[i] + " has escaped and\n")
                        self.gameLogList.append("returned to normal state.\n")
                        self.gameLogListMoves.append("[Move " + str(self.moveCounter) + "]: \n")
                        self.gameLogListMoves.append("\n")

                image = 'fish' + fishD.capitalize() + flee +'.gif'

                if type(self.fish1) == Point:
                    currentX, currentY = self.fish1.getX(), self.fish1.getY()
                else:
                    currentX, currentY = self.fish1.getAnchor().getX(), self.fish1.getAnchor().getY()

                self.fish1 = Image(Point(currentX, currentY), image)

                self.fish1.draw(self.win)
                if (fishx != self.storedFish[i*5] or fishy != self.storedFish[i*5+1]) or self.moveCounter == 0:
                    self.anim(75 * fishx + 57, fishy * 75 + 57, currentX, currentY,self.fish1, 10)
                    moveFishCounter+=1

            else:
                if not isAlive == self.storedFish[i*5+4]:
                    self.ripFishCounter += 1

                    #https: // pngio.com / PNG / 28823 - wasted - png.html
                    wasted = Image(Point(0, 400), 'wasted.gif').draw(self.win)
                    self.anim(1300, 400, 0, 400, wasted, 50)
                    wasted.undraw()
                    self.ripFish.setText("Dead Fish Counter: " + str(self.ripFishCounter))
                    self.gameLogList.append(self.fishNameList[i] + " was WASTED by\n")
                    self.gameLogList.append("the shark!\n")

                    self.gameLogListMoves.append("[Move " + str(self.moveCounter) + "]: \n")
                    self.gameLogListMoves.append("\n")

        if self.moveCounter != 0 and self.moveCounter%2 == 0 and moveFishCounter != 1:
            self.gameLogList.append(str(moveFishCounter) + " fish have moved.\n")
            self.gameLogListMoves.append("[Move " + str(self.moveCounter) + "]: \n")

        elif moveFishCounter == 1:
            self.gameLogList.append(str(moveFishCounter) + " fish has moved.\n")
            self.gameLogListMoves.append("[Move " + str(self.moveCounter) + "]: \n")

        self.storedFish = fishList
        self.updateGameLog()


    def updateShark(self, sharkList):
        """Function draws the shark on the window according to the theoretical inputted coordinates and state.

        Args:
            sharkList: List of shark theoretical position and state in format [sharkx, sharky, sharkdir, sharkchasing]
        """
        self.shark.undraw()
        # https://www.animatedimages.org/cat-sharks-516.htm
        # retrieve the proper shark image based on shark's direction
        image = 'shark' + sharkList[2] + '.gif'

        # Depending on the shark type, get the x and y position of the shark (point is used at first before fish coordinates are inputted)
        if type(self.shark) == Point: currentX, currentY = self.shark.getX(), self.shark.getY()
        else: currentX, currentY = self.shark.getAnchor().getX(), self.shark.getAnchor().getY()

        # Create the image object (updates the shark's direction facing)
        self.shark = Image(Point(currentX, currentY), image).draw(self.win)

        # Animate the movement of the shark
        self.anim(75 * sharkList[0] + 57, sharkList[1] * 75 + 57, currentX, currentY, self.shark, 10)

        # Tell the GUI which fish is being chased
        # If the shark switches fish, tell the GUI
        if sharkList[3] != 0 and sharkList[3] != self.sharkChasingVal:
            self.gameLogList.append("Dr. Mishkit smells " + self.fishNameList[sharkList[3]-1] + ";\n")
            self.gameLogList.append("he is close by!\n")
            self.gameLogListMoves.append("[Move " + str(self.moveCounter) + "]: \n")
            self.gameLogListMoves.append("\n")

        elif sharkList[3] == self.sharkChasingVal and self.moveCounter != 0:
            self.gameLogList.append("Dr. Mishkit continues to pursue\n")
            self.gameLogList.append(self.fishNameList[sharkList[3]-1] + "\n")
            self.gameLogListMoves.append("[Move " + str(self.moveCounter) + "]: \n")
            self.gameLogListMoves.append("\n")

        self.updateGameLog()
        # Save the fish that the shark is chasing for later use
        self.sharkChasingVal = sharkList[3]


    def nextTurn(self):
        """Function tells GUI that fish and sharks have moved and its time for the next turn."""
        # Swap buttons and instructions
        self.sharkButton.toggleActivation()
        self.fishButton.toggleActivation()
        if self.fishButton.isActive(): self.instructionsText.setText("Click on the fish button to move\nthe fish")
        else: self.instructionsText.setText("Click on the shark button to move\nthe shark")
        self.moveCounter+=1


    def endGame(self):
        """Function tells GUI that game has ended."""
        self.win.close()


    def winner(self, winner):
        """Function initiates win sequence and returns list of new fish coordinates.

        Args:
            winner: The team that has won the game ('fish' or 'shark')

        Returns:
            fishList: List of theoretical fish states and positions. Returns [] if user quits.
        """
        if self.fishButton.isActive(): self.fishButton.toggleActivation()
        if self.sharkButton.isActive(): self.sharkButton.toggleActivation()

        listOfConfetti = []
        for i in range(2):
            for j in range(3):
                listOfConfetti.append(Image(Point(i * 700, j * 500), 'confetti.gif').draw(self.win))

        popup = GraphWin("Play Again?", 400, 400)
        popup.setBackground(color_rgb(52, 152, 219))
        playAgain = Text(Point(200,300), "").draw(popup)

        if winner == 'fish':
            playAgain.setText("The fish have won!\nShark died of starvation!\nPlay Again!")
            self.instructionsText.setText("The fish have won!")
        elif winner == 'shark':
            playAgain.setText("The shark has won!\nAll the fish were eaten!\nPlay Again!")
            self.instructionsText.setText("The shark has won!")

        playAgain.setTextColor('white')
        playAgain.setSize(25)
        playAgainButton = Button(200,140,200,60,10,'light green', "Play Again", 'white', 20, popup)
        playAgainButton.toggleActivation()

        quitButton = Button(60,30,100,50,5,'red', "Quit", 'white', 20,popup)
        quitButton.toggleActivation()

        for k in listOfConfetti: k.undraw()

        p = popup.getMouse()
        while not quitButton.isClicked(p):
            if playAgainButton.isClicked(p):
                popup.close()
                self.resetWin()
                fishList = self.gatherUserInput()
                return fishList
            if not popup.isClosed():
                p = popup.getMouse()

        popup.close()
        self.win.close()
        return []

    """Helper functions. Should not be called outside of this class."""
    def formatGUI(self):
        """Function formats the GUI."""

        self.enterFish1 = Text(Point(955, 150), "")
        self.enterFish2 = Text(Point(950, 200), "")
        self.enterFish3 = Text(Point(950, 250), "")

        self.instructionsText.setSize(20)
        self.instructionsText.setTextColor(color_rgb(236, 240, 241))
        self.instructionsTitle.setSize(23)
        self.instructionsTitle.setStyle('bold')
        self.instructionsTitle.setTextColor('white')
        self.instructionsTitle.draw(self.win)
        self.instructionsText.draw(self.win)
        self.gameLogTitle = Text(Point(1500, 270), "Game Log:").draw(self.win)
        self.gameLogTitle.setSize(23)
        self.gameLogTitle.setStyle('bold')
        self.gameLogTitle.setTextColor('white')

        self.gameLog = Text(Point(1500, 285), "").draw(self.win)
        self.gameLog.setSize(20)
        self.gameLog.setTextColor('white')
        self.gameLogMove = Text(Point(1500, 285), "").draw(self.win)
        self.gameLogMove.setSize(20)
        self.gameLogMove.setTextColor('lightgray')
        self.gameLogMove.setStyle("italic")

        title = Text(Point(1040, 105), "Shark Game")
        title.setSize(25)
        title.setTextColor(color_rgb(10, 30, 20))
        title.setStyle('bold')
        title.draw(self.win)

        title = Text(Point(1035, 100), "Shark Game")
        title.setSize(25)
        title.setTextColor('white')
        title.setStyle('bold')
        title.draw(self.win)

        self.ripFish.setSize(20)
        self.ripFish.setTextColor("white")
        self.ripFish.draw(self.win)

        for i in range(3):
            self.entry1, self.entry2, self.entry3 = self.entry2, self.entry3, self.entry1
            self.entry1.setSize(25)
            self.entry1.setFill(color_rgb(26, 188, 156))
            self.entry1.setStyle('bold')
            self.entry1.setTextColor('white')
            self.entry1.draw(self.win)

        for i in range(3):
            self.enterFish1, self.enterFish2, self.enterFish3 = self.enterFish2, self.enterFish3, self.enterFish1
            self.enterFish1.setSize(20)
            self.enterFish1.setTextColor('white')
            self.enterFish1.draw(self.win)


    def createWin(self):
        """Function creates the GUI."""
        # Create the buttons
        self.quitButton = Button(1245, 25, 100, 40, 10, color_rgb(231, 76, 60), 'Quit', 'white', 20, self.win)
        self.start = Button(1035, 325, 200, 50, 10, color_rgb(46, 204, 113), 'Start', 'white', 25, self.win)
        self.sharkButton = Button(1035, 650, 400, 50, 10, color_rgb(142, 68, 173), 'Move Shark', 'white', 25, self.win)
        self.fishButton = Button(1035, 725, 400, 50, 10, color_rgb(243, 156, 18), 'Move Fish', 'white', 25, self.win)

        # Create the fish coord entries
        self.entry1, self.entry2, self.entry3 = Entry(Point(1160, 150), 10), Entry(Point(1160, 200),10), Entry(Point(1160, 250), 10)
        self.instructionsText = Text(Point(1035, 450),"")
        self.ripFish = Text(Point(1035, 595), "Dead Fish Counter: 0\n")
        self.ripFishCounter = 0

        self.instructionsTitle = Text(Point(1500, 180), "Instructions:")

        self.formatGUI()
        self.gameLogList, self.gameLogListMoves = [], []
        self.moveCounter = 0
        self.sharkChasingVal = 0
        self.txt, self.moveTxt = "", ""
        self.previousLines = 0

        self.fish1, self.fish2, self.fish3, self.shark = Point(0, 0).draw(self.win), Point(0, 0).draw(self.win), Point(0, 0).draw(self.win), Point(0, 0).draw(self.win)
        # Draw the shark on the board
        self.updateShark([7, 2, 'East', 0])
        self.storedFish = []

        # Finally activate quit button
        self.quitButton.toggleActivation()


    def anim(self, futureX, futureY, currentX, currentY, graphics, t):
        """Function animates the movement of graphics objects.

        Args:
            futureX: The x position to move the object
            futureY: The y position to move the object
            currentX: The current x position of the object
            currentY: The current y position of the object
            graphics: The object to be moved
            t: The speed at which the object should be moved
        """
        moveX, moveY = futureX - currentX, futureY - currentY
        if moveX != 0.0 or moveY != 0.0:
            for i in range(t):
                graphics.move(moveX / t, moveY / t)
                time.sleep(0.001)


    def resetWin(self):
        """Function resets the GUI values and graphics."""
        self.gameLogList, self.moveCounter, self.txt, self.previousLines, self.gameLogListMoves, self.moveTxt = [], 0, "", 0, [], ""
        self.instructionsText.undraw()
        self.ripFish.undraw()
        self.fish1.undraw()
        self.fish2.undraw()
        self.fish3.undraw()
        self.instructionsTitle.undraw()
        self.instructionsText.undraw()
        self.quitButton.undraw()
        self.shark.undraw()
        self.gameLog.undraw()
        self.gameLogTitle.undraw()
        self.gameLogMove.undraw()
        self.createWin()


    def updateGameLog(self):
        """Function updates and displays the dynamic gamelog."""
        newLines, shifter = len(self.gameLogList) - self.previousLines, 0
        for j in range(len(self.gameLogList)-newLines, len(self.gameLogList)):
            if len(self.gameLogList) > 11:
                self.txt, shifter, self.moveTxt = "", shifter + 1, ""
                self.gameLogList.pop(0)
                self.gameLogListMoves.pop(0)
                for i in range(10):
                    self.txt+=self.gameLogList[i]
                    self.moveTxt+=self.gameLogListMoves[i]
            self.moveTxt += self.animText(self.moveTxt, self.gameLogListMoves[j-shifter], self.gameLogMove)
            self.txt += self.animText(self.txt, self.gameLogList[j-shifter], self.gameLog)
        self.previousLines = len(self.gameLogList)


    def animText(self, originalText, newText, regularText):
        """Function animates the movement of text.

        Args:
            originalText: The current text of the object
            newText: The to be displayed text of the object
            regularText: The Text graphics object to be animated

        Returns:
            newText: The nexText inputted into the function.
        """
        for i in range(0,len(newText),2):
            if len(newText) - i < 2:
                originalText += newText[i:i+len(newText) % 2]
            else:
                originalText += newText[i:i+2]
            regularText.setText(originalText)
        return newText
