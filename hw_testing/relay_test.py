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

print("Relay is connected to GPIO "+str(RELAY1));

# Init relay and make sure all are off
GPIO.setup(RELAY1, GPIO.OUT);
GPIO.output(RELAY1, True);

# **************************

rout1=GPIO.LOW

while True:
	if(rout1==GPIO.LOW):
		rout1=GPIO.HIGH
		print("On")
	else:
		rout1=GPIO.LOW
		print("Off")
		
	GPIO.output(RELAY1, rout1)
	time.sleep(1)

print("Done")
GPIO.cleanup()	
	
# ****************************************************

