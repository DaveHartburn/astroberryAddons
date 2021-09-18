# Basic stepper motor test program, using stepperLib
# By Dave Hartburn - January 2021

import sys
# Add parent directory to import path to find stepper library
sys.path.insert(0, '..')
import RPi.GPIO as GPIO
from stepperLib import BYJstepper
import time

# Define the stepper pins using GPIO numbers, the mis-ordering is intentional
stepPins=[5,13,6,19]
# How many steps per revolution does this motor perform?
SPR=32
# Steps per output revolution = 32 * 64
SPOR=2048

print("Stepper test")

stepper = BYJstepper(SPR, stepPins, True, GPIO.BCM)

print("1 turn clockwise at 100%")
stepper.setSpeedPc(100)
stepper.turnDeg(360)
time.sleep(2)

print("1 turn anti-clockwise at 33%")
stepper.setSpeedPc(33)
stepper.turnDeg(-360)
time.sleep(2)


stepper.setSpeed(200)

print("1 turn clockwise - speed 200")
stepper.turnDeg(360)
time.sleep(2)

print("1 turn anti-clockwise - speed 200")
stepper.turnDeg(-360)
time.sleep(2)

stepper.setSpeed(400)
print("1/2 turn clockwise - speed 400")
stepper.turnDeg(180)
time.sleep(2)
print("1/2 turn anti-clockwise - speed 400")
stepper.turnDeg(-180)
time.sleep(2)

stepper.setSpeed(800)
print("1/4 turn clockwise - speed 800")
stepper.turnDeg(90)
time.sleep(2)
print("1/4 turn anti-clockwise - speed 800")
stepper.turnDeg(-90)
time.sleep(2)

stepper.setSpeed(1100)
print("Fast turn clockwise - speed 1100")
stepper.turnDeg(360)

stepper.disable()

time.sleep(2)

print("Done");
