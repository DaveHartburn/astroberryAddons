#!/usr/bin/python

# Test 1 channel relay
# Connections for relay board
# GND to GND
# Vcc to Pi 5v
# IN1 Pi GPIO pins

# Setting pin to False is on and True is off

import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

RELAY1 = 17
RELAY2 = 27

# Init relay and make sure all are off
GPIO.setup(RELAY1, GPIO.OUT)
GPIO.output(RELAY1, GPIO.HIGH)
GPIO.setup(RELAY2, GPIO.OUT)
GPIO.output(RELAY2, GPIO.HIGH)


