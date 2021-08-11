import cv2


def getImage(imageSource):
    image = imageSource.GetImage()

    if image is None:
        raise ValueError

    return image


def cropImageVertical(image, y, height):
    width = image.shape[1]
    image = image[y:y + height, 0:width]


def blurImage(image):
    return cv2.GaussianBlur(image, (11, 11), 0)
