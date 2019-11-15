# File: Shark.py
# Date: 11/14/19
# Written By: Christopher Luey
# Shark class for SharkRunner.py

class Shark:

    def __init__(self):
        self.sharkPosition = [7,2,'w',0]

    def sharkTurn(self, fishList):

        return self.sharkPosition, fishList
