import argparse

from rescan import calibration, scanner
from rescan.image import imagesource


# signal.signal(signal.SIGINT, self.exit_gracefully)
# signal.signal(signal.SIGTERM, self.exit_gracefully)

# main entry point
def run():
    args = parseCommandLine()

    # Check first is an image path was supplied,
    # and finally try grab the reference to the webcam
    if args.get("image", False):
        imageSource = imagesource.FileImageSource(args["image"])
    else:
        imageSource = imagesource.RaspCameraImageSource()

    # dispatch between calibration and normal operation mode
    if args.get("calibrate", False):
        run_calibration_gui(imageSource)
    else:
        run_scanner(imageSource)


def parseCommandLine():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", help="path to the (optional) image file")
    ap.add_argument("-c", "--calibrate", help="open calibration mode", action='store_true')
    args = vars(ap.parse_args())
    
    return args


def run_calibration_gui(imageSource):
    calibration.start_calibration_gui(imageSource)


def run_scanner(imageSource):
    scan = scanner.Scanner()
    
    while True:
        strips = scan.extractColorStrips(imageSource)
        
        for strip in strips:
            print(strip.colorCode.colorName)
