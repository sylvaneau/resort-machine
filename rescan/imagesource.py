from abc import abstractmethod
import time
import cv2
import picamera
import picamera.array

class ImageSource:
    @abstractmethod
    def GetImage(self):
        pass

class FileImageSource(ImageSource):

    def __init__(self, filePath):
        self.__filePath = filePath

    def GetImage(self):
        return cv2.imread(self.__filePath)

class RaspCameraImageSource(ImageSource):

    def __init__(self):
        self.__camera = picamera.PiCamera(resolution=(2592, 1944), framerate=5)

        # Set ISO to the desired value
        self.__camera.iso = 100

        # Wait for the automatic gain control to settle
        time.sleep(3.0)

        # Now fix the values
        #self.__camera.shutter_speed = self.__camera.exposure_speed
        #self.__camera.exposure_mode = 'off'
        # g = self.__camera.awb_gains
        # self.__camera.awb_mode = 'off'
        # self.__camera.awb_gains = g

        self.__rawCapture = picamera.array.PiRGBArray(self.__camera, size=(2592, 1944))

    def GetImage(self):
        self.__camera.capture(self.__rawCapture, 'rgb', use_video_port=False)
        image = self.__rawCapture.array

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        self.__rawCapture.truncate(0)

        return image