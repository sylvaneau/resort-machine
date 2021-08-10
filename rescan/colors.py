
from argparse import REMAINDER

import cv2

COLOR_NAME_BLACK = "BLACK"
COLOR_NAME_BROWN = "BROWN"
COLOR_NAME_RED = "RED"
COLOR_NAME_ORANGE = "ORANGE"
COLOR_NAME_YELLOW = "YELLOW"
COLOR_NAME_GREEN = "GREEN"
COLOR_NAME_BLUE = "BLUE"
COLOR_NAME_VIOLET = "VIOLET"
COLOR_NAME_GREY = "GREY"
COLOR_NAME_WHITE = "WHITE"
COLOR_NAME_GOLD = "GOLD"
COLOR_NAME_SILVER = "SILVER"

class ColorCode:

    def __init__(self, color_name, resistanceValue, multiplierValue, toleranceValue):
        self.__colorName = color_name
        self.__resistanceValue = resistanceValue
        self.__multiplierValue = multiplierValue
        self.__toleranceValue = toleranceValue

    @property
    def colorName(self):
        return self.__colorName

    @property
    def resistanceValue(self):
        return self.__resistanceValue

    @property
    def multiplierValue(self):
        return self.__multiplierValue

    @property
    def toleranceValue(self):
        return self.__toleranceValue


class ColorRange:

    def __init__(self, lowerBound, upperBound, range_name: str, plot_color, color_code: ColorCode):
        self.__lowerBound = self.__checkRange(lowerBound)
        self.__upperBound = self.__checkRange(upperBound)
        self.__range_name = range_name
        self.__plot_color = plot_color
        self.__color_code = color_code

    @property
    def lowerBound(self):
        return self.__lowerBound

    @property
    def upperBound(self):
        return self.__upperBound

    @property
    def rangeName(self):
        return self.__range_name

    @property
    def plotColor(self):
        return self.__plot_color

    @property
    def colorCode(self):
        return self.__color_code

    def __checkRange(self, hsv):
        h = hsv[0]
        s = hsv[1]
        v = hsv[2]
        
        # H
        if not (h >= 0 & h <= 179):
            raise ValueError(h)

        #S
        if not (s >= 0 & s <= 255):
            raise ValueError(s)

        #V
        if not (v >= 0 & v <= 255):
            raise ValueError(v)

        return hsv


class ColorArea:
    
    def __init__(self, color_range: ColorRange, contour):
        self.__color_range = color_range
        self.__contour = contour
        self.__minEnclosingCircle = None
        self.__boundingRectangle = None

    @property
    def colorRange(self):
        """The colorRange property."""
        return self.__color_range

    @property
    def colorCode(self):
        """The colorCode property."""
        return self.__color_range.colorCode

    @property
    def contour(self):
        """The contour property."""
        return self.__contour

    def getMinEnclosingCircle(self):
        if self.__minEnclosingCircle is None:
            self.__minEnclosingCircle = cv2.minEnclosingCircle(self.__contour)
        
        return self.__minEnclosingCircle

    def getBoundingRectangle(self):
        if self.__boundingRectangle is None:
            self.__boundingRectangle = cv2.boundingRect(self.__contour)
        
        return self.__boundingRectangle

class ColorAreaGroup():

    """docstring for ColorStrip."""
    def __init__(self, color_code: ColorCode, color_areas: 'list[ColorArea]', boundingRectangle):
        self.__colorCode = color_code
        self.__colorAreas = color_areas
        self.__boundingRectangle = boundingRectangle

    @property
    def colorCode(self):
        return self.__colorCode

    @property
    def colorAreas(self):
        return self.__colorAreas

    @property
    def boundingRectangle(self):
        return self.__boundingRectangle

    def addArea(self, colorArea: ColorArea):
        if self.__colorCode != colorArea.colorCode:
            raise ValueError
        
        self.__colorAreas.append(colorArea)
        self.__boundingRectangle = ColorAreaGroup.__mergeRectangles(self.__boundingRectangle, colorArea.getBoundingRectangle())

    def __mergeRectangles(a, b):
        x = min(a[0], b[0])
        y = min(a[1], b[1])
        w = max(a[0]+a[2], b[0]+b[2]) - x
        h = max(a[1]+a[3], b[1]+b[3]) - y
        return (x, y, w, h)

class ColorStrip():
    """docstring for ColorStrip."""
    def __init__(self, color_code: ColorCode, color_areas: 'list[ColorArea]', boundingRectangle):
        self.__colorCode = color_code
        self.__colorAreas = color_areas
        self.__boundingRectangle = boundingRectangle

    @property
    def colorCode(self):
        return self.__colorCode

    @property
    def colorAreas(self):
        return self.__colorAreas

    @property
    def boundingRectangle(self):
        return self.__boundingRectangle
        

# def addArea(self, colorArea: ColorArea):
#         if self.__colorCode != colorArea.colorCode:
#             raise ValueError
        
#         self.__colorAreas.append(colorArea)
#         self.__boundingRectangle = ColorStrip.__mergeRectangles(self.__boundingRectangle, colorArea.getBoundingRectangle())

#     def __mergeRectangles(a, b):
#         x = min(a[0], b[0])
#         y = min(a[1], b[1])
#         w = max(a[0]+a[2], b[0]+b[2]) - x
#         h = max(a[1]+a[3], b[1]+b[3]) - y
#         return (x, y, w, h)

