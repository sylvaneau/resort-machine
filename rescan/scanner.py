import cv2

from rescan import color, settings
from rescan.image import imagesource, imageutils


class Scanner:
    
    def __init__(self):
        pass
    
    def extractColorStrips(self, imageSource: imagesource.ImageSource) -> list[color.ColorStrip]:
        # get a new image
        image = imageutils.getImage(imageSource)
        
        # crop it
        image = imageutils.cropImageVertical(image, settings.CROP_IMAGE_Y, settings.CROP_IMAGE_HEIGHT)
        
        # blur it
        blured = imageutils.blurImage(image)

        # and convert it to the HSV color space
        blured = cv2.cvtColor(blured, cv2.COLOR_BGR2HSV)

        # loop through colors ranges to build color areas
        areas: self.extractColorAreas(blured)

        # merge areas that are actually forming the same strip
        groups = self.groupAreas(areas)
        
        # and finally produce strip
        return self.createStrips(groups)
        

    def extractColorAreas(self, image) -> list[color.ColorArea]:
        # initialize result array
        colorAreas: list[color.ColorArea] = []
            
        for colorRange in settings.ColorRanges:
            contours = self.findContours(image, colorRange.lowerBound, colorRange.upperBound)

                # eliminate artifacts (contour too small to be an actual strip)
            for contour in contours:
                colorArea = color.ColorArea(colorRange, contour)
                ((_, _), radius) = colorArea.getMinEnclosingCircle()
                        
                if radius > settings.AREA_MIN_RADIUS:
                    colorAreas.append(colorArea)
        
        return colorAreas
    
    def findContours(self, image, lowerBound, upperBound):
        # apply a color mask to find contours
        mask = cv2.inRange(image, lowerBound, upperBound)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        return contours

    def groupAreas(self, areas: 'list[color.ColorArea]') -> 'list[color.ColorAreaGroup]':
        groups: list[color.ColorAreaGroup] = []
        
        for area in areas:
            groups = self.__createGroups(area, groups)

        return groups

    def __createGroups(self, area: color.ColorArea, existingGroups: 'list[color.ColorAreaGroup]') -> 'list[color.ColorAreaGroup]':
        result: list[color.ColorAreaGroup] = []
        
        # encapsulate the candidate area in a group
        newGroup = color.ColorAreaGroup(area)

        # go though already existing groups
        for group in existingGroups:
            # To check if groups overlap wa are actually testing for the opposite (no overlap)
            # if there is no overlap, dont touch the existing group and skip to the next one
            if newGroup.xMin > group.xMax or newGroup.xMax < group.xMin:
                result.append(group)
                continue

            # if they do, merge the exiting group in the newly created one (will raise an error if color codes doesn't match)
            # and go to the next group
            newGroup.mergeGroup(group)
        
        # at the end append the new group to the result, either as a single area group or as a merge of existing groups
        result.append(newGroup)

        return result
    
    def createStrips(self, groups: list[color.ColorAreaGroup]) -> list[color.ColorStrip]:
        sortedStrips: list[color.ColorStrip] = []

        for group in groups:
            newStrip = color.ColorStrip(group)
            append = True
            
            for i in range(0, len(sortedStrips)):
                if sortedStrips[i].xPos == newStrip.xPos:
                    raise ValueError
                
                if newStrip.xPos < sortedStrips[i].xPos:
                    sortedStrips.insert(i, newStrip)
                    append = False
                    break
            
            if append == True:
                sortedStrips.append(newStrip)
        
        return sortedStrips
            
            