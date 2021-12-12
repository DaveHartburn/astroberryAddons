#!/usr/bin/python

# stepperWiring.py - Dave Hartburn March 2021
#
# Tests the wiring connections to a ULN2003 stepper motor driver
# Made after I noticed the motor was stuttering and one of the four
# lights failed to show.
# The UNL2003 module has 4 lights and will show when that channel
# is set to high. This script should flash the lights but probably
# will not do anything useful with the motor

import RPi.GPIO as GPIO
import time

# Define the stepper pins in numeric order. Note this is different
# for the actual stepper lib. Use GPIO numbers
stepPins=[5, 6, 13, 19]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Set all pins as output with initial state low
GPIO.setup(stepPins, GPIO.OUT, initial=GPIO.LOW)

# Cycle through each set of pins
for p in stepPins:
    print(f"Blinking pin {p}")
    for i in range(4):
        print("  HIGH")
        GPIO.output(p, GPIO.HIGH)
        time.sleep(0.5)
        print("  LOW")
        GPIO.output(p, GPIO.LOW)
        time.sleep(0.5)
