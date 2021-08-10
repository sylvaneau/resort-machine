# import the necessary packages
from collections import deque

from numpy.core.records import array
from rescan import calibrate
import numpy as np
import argparse
import cv2
import time
import sys

from . import imagesource
from . import colors

ColorCodes = {
    colors.COLOR_NAME_BLACK: colors.ColorCode(colors.COLOR_NAME_BLACK,    0, 1, None),
    colors.COLOR_NAME_BROWN: colors.ColorCode(colors.COLOR_NAME_BROWN,    1, 10, 1),
    colors.COLOR_NAME_RED: colors.ColorCode(colors.COLOR_NAME_RED,        2, 100, 2),
    colors.COLOR_NAME_ORANGE: colors.ColorCode(colors.COLOR_NAME_ORANGE,  3, 1000, None),
    colors.COLOR_NAME_YELLOW: colors.ColorCode(colors.COLOR_NAME_YELLOW,  4, 10000, None),
    colors.COLOR_NAME_GREEN: colors.ColorCode(colors.COLOR_NAME_GREEN,    5, 100000, 0.5),
    colors.COLOR_NAME_BLUE: colors.ColorCode(colors.COLOR_NAME_BLUE,      6, 1000000, 0.25),
    colors.COLOR_NAME_VIOLET: colors.ColorCode(colors.COLOR_NAME_VIOLET,  7, 10000000, 0.1),
    colors.COLOR_NAME_GREY: colors.ColorCode(colors.COLOR_NAME_GREY,      8, 100000000, 0.05),
    colors.COLOR_NAME_WHITE: colors.ColorCode(colors.COLOR_NAME_WHITE,    9, 1000000000, None),
    colors.COLOR_NAME_GOLD: colors.ColorCode(colors.COLOR_NAME_GOLD,      None, 0.1, 5),
    colors.COLOR_NAME_SILVER: colors.ColorCode(colors.COLOR_NAME_SILVER,  None, 0.01, 10),
}

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
ColorRanges = [
    colors.ColorRange((0, 0, 0), (179, 64, 38), "BLACK", (0, 0, 0), ColorCodes[colors.COLOR_NAME_BLACK]),
    colors.ColorRange((5, 100, 20), (17, 255, 255), "BROWN", (19, 69, 139), ColorCodes[colors.COLOR_NAME_BROWN]),
    colors.ColorRange((0, 100, 20), (6, 255, 255), "RED_LOW", (0, 0, 180), ColorCodes[colors.COLOR_NAME_RED]),
    colors.ColorRange((170, 100, 20), (179, 255, 255), "RED_HIGH", (0, 0, 255), ColorCodes[colors.COLOR_NAME_RED]),
]

#signal.signal(signal.SIGINT, self.exit_gracefully)
#signal.signal(signal.SIGTERM, self.exit_gracefully)

def run():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", help="path to the (optional) image file")
    ap.add_argument("-c", "--calibrate", help="open calibration mode", action='store_true')
    args = vars(ap.parse_args())

    # Check first is an image path was supplied,
    # and finally try grab the reference to the webcam
    if args.get("image", False):
        imageSource = imagesource.FileImageSource(args["image"])
    else:
        imageSource = imagesource.RaspCameraImageSource()

    if args.get("calibrate", False):
        image = prepareImage(imageSource)
        calibrate.start_calibration(image)
        exit()

    # keep looping
    while True:
        image = prepareImage(imageSource)

        # and convert it to the HSV color space
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        colorAreas = []

        # loop through colors ranges to build ColorStrips candidates
        for colorRange in ColorRanges:
            # colorRange = colorRanges[rangeKey]

            # apply a color mask to find contours
            mask = cv2.inRange(hsv_image, colorRange.lowerBound, colorRange.upperBound)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # eliminate artifacts (contour too small to be an actual strip)
            for contour in contours:
                colorArea = colors.ColorArea(colorRange, contour)
                ((x, y), radius) = colorArea.getMinEnclosingCircle()
                    
                if radius > 10:
                    colorAreas.append(colorArea)

        # merge areas that are actually forming the same strip
        groups = createGroups(colorAreas)

        cv2.imshow("Result", image)

        colorRange = cv2.waitKey(1) & 0xFF
        # if the 'q' key is pressed, stop the loop
        if colorRange == ord("q"):
            break
    
    # close all windows
    cv2.destroyAllWindows()

def createGroups(areas: 'list[colors.ColorArea]') -> 'list[colors.ColorAreaGroup]':
    groups = []
    
    for area in areas:
        groups = _createGroups(area, groups)

    return groups

def _createGroups(area: colors.ColorArea, groups: 'list[colors.ColorAreaGroup]') -> 'list[colors.ColorAreaGroup]':
    result = []

    newGroup = colors.ColorAreaGroup(area.colorCode, [area], area.getBoundingRectangle())
    isNew = True

    # go though already existing strips
    for group in groups:
        # check if bounding rectangles overlaps
        (x,y,w,h) = group.boundingRectangle
        (nx, ny, nw, nh) = newGroup.boundingRectangle

        # if they doesn't, skip to the next strip
        if nx > x + w | nx + nw < x:
            result.append(group)
            continue

        # if they does, add area to existing strip (will raise an error if color codes doesn't match)
        for oldArea in group.colorAreas:
            newGroup.addArea(oldArea)
        
        result.append(newGroup)

        isNew = False
    
    if isNew == True:
        result.append(newGroup)

    return result

    
    # strips = [colors.ColorStrip]

    # for area in areas:
        
        


    # refStrip = areas[0]
    
    # (x,y,w,h) = refStrip.getBoundingRectangle()

    

    # for i in range(1, len(candidates)):
    #     candidate = candidates[i]
    #     (nx, ny, nw, nh) = candidate.getBoundingRectangle()

    #     if nx > x + w | nx + nw < x:
    #         break

    #     #() union((x,y,w,h), (cx, cy, cw, ch))

    

def prepareImage(imageSource):
# if videoSource is defined we are dealing with the camera to get a new frame
    image = imageSource.GetImage()

    if image is None:
        sys.exit("Could not read the image (file not found or camera not accessible).")

    # crop the image,
    width = image.shape[1]
    image = image[500:1300, 0:width]

    # blur it, 
    image = cv2.GaussianBlur(image, (11, 11), 0)

    return image

# extract center of mass
                    #M = cv2.moments(contours[i])
                    # cX = int(M["m10"] / M["m00"])
                    # cY = int(M["m01"] / M["m00"])


                    # cv2.circle(image, (cX, cY), 2, colorRange.colorBgr, 2)
                    # cv2.drawContours(image, contours, i, (17,255,255), 1)