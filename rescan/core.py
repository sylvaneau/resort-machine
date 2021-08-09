# import the necessary packages
from collections import deque
import numpy as np
import argparse
import cv2
import time
import sys

def main():
    print('lets go')

def toto():
    # define the lower and upper boundaries of the "green"
    # ball in the HSV color space, then initialize the
    # list of tracked points
    # GREEN
    #greenLower = (55, 80, 20)
    #greenUpper = (80, 255, 255)

    # Brown
    # greenLower = (0, 87, 0)
    # greenUpper = (16, 255, 87)

    # black
    greenLower = (0, 87, 0)
    greenUpper = (16, 255, 87)

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", help="path to the (optional) image file")
    args = vars(ap.parse_args())

    # Check first is an image path was supplied,
    # then check for a video path
    # and finally try grab the reference to the webcam
    if args.get("image", False):
        vs = None
        frame = cv2.imread(args["image"])

        if frame is None:
            sys.exit("Could not read the image.")
    else:
        vs = cv2.VideoCapture(0)

        if not vs.isOpened():
            sys.exit("Cannot open camera")

    # allow the camera or file to warm up
    time.sleep(2.0)

    # keep looping
    while True:
        if vs:
            # grab the current frame
            ret, frame = vs.read()

            if not ret:
                break

        # resize the frame, blur it, and convert it to the HSV
        # color space
        # frame = cv2.resize(frame, (960, 540))
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)

        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        ctrs, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        result = frame.copy()

        if len(ctrs) > 0:
            # c = max(ctrs, key=cv2.contourArea)
            

            for i in range(len(ctrs)):
                ((x, y), radius) = cv2.minEnclosingCircle(ctrs[i])
                #cv2.circle(result, (int(x), int(y)), int(radius), (255, 255, 255), 1)

                #cv.approxPolyDP(c, 3, True)
                #bb = cv2.boundingRect(ctrs[i])
                #cv2.rectangle(result, (int(bb[0]), int(bb[1])), \
                #(int(bb[0]+bb[2]), int(bb[1]+bb[3])), (50, 255, 255), 1)
                
                if radius > 4:
                    M = cv2.moments(ctrs[i])
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])

                    cv2.circle(result, (cX, cY), 2, (0, 0, 255), 2)
                    cv2.drawContours(result, ctrs, i, (17,255,255), 1)

        #cv2.imshow("Original", frame)
        #cv2.imshow("Blured", blurred)
        #cv2.imshow("Mask", mask)
        cv2.imshow("Result", result)

        key = cv2.waitKey(1) & 0xFF
        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break

    if vs:
        vs.release()

    # close all windows
    cv2.destroyAllWindows()