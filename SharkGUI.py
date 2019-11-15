# File: SharkGUI.py
# Date: 11/14/19
# Written By: Christopher Luey
# Manages all GUI events for SharkRunner.py

from Button import *

class SharkGUI:
    def __init__(self):
        self.x, self.y = 1300, 800
        self.win = GraphWin("Shark Game", self.x, self.y)

        r = Rectangle(Point(800, 60), Point(1275, 780)).draw(self.win)
        r.setFill(color_rgb(41, 128, 185))
        r.setOutline(color_rgb(41, 128, 185))

        self.win.setBackground(color_rgb(52, 152, 219))
        for i in range(11):
            l = Line(Point(75*i + 25,25), Point(75*i + 25, 775)).draw(self.win)
            l.setWidth(5)
            l.setFill('white')
            l = Line(Point(25, i*75 + 25), Point(775, i*75 + 25)).draw(self.win)
            l.setWidth(5)
            l.setFill('white')

        self.quitButton = Button(1245, 25, 100, 40, 10, color_rgb(231, 76, 60), 'Quit', 'white', 20, self.win)
        self.quitButton.toggleActivation()

        self.start = Button(1035, 325, 200, 50, 10, color_rgb(46, 204, 113), 'Start', 'white', 25, self.win)

        self.sharkButton = Button(1035, 650, 400, 50, 10, color_rgb(142, 68, 173), 'Move Shark', 'white', 25, self.win)

        self.fishButton = Button(1035, 725, 400, 50, 10, color_rgb(243, 156, 18), 'Move Fish', 'white', 25, self.win)

        self.fish1 = Point(0,0).draw(self.win)
        self.fish2 = Point(0,0).draw(self.win)
        self.fish3 = Point(0,0).draw(self.win)
        self.shark = Point(0,0).draw(self.win)

        enterFish1, enterFish2, enterFish3 = Text(Point(960, 150), "Alpha Coordinate(x,y): ").draw(self.win), Text(Point(960, 200), "Beta Coordinate(x,y): ").draw(self.win), Text(Point(960, 250), "Gamma Coordinate(x,y): ").draw(self.win)
        enterFish1.setSize(20)
        enterFish1.setTextColor('white')
        enterFish2.setSize(20)
        enterFish2.setTextColor('white')
        enterFish3.setSize(20)
        enterFish3.setTextColor('white')

        self.entry1 = Entry(Point(1145, 150), 10).draw(self.win)
        self.entry2 = Entry(Point(1145, 200), 10).draw(self.win)
        self.entry3 = Entry(Point(1145, 250), 10).draw(self.win)

        title = Text(Point(1035, 100), "Shark Game").draw(self.win)
        title.setSize(25)
        title.setTextColor('white')
        title.setStyle('bold')

        self.instructionsText = Text(Point(1035, 480), "Instructions: Enter the coordinates\nof the three fish above.").draw(self.win)
        self.formatGUI()

    def createWindow(self):
        self.start.toggleActivation()
        p = self.win.getMouse()
        while not self.quitButton.isClicked(p):
            if self.start.isClicked(p):
                fishList, entry1, entry2, entry3 = [], self.entry1.getText(), self.entry2.getText(), self.entry3.getText()

                for i in range(3):
                    entry1, entry2, entry3, self.entry1, self.entry2, self.entry3 = entry2, entry3, entry1, self.entry2, self.entry3, self.entry1
                    if len(entry1) == 3 and entry1[1] == "," and 48<=ord(entry1[0])<=57 and 48<=ord(entry1[2])<=57:
                        fishList.extend([int(entry1[0]), int(entry1[2]), 'e', False])
                        self.entry1.setFill(color_rgb(26, 188, 156))
                    else:
                        self.entry1.setFill(color_rgb(192, 57, 43))
                        self.instructionsText.setText("Instruction: Your inputted points are invalid.\nPlease try again.")

                if len(fishList) == 12:
                    self.sharkButton.toggleActivation()
                    self.update(fishList, [7,2,'e'])
                    self.start.toggleActivation()
                    # When user inputs 3 things, then it exits the function and returns the initial fish
                    return fishList

            if not self.win.isClosed():
                p = self.win.getMouse()


    def isClicked(self, button):
        p = self.win.getMouse()
        if button == 'fish': return self.fish.isClicked(p)
        elif button == 'shark': return self.shark.isClicked(p)
        elif button == 'quit': return self.quitButton.isClicked(p)
        elif button == 'start': return self.start.isClicked(p)

    def update(self, fishList, sharkList):
        # Moves the fish and sharks to the specified locations
        self.sharkButton.toggleActivation()
        self.fishButton.toggleActivation()

        for i in range(3):
            self.fish1, self.fish2, self.fish3 = self.fish2, self.fish3, self.fish1
            self.fish1.undraw()

            fishx, fishy, fishD, fishf = fishList[i*4], fishList[i*4+1], fishList[i*4+2], fishList[i*4+3]

            # https://giphy.com/kittusz
            # https://media.giphy.com/media/cRKRjNNmYCqUPK8leA/giphy.gif
            if fishf: flee = 'Flee'
            else: flee = ''

            image = 'fishWest' + flee +'.gif'
            if fishD == 'n': image = 'fishNorth'+flee+'.gif'
            elif fishD == 'e': image = 'fishEast'+flee+'.gif'
            elif fishD == 's': image = 'fishSouth'+flee+'.gif'

            self.fish1 = Image(Point(75 * fishx + 57, fishy*75 + 57), image).draw(self.win)

        # https://www.animatedimages.org/cat-sharks-516.htm
        self.shark.undraw()
        image = 'sharkEast.gif'
        if sharkList[2] == 'n': image = 'sharkNorth.gif'
        elif sharkList[2] == 'e': image = 'sharkEast.gif'
        elif sharkList[2] == 's': image = 'sharkSouth.gif'
        elif sharkList[2] == 'w': image = 'sharkWest.gif'
        elif sharkList[2] == 'ne': image = 'sharkNorthEast.gif'
        elif sharkList[2] == 'se': image = 'sharkSouthEast.gif'
        elif sharkList[2] == 'sw': image = 'sharkSouthWest.gif'
        elif sharkList[2] == 'nw': image = 'sharkNorthWest.gif'

        self.shark = Image((Point(75 * sharkList[0] + 57, sharkList[1]*75 + 57)), image).draw(self.win)

    def endgame(self):
        self.win.close()

    def win(self, winner):
        if self.fishButton.isActive(): self.fishButton.toggleActivation()
        if self.sharkButton.isActive(): self.sharkButton.toggleActivation()
        if winner == 'fish': self.instructionsText.setText("The fish have won!\nShark died of starvation!\nPlay Again!")
        elif winner == 'shark': self.instructionsText.setText("The shark has won!\nAll the fish were eaten!\nPlay Again!")

    def formatGUI(self):
        self.entry1.setSize(25)
        self.entry2.setSize(25)
        self.entry3.setSize(25)
        self.entry1.setFill(color_rgb(26, 188, 156))
        self.entry2.setFill(color_rgb(26, 188, 156))
        self.entry3.setFill(color_rgb(26, 188, 156))
        self.entry1.setStyle('bold')
        self.entry2.setStyle('bold')
        self.entry3.setStyle('bold')
        self.entry1.setTextColor('white')
        self.entry2.setTextColor('white')
        self.entry3.setTextColor('white')
        self.instructionsText.setSize(23)
        self.instructionsText.setTextColor('white')


def main():
    gui = SharkGUI()
    fish = gui.createWindow()

    while not gui.isClicked('quit'):
        if gui.isClicked('fish'):
            # Move fish
            gui.update()
        if gui.isClicked('shark'):
            # Move shark
            gui.update()

    gui.endgame()

main()