# File: Button.py
# Written By: Christopher Luey
# Date: 9/24/19
# This is a class that creates a Button using Zelle's Graphics Library

from graphics import *

class Button:
    """
    This is a class that creates a Button using Zelle's Graphics Library.

    Attributes:
        x (int, float): The x coordinate to place Button.
        y (int, float): The y coordinate to place Button.
        width (int, float): The width of the Button.
        height (int, float): The height of the Button.
        radius (int, float): The radius of the Button border.
        color (str): Color of the Button.
        text (str): Label of the Button.
        textColor (str): Color of the Label of the Button.
        textSize (int): The Size of the Label of the Button.
        win (graphics.GraphWin): The window to draw the Button on.
        timesClicked (int): The number of times a Button has been clicked.
    """

    def __init__(self, x, y, width, height, radius, color, text, textColor, textSize, win):
        """
        The constructor for Button class.

        Parameters:
            x (float): The x coordinate to place Button.
            y (float): The y coordinate to place Button.
            width (float): The width of the Button.
            height (float): The height of the Button.
            radius (float): The radius of the Button border.
            color (str): Color of the Button.
            text (str): Label of the Button.
            textColor (str): Color of the Label of the Button.
            textSize (int): The Size of the Label of the Button.
            win (graphics.GraphWin): The window to draw the Button on.
        """
        self.textSize = textSize
        self.text = text
        self.textColor = textColor
        self.width = width
        self.height = height
        self.radius = radius
        self.centerX = x
        self.centerY = y
        self.color = 'dim gray'
        self.deactiveColor = color
        self.active = False
        self.radiusInd = False
        self.timesClicked = 0

        # Check if diameter of the curved edge is bigger than the width or height
        if self.radius * 2 <= self.height and self.radius * 2 <= self.width:
            self.radiusInd = True

        # Draw itself on the window
        self.draw(win)

    def draw(self, win):
        """
        Function draws the button on the referenced window.

        Parameters:
            win (GraphWin): The window to draw the Button on.
        """
        if self.radiusInd:
            self.p1 = Point((self.centerX - self.width / 2 - 3) + self.radius,
                            (self.centerY - self.height / 2 + 5) + self.radius)
            self.p3 = Point((self.centerX + self.width / 2 - 3) - self.radius,
                            (self.centerY + self.height / 2 + 5) - self.radius)
            self.p2 = Point((self.centerX - self.width / 2 - 3) + self.radius,
                            (self.centerY + self.height / 2 + 5) - self.radius)
            self.p4 = Point((self.centerX + self.width / 2 - 3) - self.radius,
                            (self.centerY - self.height / 2 + 5) + self.radius)

            self.shadowCircle1, self.shadowCircle2, self.shadowCircle3, self.shadowCircle4 = Circle(self.p1, self.radius), Circle(self.p2, self.radius), Circle(self.p3, self.radius), Circle(self.p4, self.radius)
            self.shadowCircle1.setOutline(color_rgb(10, 30, 20))
            self.shadowCircle2.setOutline(color_rgb(10, 30, 20))
            self.shadowCircle3.setOutline(color_rgb(10, 30, 20))
            self.shadowCircle4.setOutline(color_rgb(10, 30, 20))
            self.shadowCircle1.setFill(color_rgb(10, 30, 20))
            self.shadowCircle2.setFill(color_rgb(10, 30, 20))
            self.shadowCircle3.setFill(color_rgb(10, 30, 20))
            self.shadowCircle4.setFill(color_rgb(10, 30, 20))
            self.shadowCircle1.draw(win)
            self.shadowCircle2.draw(win)
            self.shadowCircle3.draw(win)
            self.shadowCircle4.draw(win)

            # Define points that form the polygon around the circles
            pa = Point(self.p1.getX(), self.p1.getY() - self.radius)
            pb = Point(self.p4.getX(), self.p4.getY() - self.radius)
            pc = Point(self.p4.getX() + self.radius, self.p4.getY())
            pd = Point(self.p3.getX() + self.radius, self.p3.getY())
            pe = Point(self.p3.getX(), self.p3.getY() + self.radius)
            pf = Point(self.p2.getX(), self.p2.getY() + self.radius)
            pg = Point(self.p2.getX() - self.radius, self.p2.getY())
            ph = Point(self.p1.getX() - self.radius, self.p1.getY())

            self.polyShadow = Polygon(pa, pb, pc, pd, pe, pf, pg, ph)
            self.polyShadow.setOutline(color_rgb(10, 30, 20))
            self.polyShadow.setFill(color_rgb(10, 30, 20))
            self.polyShadow.draw(win)


            # Create circles in 4 corners of Button
            self.p1 = Point((self.centerX - self.width / 2) + self.radius, (self.centerY - self.height / 2) + self.radius)
            self.p3 = Point((self.centerX + self.width / 2) - self.radius, (self.centerY + self.height / 2) - self.radius)
            self.p2 = Point((self.centerX - self.width / 2) + self.radius, (self.centerY + self.height / 2) - self.radius)
            self.p4 = Point((self.centerX + self.width / 2) - self.radius, (self.centerY - self.height / 2) + self.radius)

            self.circle1, self.circle2, self.circle3, self.circle4 = Circle(self.p1, self.radius), Circle(self.p2, self.radius), Circle(self.p3, self.radius), Circle(self.p4, self.radius)
            self.circle1.setOutline(self.color)
            self.circle2.setOutline(self.color)
            self.circle3.setOutline(self.color)
            self.circle4.setOutline(self.color)
            self.circle1.setFill(self.color)
            self.circle2.setFill(self.color)
            self.circle3.setFill(self.color)
            self.circle4.setFill(self.color)
            self.circle1.draw(win)
            self.circle2.draw(win)
            self.circle3.draw(win)
            self.circle4.draw(win)

            # Define points that form the polygon around the circles
            pa = Point(self.p1.getX(), self.p1.getY() - self.radius)
            pb = Point(self.p4.getX(), self.p4.getY() - self.radius)
            pc = Point(self.p4.getX() + self.radius, self.p4.getY())
            pd = Point(self.p3.getX() + self.radius, self.p3.getY())
            pe = Point(self.p3.getX(), self.p3.getY() + self.radius)
            pf = Point(self.p2.getX(), self.p2.getY() + self.radius)
            pg = Point(self.p2.getX() - self.radius, self.p2.getY())
            ph = Point(self.p1.getX() - self.radius, self.p1.getY())

            self.poly = Polygon(pa, pb, pc, pd, pe, pf, pg, ph)
            self.poly.setOutline(self.color)
            self.poly.setFill(self.color)
            self.poly.draw(win)

        else:
            # The Button will be a rectangle
            self.p1 = Point((self.centerX - self.width / 2), (self.centerY - self.height / 2))
            self.p3 = Point((self.centerX + self.width / 2), (self.centerY + self.height / 2))
            self.p2 = Point((self.centerX - self.width / 2), (self.centerY + self.height / 2))
            self.p4 = Point((self.centerX + self.width / 2), (self.centerY - self.height / 2))

            self.poly = Rectangle(self.p1, self.p3).draw(win)
            self.poly.setOutline(self.color)
            self.poly.setFill(self.color)

        # Create the Button text
        # self.shadow = Text(Point(self.centerX+2, self.centerY + 2), self.text).draw(win)
        # self.shadow.setOutline(color_rgb(10, 30, 20))
        # self.shadow.setFill(color_rgb(10, 30, 20))
        # self.shadow.setSize(self.textSize)

        self.textBox = Text(Point(self.centerX, self.centerY), self.text).draw(win)
        self.textBox.setFill(self.textColor)
        self.textBox.setOutline(self.textColor)
        self.textBox.setSize(self.textSize)

        self.win = win
        return self

    def undraw(self):
        """
        Function removes the button on the window it is currently placed on.
        """

        self.poly.undraw()
        self.polyShadow.undraw()
        self.textBox.undraw()
        #self.shadow.undraw()
        if self.radiusInd:
            # If there are circles that form the Button:
            self.circle1.undraw()
            self.circle2.undraw()
            self.circle3.undraw()
            self.circle4.undraw()
            self.shadowCircle1.undraw()
            self.shadowCircle2.undraw()
            self.shadowCircle3.undraw()
            self.shadowCircle4.undraw()

    def toggleActivation(self):
        """
        Function toggles the Button activation and changes its color correspondingly.
        """

        # Switch the activation colors and reverse activation variable
        temp = self.color
        self.setColor(self.deactiveColor)
        self.color = self.deactiveColor
        self.deactiveColor = temp
        self.active = not self.active

    def isActive(self):
        """
        Function checks the Button activation state changes its color correspondingly.

        Returns:
            active (bool): True or False depending on the active state of Button.
        """

        return self.active

    def isClicked(self, p):
        """
        Function checks if the Button is clicked.

        Parameters:
            p (Point): Point where the mouse is clicked.

        Returns:
             True (bool): If the Button is clicked on.
             False (bool): If the Button is not clicked on.
        """

        # Check if Button is active
        if self.isActive():
            x = p.getX()
            y = p.getY()
            # Check if the point is within the Button
            if self.p3.getX() + self.radius >= x >= self.p1.getX() - self.radius and self.p1.getY() - self.radius <= y <= self.p2.getY() + self.radius:
                self.timesClicked = self.timesClicked + 1
                self.setColor('white')
                self.setColor(self.color)
                return True
            return False
        return False

    def getTextSize(self):
        """
        Function accesses text size of the Button.

        Returns:
            textSize (int): The text size of the label of the Button.
        """
        return self.textSize

    def getWidth(self):
        """
        Function accesses width of the Button.

        Returns:
            width (int, float): The width of the Button.
        """
        return self.width

    def getHeight(self):
        """
        Function accessess height of the Button.

        Returns:
             height (int, float): The height of the Button.
        """
        return self.height

    def getRadius(self):
        """
        Function accessess radius of the Button.

        Returns:
             radius (int, float): The radius of the Button border.
        """
        return self.radius

    def getCenter(self):
        """
        Function accessess center of the Button.

        Returns:
             center (Point): The center of the Button.
        """
        return Point(self.centerX, self.centerY)

    def getColor(self):
        """
        Function accessess color of the Button.

        Returns:
             color (str): The color of the Button.
        """
        return self.color

    def getText(self):
        """
        Function accessess text of the Button.

        Returns:
             text (str): The text of the Button.
        """
        return self.text

    def getTextColor(self):
        """
        Function accessess text color of the Button.

        Returns:
             textColor (str): The text color of the Button.
        """
        return self.textColor

    def getWin(self):
        """
        Function accessess the window the Button is placed on.

        Returns:
            win (graphics.GraphWin): The window that the Button is drawn on.
        """
        return self.win

    def setWidth(self, width):
        """
        Function mutates the width of the Button.

        Parameters:
            width (int, float): The width of the Button.
        """
        self.width = width
        self.undraw()
        self.draw(self.win)

    def setHeight(self, height):
        """
        Function mutates the height of the Button.

        Parameters:
            height (int, float): The height of the Button.
        """
        self.height = height
        self.undraw()
        self.draw(self.win)

    def setRadius(self, radius):
        """
        Function mutates the radius of the Button.

        Parameters:
            radius (int, float): The radius of the Button border.
        """
        # Change the radius
        self.radius = radius
        if self.radius * 2 <= self.height and self.radius * 2 <= self.width:
            self.radiusInd = True
        else:
            self.radiusInd = False
        # Redraw the Button
        self.undraw()
        self.draw(self.win)

    def setCenter(self, p):
        """
        Function mutates the center of the Button.

        Parameters:
            p (Point): The center of the Button.
        """
        moveX, moveY = p.getX() - self.centerX, p.getY() - self.centerY
        self.centerX, self.centerY = p.getX(), p.getY()
        # Check if there are circles to move
        if self.radiusInd:
            self.circle1.move(moveX, moveY)
            self.circle2.move(moveX, moveY)
            self.circle3.move(moveX, moveY)
            self.circle4.move(moveX, moveY)
        self.poly.move(moveX, moveY)
        self.textBox.move(moveX, moveY)
        self.shadow.move(moveX, moveY)
        self.p1.move(moveX, moveY)
        self.p2.move(moveX, moveY)
        self.p3.move(moveX, moveY)
        self.p4.move(moveX, moveY)

    def setColor(self, color):
        """
        Function mutates the color of the Button.

        Parameters:
            color (str): The color of the Button.
        """
        # Check if there are circles to fill
        if self.radiusInd:
            self.circle1.setFill(color)
            self.circle1.setOutline(color)
            self.circle2.setFill(color)
            self.circle2.setOutline(color)
            self.circle3.setFill(color)
            self.circle3.setOutline(color)
            self.circle4.setFill(color)
            self.circle4.setOutline(color)
        self.poly.setOutline(color)
        self.poly.setFill(color)

    def setText(self, text):
        """
        Function mutates the text of the Button.

        Parameters:
            text (str): The text of the Button.
        """
        self.text = text
        self.textBox.setText(self.text)

    def setTextColor(self, color):
        """
        Function mutates the color of the label of the Button.

        Parameters:
            textColor (str): The color of the label of the Button.
        """
        self.textColor = color
        self.textBox.setOutline(self.textColor)
        self.textBox.setFill(self.textColor)

    def setTextSize(self, size):
        """
        Function mutates the text size of the label of the Button.

        Parameters:
            textSize (int): The text size of the label of the Button.
        """
        self.textSize = size
        self.textBox.setSize(self.textSize)

    def setWin(self, win):
        """
        Function mutates the window the Button is placed on.

        Parameters:
            win (graphics.GraphWin): The window the Button is drawn on.
        """
        self.undraw()
        self.win = win
        self.draw(self.win)

    def getTimesClicked(self):
        """
        Function returns the number of times a Button has been clicked.

        Returns:
            timesClicked (int): The number of times a Button has been clicked.
        """
        return self.timesClicked

    def setTimesClicked(self, timesClicked):
        """
        Function sets the number of times a Button has been clicked.

        Parameters:
            timesClicked (int): The number of times a Button has been clicked.
        """
        self.timesClicked = timesClicked

    def setInactiveColor(self, color):
        """
        Function sets the deactive state color.

        Parameters:
            color (str): The color of the deactive Button.
        """
        if self.isActive():
            self.deactiveColor = color
        else:
            self.color = color


