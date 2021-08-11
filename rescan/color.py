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

    def __init__(self, color_name,
                 resistanceValue, multiplierValue, toleranceValue):
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

    def __init__(self, lowerBound, upperBound, range_name: str, plot_color,
                 color_code: ColorCode):
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

        # S
        if not (s >= 0 & s <= 255):
            raise ValueError(s)

        # V
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

    def __init__(self, area: 'ColorArea'):
        self.__colorCode = area.colorCode
        self.__colorAreas: list[ColorArea] = []
        self.__xMin: int = None
        self.__xMax: int = None
        
        (x, _, w, _) = area.getBoundingRectangle()
        self.__xMin = x
        self.__xMax = x + w
        
        self.__colorAreas.append(area)

    @property
    def colorCode(self):
        return self.__colorCode

    @property
    def colorAreas(self):
        return self.__colorAreas

    @property
    def xMin(self):
        return self.__xMin
    
    @property
    def xMax(self):
        return self.__xMax

    def mergeGroup(self, group: 'ColorAreaGroup'):
        if self.__colorCode != group.colorCode:
            raise ValueError
            
        self.__xMin = min(self.__xMin, group.xMin)
        self.__xMax = max(self.__xMax, group.xMax)
    
        for area in group.colorAreas:
            self.__colorAreas.append(area)
            
    def compute_xPos(self):
        return (self.__xMin + self.__xMax) / 2


class ColorStrip():
    
    def __init__(self, group: ColorAreaGroup):
        self.__colorCode = group.colorCode
        self.__colorAreas = group.colorAreas
        self.__xMin = group.xMin
        self.__xMax = group.xMax
        self.__xPos = group.compute_xPos()

    @property
    def colorCode(self):
        return self.__colorCode
    
    @property
    def colorAreas(self):
        return self.__colorAreas
    
    @property
    def xMin(self):
        return self.__xMin
    
    @property
    def xMax(self):
        return self.__xMax
    
    @property
    def xPos(self):
        return self.__xPos
