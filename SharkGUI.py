# File: SharkGUI.py
# Date: 11/14/19
# Written By: Christopher Luey
# Manages all GUI events for SharkRunner.py

from Button import *

class SharkGUI:
    def __init__(self):
        self.x = 1300
        self.y = 800
        self.win = GraphWin("Shark Game", self.x, self.y)
        for i in range(11):
            Line(Point(75*i + 25,25), Point(75*i + 25, 775)).draw(self.win)
            Line(Point(25, i*75 + 25), Point(775, i*75 + 25)).draw(self.win)

        self.quitButton = Button(1245, 25, 100, 40, 10, 'red', 'Quit', 'white', 20, self.win)
        self.quitButton.toggleActivation()

        self.start = Button(1025, 325, 200, 50, 10, 'light green', 'Start', 'white', 25, self.win)
        self.start.toggleActivation()

        self.shark = Button(1025, 650, 400, 50, 10, 'light green', 'Move Shark', 'white', 25, self.win)
        self.shark.toggleActivation()

        self.fish = Button(1025, 725, 400, 50, 10, 'light green', 'Move Fish', 'white', 25, self.win)
        self.fish.toggleActivation()

        self.entry1 = Entry(Point(1025, 150), 10).draw(self.win)
        self.entry2 = Entry(Point(1025, 200), 10).draw(self.win)
        self.entry3 = Entry(Point(1025, 250), 10).draw(self.win)
        self.entry1.setSize(25)
        self.entry2.setSize(25)
        self.entry3.setSize(25)


    def createWindow(self):

        # When user inputs 3 things, then it exits the function and returns the initial fish
        listOfFish = [0,0,'n',False, 0,0,'n',False, 0,0,'n',False]

        return listOfFish

    def isClicked(self, button):
        p = self.win.getMouse()
        if button == 'fish':
            print()
        elif button == 'shark':
            print()
        elif button == 'quit':
            return self.quitButton.isClicked(p)
        elif button == 'start':
            print()
    def update(self, listOfFish, listOfShark):
        print()
        # Moves the fish and sharks to the specified locations

    def endgame(self):
        print()
        self.win.close()

    def win(self, winner):
        if winner == 'fish':
            print()
        elif winner == 'shark':
            print()

def main():
    gui = SharkGUI()
    while not gui.isClicked('quit'):
        fish = gui.createWindow()

    gui.endgame()

main()