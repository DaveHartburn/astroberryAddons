# Python stepper motor library
# Dave Hartburn - Jan 2021
#
# Written to drive a 28BJY-48 5V DC Stepper on a Pi 4
# using a ULN2003 module
#
# Wiring:
#   Pi    ---- ULN2003
# 2 (5v)  ---- Vcc
# 14 (GND) --- GND
# 29 (GPIO 5)- IN1
# 31 (GPIO 6)- IN2
# 33 (GPIO 13) IN3
# 35 (GPIO 19) IN4

import RPi.GPIO as GPIO
import time

# Init the Pi GPIO
GPIO.setwarnings(False)


class BYJstepper():
    # Class for driving a 28BYJ-48 stepper with a ULN2003 module
    # Based on the arduino stepper library:
    # https://github.com/arduino-libraries/Stepper
    # This version will only control 4 wire steppers

    # Call with the number of steps per motor (not output) revolutions per step,
    # an array containing the four pins
    # If disable=True, the motor will be put into a standby (all zero) state after
    # each turn operation. This saves power if used in a battery application

    # Speed is a value of 1 to about 960. Above 960 there is little speed difference
    # and above about 1870, the motor fails to turn. Python and the Pi are not real
    # time so there may be differences from system to system depending on power and load

    # Position is recorded as zero on init. This has no relation to any physical
    # position unless you have some way to home the motor. It is used to keep
    # track of the number of turns anti-clockwise and clockwise it has move.
    # If it turns 30 clockwise and 40 anti-clockwise, position will be -10

    def __init__(self, nostep, pins, disable, gpioMode):
        # Define basic variables
        self.pins=pins
        self.step_number = 0   # Which step the motor is on
        self.direction = 0     # Motor direction
        self.position = 0       # Assume position 0 on start
        self.last_step_time = 0 # Time stamp of last step taken
        self.nostep = nostep    # Total number of steps for this motor
        self.nopins = 4         # Number of output pins
        self.powerDown = disable
        self.spor = nostep * 64     # Steps per output revolution
        self.maxSpeed = 960         # The max speed by experimentation. This limit is not
                                    # imposed and can be overridden with setSpeed. Used for
                                    # setting a speed by percentage
        GPIO.setmode(gpioMode)

        # Define the step sequences
        self.seq = [
            [GPIO.HIGH, GPIO.LOW, GPIO.HIGH, GPIO.LOW],     # 1010
            [GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW],     # 0110
            [GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.HIGH],     # 0101
            [GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH]      # 1001
        ]
        # Init the pins for output and put all to LOW (stepper disabled)
        GPIO.setup(pins, GPIO.OUT, initial=GPIO.LOW)

        # Set a default speed of 200
        self.setSpeed(200)

    def disable(self):
        # Sets all motor pins to zero
        GPIO.output(self.pins, [GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW])

    def setSpeed(self, sp):
        self.step_delay = 60 * 1000 / self.nostep / sp
        # 1000  less than the original arduino code, which worked in micro seconds

    def setSpeedPc(self, pc):
        # Sets the speed according to the defined max speed
        self.setSpeed(round(pc/100*self.maxSpeed))
        
    def setMaxSpeed(self, max):
        # Sets the maximum speed, used for calculating by percentage
        self.maxSpeed = max

    def resetPosition(self):
        # Sets the position to zero
        self.position = 0

    def getPosition(self):
        # Return the current position variable
        return self.position

    def turnDeg(self, d):
        # Turn the specified number of degrees clockwise
        # Need to invert value
        steps_to_turn = round((d/360) * self.spor)*-1
        self.step(steps_to_turn)

    def step(self, stm):
        # Move stm numbers of steps
        steps_left = abs(stm)

        # Determine direction based on whether stm is + or -
        if stm > 0:
            self.direction = 1
        else:
            self.direction = 0

        while steps_left > 0:
            now = self.timeMillis()
            # Move only if the appropriate delay has passed
            if(now - self.last_step_time >= self.step_delay):
                # Get the timestamp of when you last stepped:
                self.last_step_time = self.timeMillis()
                # Increment or decrement the step number, depending on direction
                if(self.direction == 1):
                    self.step_number+=1
                    if(self.step_number>self.nostep):
                        # Reached max, reset
                        self.step_number=0
                else:
                    if(self.step_number==0):
                        self.step_number = self.nostep
                    self.step_number-=1
                # Decrement the steps left
                steps_left-=1
                # Step the motor
                self.stepMotor(self.step_number % 4)
        # End of while
        if(self.powerDown):
            # Drop power to pins
            self.disable()

        # Set the position counter
        self.position+=stm
        return self.position
    # End of step()

    def stepMotor(self, thisStep):
        GPIO.output(self.pins, self.seq[thisStep])

    def timeMillis(self):
        return round(time.time() * 1000 )

# End of BYJstepper class
