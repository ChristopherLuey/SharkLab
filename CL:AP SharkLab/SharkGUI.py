# File: SharkGUI.py
# Date: 11/14/19
# Written By: Christopher Luey
# Manages all GUI events for SharkRunner.py

from Button import *

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
        mover, moveg, moveb = 90, 117, 8
        for i in range(102):
            l = Line(Point(0, i * 8), Point(1300, i * 8))
            l.setFill(color_rgb(int(9 + mover * i / 102), int(130 - moveg * i / 102), int(230 - moveb * i / 102)))
            l.setOutline(color_rgb(int(9 + mover * i / 102), int(130 - moveg * i / 102), int(230 - moveb * i / 102)))
            l.setWidth(10)
            gridList.append(l)

        # Shadow for Box
        p = Polygon(Point(800, 780), Point(820, 790), Point(1290, 790), Point(1290, 80), Point(1275, 60))
        p.setFill(color_rgb(10, 30, 20))
        p.setOutline(color_rgb(10, 30, 20))
        gridList.append(p)
        p2 = Polygon(Point(800, 780), Point(820, 790), Point(1290, 790), Point(1275, 780))
        p2.setFill(color_rgb(10, 20, 10))
        p2.setOutline(color_rgb(10, 20, 10))
        gridList.append(p2)

        # Box
        # r = Rectangle(Point(820, 70), Point(1290, 790))
        # r.setFill(color_rgb(41, 128, 185))
        # r.setOutline(color_rgb(41, 128, 185))
        # gridList.append(r)
        mover, moveg, moveb = 40, 90, 9
        for i in range(143):
            l = Line(Point(800, i * 5 + 65), Point(1275, i * 5 + 65))
            l.setFill(color_rgb(int(9 + mover * i / 143), int(90 + moveg * i / 143), int(255 - moveb * i / 143)))
            l.setOutline(color_rgb(int(9 + mover * i / 143), int(90 + moveg * i / 143), int(255 - moveb * i / 143)))
            l.setWidth(10)
            gridList.append(l)

        # Draw the grid shadow and grid
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

        # Draw all the attributes at once
        for line in gridList: line.draw(self.win)

        self.fishNameList = ["Fortnite", "Minecraft", "Roblox"]
        self.createWin()


    def gatherUserInput(self):
        """Function gathers the inputs of the fish Entry and determines whether they are formatted correctly.

        Returns:
            fishList: List of fish positions and states in format [fish1x, fish1y, fish1dir, fish1flee, fish1alive, fish2x ... ]
                      List if blank if user quits.
        """
        if not self.win.isClosed():
            self.animText("", "Fortnite Coordinate(x,y): ", self.enterFish1)
            self.animText("", "Minecraft Coordinate(x,y): ", self.enterFish2)
            self.animText("", "Roblox Coordinate(x,y): ", self.enterFish3)
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
                    originalText = ""
                    for i in ["Input 1: ", "Input 2: ", "Input 3: "]:
                        # Check if it is properly formatted with m,n
                        # This means entry must be 3 chars long, must include a comma at the second char, and the first and third chars must be from 0-9
                        if len(entry1) == 3 and entry1[1] == "," and 48<=ord(entry1[0])<=57 and 48<=ord(entry1[2])<=57 and (int(entry1[0]) != 7 or int(entry1[2]) != 2):
                            # Add this to the fish attributes list which will be passed into updateFish()
                            fishList.extend([int(entry1[0]), int(entry1[2]), 'east', False, True])
                            self.entry1.setFill(color_rgb(26, 188, 156))
                        else:
                            self.entry1.setFill(color_rgb(192, 57, 43))
                            # Check the error type
                            if len(entry1) == 0:
                                originalText+= i+"Your point is blank.\n"
                            elif len(entry1) != 3:
                                originalText+= i+"Your point is not 3 characters long.\n"
                            else:
                                if len(entry1) >= 2 and entry1[1] != ",":
                                    originalText+= i+"Your point is not separated\nby a comma at the second character.\n"
                                else:
                                    if len(entry1) >= 1 and not(48<=ord(entry1[0])<=57):
                                        originalText+= i+"Your x-coordinate is not between 0-9.\n"
                                    if len(entry1) >= 3 and not(48<=ord(entry1[2])<=57):
                                        originalText+= i+"Your y-coordinate is not between 0-9.\n"
                                    if len(entry1) >= 3 and (48<=ord(entry1[0])<=57) and (48<=ord(entry1[2])<=57) and int(entry1[0]) == 7 and int(entry1[2]) == 2:
                                        originalText+= i+"Your point overlaps with the shark.\n"

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
                            if (f1x == f2x and f1y == f2y) and not(f1x == f2x == f3x and f1y == f2y == f3y):
                                self.entry1.setFill(color_rgb(192, 57, 43))
                                self.entry2.setFill(color_rgb(192, 57, 43))
                                originalText+= ["Input 1: ", "Input 2: ", "Input 3: ", "Input 1: "][i]+"Your inputted point overlaps with other fish\n"
                                originalText+= ["Input 1: ", "Input 2: ", "Input 3: ", "Input 1: "][i+1]+"Your inputteda point overlaps with other fish\n"
                                invalid = True

                            elif f1x == f2x == f3x and f1y == f2y == f3y:
                                self.entry1.setFill(color_rgb(192, 57, 43))
                                originalText+= ["Input 1: ", "Input 2: ", "Input 3: "][i]+"Your inputted fish point overlaps with other fish\n"
                                invalid = True

                            # Swap values so everything is checked
                            f1x, f2x, f3x = f2x, f3x, f1x
                            f1y, f2y, f3y = f2y, f3y, f1y
                            self.entry1, self.entry2, self.entry3 = self.entry2, self.entry3, self.entry1

                        if not invalid:
                            self.storedFish = fishList
                            self.startGame()
                            for i in range(3):
                                self.gameLogList.append(self.fishNameList[i] + " is at: (" + str(fishList[i * 5]) + ", " + str(fishList[i * 5 + 1]) + ")\n")
                                self.gameLogListMoves.append("[Move " + str(self.moveCounter) + "]: \n")

                            # Return the entered fish locations
                            return fishList

                    self.animText("", originalText[0:len(originalText)-1], self.instructionsText)

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

        try:
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
                            self.gameLogList.append(self.fishNameList[i] + " senses mom nearby;\n")
                            self.gameLogList.append("it transforms into flee mode!\n")
                            self.gameLogListMoves.append("[Move " + str(self.moveCounter) + "]: \n")
                            self.gameLogListMoves.append("\n")

                    else:
                        if self.storedFish[i * 5 + 3]:
                            self.gameLogList.append(self.fishNameList[i] + " has escaped mom and\n")
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

        except:
            self.gameLogList.append("Error moving fish. Image not found.\n")
            self.gameLogListMoves.append("[Move " + str(self.moveCounter) + "]: \n")

        self.updateGameLog()


    def updateShark(self, sharkList):
        """Function draws the shark on the window according to the theoretical inputted coordinates and state.

        Args:
            sharkList: List of shark theoretical position and state in format [sharkx, sharky, sharkdir, sharkchasing]
        """
        try:
            self.shark.undraw()
            # https://www.animatedimages.org/cat-sharks-516.htm
            # retrieve the proper shark image based on shark's direction
            image = 'shark' + sharkList[2] + '.gif'

            # Depending on the shark type, get the x and y position of the shark (point is used at first before fish coordinates are inputted)
            if type(self.shark) == Point: currentX, currentY = self.shark.getX(), self.shark.getY()
            else: currentX, currentY = self.shark.getAnchor().getX(), self.shark.getAnchor().getY()

            # Create the image object (updates the shark's direction facing)
            self.shark = Image(Point(currentX, currentY), image).draw(self.win)

            self.anim(75 * sharkList[0] + 57, sharkList[1] * 75 + 57, currentX, currentY, self.shark, 10)

            # Tell the GUI which fish is being chased
            # If the shark switches fish, tell the GUI
            if sharkList[3] != 0 and sharkList[3] != self.sharkChasingVal:
                self.gameLogList.append("Mom smells " + self.fishNameList[sharkList[3]-1] + ";\n")
                self.gameLogList.append("it is close by!\n")
                self.gameLogListMoves.append("[Move " + str(self.moveCounter) + "]: \n")
                self.gameLogListMoves.append("\n")

            elif sharkList[3] == self.sharkChasingVal and self.moveCounter != 0:
                self.gameLogList.append("Mom continues to pursue\n")
                self.gameLogList.append(self.fishNameList[sharkList[3]-1] + "\n")
                self.gameLogListMoves.append("[Move " + str(self.moveCounter) + "]: \n")
                self.gameLogListMoves.append("\n")

            # Save the fish that the shark is chasing for later use
            self.sharkChasingVal = sharkList[3]

        except:
            self.gameLogList.append("Error. Shark Image not found\n")
            self.gameLogListMoves.append("[Move " + str(self.moveCounter) + "]: \n")
        self.updateGameLog()


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
        self.quitButton.toggleActivation()

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
        drawList = []
        self.enterFish1 = Text(Point(955, 150), "")
        self.enterFish2 = Text(Point(950, 200), "")
        self.enterFish3 = Text(Point(950, 250), "")

        self.instructionsTitle.setSize(23)
        self.instructionsTitle.setStyle('bold')
        self.instructionsTitle.setTextColor('white')
        drawList.append(self.instructionsTitle)

        self.instructionsText.setSize(19)
        self.instructionsText.setTextColor(color_rgb(236, 240, 241))
        drawList.append(self.instructionsText)

        self.gameLogTitle = Text(Point(1500, 270), "Game Log:")
        self.gameLogTitle.setSize(23)
        self.gameLogTitle.setStyle('bold')
        self.gameLogTitle.setTextColor('white')
        drawList.append(self.gameLogTitle)

        self.gameLog = Text(Point(1500, 285), "")
        self.gameLog.setSize(20)
        self.gameLog.setTextColor('white')
        drawList.append(self.gameLog)

        self.gameLogMove = Text(Point(1500, 285), "")
        self.gameLogMove.setSize(20)
        self.gameLogMove.setTextColor('lightgray')
        self.gameLogMove.setStyle("italic")
        drawList.append(self.gameLogMove)

        title = Text(Point(1040, 105), "Shark Game")
        title.setSize(25)
        title.setTextColor(color_rgb(10, 30, 20))
        title.setStyle('bold')
        drawList.append(title)

        title = Text(Point(1035, 100), "Shark Game")
        title.setSize(25)
        title.setTextColor('white')
        title.setStyle('bold')
        drawList.append(title)

        self.ripFish.setSize(20)
        self.ripFish.setTextColor("white")
        drawList.append(self.ripFish)

        for i in range(3):
            self.entry1, self.entry2, self.entry3 = self.entry2, self.entry3, self.entry1
            self.entry1.setSize(25)
            self.entry1.setFill(color_rgb(26, 188, 156))
            self.entry1.setStyle('bold')
            self.entry1.setTextColor('white')
            drawList.append(self.entry1)

        for i in range(3):
            self.enterFish1, self.enterFish2, self.enterFish3 = self.enterFish2, self.enterFish3, self.enterFish1
            self.enterFish1.setSize(20)
            self.enterFish1.setTextColor('white')
            drawList.append(self.enterFish1)

        for gui in drawList: gui.draw(self.win)


    def createWin(self):
        """Function creates the GUI."""
        # Create the buttons
        self.quitButton = Button(1245, 25, 100, 40, 10, color_rgb(231, 76, 60), 'Quit', 'white', 20, self.win)
        self.start = Button(1035, 325, 200, 50, 10, color_rgb(46, 204, 113), 'Start', 'white', 25, self.win)
        self.sharkButton = Button(1035, 650, 400, 50, 10, color_rgb(142, 68, 173), 'Move Shark', 'white', 25, self.win)
        self.fishButton = Button(1035, 725, 400, 50, 10, color_rgb(243, 156, 18), 'Move Fish', 'white', 25, self.win)

        # Create the fish coord entries
        self.entry1, self.entry2, self.entry3 = Entry(Point(1160, 150), 10), Entry(Point(1160, 200),10), Entry(Point(1160, 250), 10)
        self.instructionsText = Text(Point(1035, 460),"")
        self.ripFish, self.ripFishCounter = Text(Point(1035, 595), "Dead Fish Counter: 0\n"), 0

        self.instructionsTitle = Text(Point(1500, 180), "Instructions:")

        self.formatGUI()
        self.gameLogList, self.gameLogListMoves = [], []
        self.moveCounter, self.sharkChasingVal = 0, 0
        self.txt, self.moveTxt, self.previousLines = "", "", 0

        self.storedFish = []
        self.fish1, self.fish2, self.fish3, self.shark = Point(0, 0).draw(self.win), Point(0, 0).draw(self.win), Point(0, 0).draw(self.win), Point(0, 0).draw(self.win)
        self.updateShark([7, 2, 'East', 0])

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
        # newLines: number number of lines - number of previous lines
        # shifter: amount of lines over 11

        # Iterate through the new lines added to the log list
        # If the length of the log list is more than 11, remove the first index values,
        # reassign txt to all but the removed log list value
        # animate the movement of the new text added
        newLines, shifter = len(self.gameLogList) - self.previousLines, 0
        for j in range(self.previousLines, len(self.gameLogList)):
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
        # Iterate through the text
        # Add portions of the text to the originalText
        # Display originalText to GUI
        for i in range(0,len(newText),2):
            if len(newText) - i < 2:
                originalText += newText[i:i+len(newText) % 2]
            else:
                originalText += newText[i:i+2]
            regularText.setText(originalText)
        return newText


    def startGame(self):
        """Function initiates starting sequence of events."""
        # Display fish and shark on the board
        self.fishButton.toggleActivation()
        self.entry1.undraw()
        self.entry2.undraw()
        self.entry3.undraw()
        self.enterFish1.undraw()
        self.enterFish2.undraw()
        self.enterFish3.undraw()
        self.start.undraw()
        self.instructionsText.setText("Click on the fish button to move\nthe fish")
        self.anim(1035, 210, self.instructionsText.getAnchor().getX(), self.instructionsText.getAnchor().getY(),self.instructionsText, 10)
        self.anim(1035, 165, self.instructionsTitle.getAnchor().getX(), self.instructionsTitle.getAnchor().getY(),self.instructionsTitle, 10)
        self.anim(1035, 275, self.gameLogTitle.getAnchor().getX(), self.gameLogTitle.getAnchor().getY(),self.gameLogTitle, 10)
        self.anim(1100, 445, self.gameLog.getAnchor().getX(), self.gameLog.getAnchor().getY(), self.gameLog, 10)
        self.anim(865, 445, self.gameLogMove.getAnchor().getX(), self.gameLogMove.getAnchor().getY(), self.gameLogMove, 10)
        # Turn off start button
        self.start.toggleActivation()
