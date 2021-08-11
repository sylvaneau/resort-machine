from rescan import color

CROP_IMAGE_Y = 500
CROP_IMAGE_HEIGHT = 800

AREA_MIN_RADIUS = 10

ColorCodes = {
    color.COLOR_NAME_BLACK: color.ColorCode(color.COLOR_NAME_BLACK, 0, 1, None),
    color.COLOR_NAME_BROWN: color.ColorCode(color.COLOR_NAME_BROWN, 1, 10, 1),
    color.COLOR_NAME_RED: color.ColorCode(color.COLOR_NAME_RED, 2, 100, 2),
    color.COLOR_NAME_ORANGE: color.ColorCode(color.COLOR_NAME_ORANGE, 3, 1000, None),
    color.COLOR_NAME_YELLOW: color.ColorCode(color.COLOR_NAME_YELLOW, 4, 10000, None),
    color.COLOR_NAME_GREEN: color.ColorCode(color.COLOR_NAME_GREEN, 5, 100000, 0.5),
    color.COLOR_NAME_BLUE: color.ColorCode(color.COLOR_NAME_BLUE, 6, 1000000, 0.25),
    color.COLOR_NAME_VIOLET: color.ColorCode(color.COLOR_NAME_VIOLET, 7, 10000000, 0.1),
    color.COLOR_NAME_GREY: color.ColorCode(color.COLOR_NAME_GREY, 8, 100000000, 0.05),
    color.COLOR_NAME_WHITE: color.ColorCode(color.COLOR_NAME_WHITE, 9, 1000000000, None),
    color.COLOR_NAME_GOLD: color.ColorCode(color.COLOR_NAME_GOLD, None, 0.1, 5),
    color.COLOR_NAME_SILVER: color.ColorCode(color.COLOR_NAME_SILVER, None, 0.01, 10),
}

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
ColorRanges = [
    color.ColorRange((0, 0, 0), (179, 64, 38), "BLACK", (0, 0, 0), ColorCodes[color.COLOR_NAME_BLACK]),
    color.ColorRange((5, 100, 20), (17, 255, 255), "BROWN", (19, 69, 139), ColorCodes[color.COLOR_NAME_BROWN]),
    color.ColorRange((0, 100, 20), (6, 255, 255), "RED_LOW", (0, 0, 180), ColorCodes[color.COLOR_NAME_RED]),
    color.ColorRange((170, 100, 20), (179, 255, 255), "RED_HIGH", (0, 0, 255), ColorCodes[color.COLOR_NAME_RED]),
]