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

# **************************

rout1=GPIO.LOW
rout2=GPIO.HIGH

while True:
	if(rout1==GPIO.LOW):
		rout1=GPIO.HIGH
		rout2=GPIO.LOW
		print("On")
	else:
		rout1=GPIO.LOW
		rout2=GPIO.HIGH		
		print("Off")
		
	GPIO.output(RELAY1, rout1)
	GPIO.output(RELAY2, rout2)
	time.sleep(2)

print("Done")
GPIO.cleanup()	
	
# ****************************************************

