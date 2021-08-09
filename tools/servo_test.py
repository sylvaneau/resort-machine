
#Set function to calculate percent from angle
def angle_to_percent (angle) :
    if angle > 180 or angle < 0 :
        return False

    start = 0e
    end = 12.5
    ratio = (end - start)/180 #Calcul ratio from angle to percent

    angle_as_percent = angle * ratio

    return start + angle_as_percent

#import RPi.GPIO as GPIO
#import time


#servoPIN = 18

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(servoPIN, GPIO.OUT)

#p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
#p.start(0) # Initialization

