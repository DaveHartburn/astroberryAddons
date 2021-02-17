# Stepper motor based telescope focuser
# Dave Hartburn - Febuary 2021
#
# Controls a stepper motor which will drive the focus knob on a Celestron
# NexStar 90SLT, though could be used for any telescope with the correct
# attachments.
#
# This server allows remote control via an infrared control and also implements
# a basic network protocol, to allow a graphical client to attach. At some point
# it should be upgraded to integrate with INDI/EKOS.
#
# The remote is a basic arduino remote (see eBay!) with four directional arrows
# an ok, *, # and numbers 0 to 9. Motor positions are displayed on an SSD1306 screen
# When setup correctly with ir-keytable, we can use the linux event system for input
#
# The focuser has no idea what position it is in, at power on this is always zero.
#
# Basic command set:
#   Network   Remote    Function
# x  STOP      OK        Stops the motor
# x  CW        Right     Start turning clockwise
# x  ACW       Left      Start turning anti-clockwise
# x  SPU       Up        Increase speed, returns speed as %
# x  SPD       Down      Decrease speed, returns speed as %
# X  SETS x              Set speed
#             1-9,0     Set speed 10%-90%,100%
# x  SSA       *         Single movement anticlockwise
# x  SSC       #         Single movement clockwise
# x  GPOS                Get motor position, returns an integer
#
# To Do:
#  Display screen
#  Network input
#  GitHub

from stepperLib import BYJstepper
import time
import curses
import os
from evdev import *
from select import select
import re

# Display libraries
import RPi.GPIO as GPIO
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# Defaults
startPos=0
stepSpeed=50     # Percentage speed
minStep=8         # Less than 8 (especially 1 or 2), give poor performance
dir = 0         # Direction, 0 for stopped, 1 clockwise, -1 anti-clockwise
                # Direction refers to the focus knob, the motor turns the opposite
SOFF=30         # How many seconds before the screen turns off

# Define the stepper pins, the mis-ordering is intentional
# stepPins=[29,33,31,35] -- was pin numbers, use GPIO
stepPins=[5,13,6,19]

# How many steps per revolution does this motor perform?
SPR=32
# Steps per output revolution = 32 * 64
SPOR=2048

# Init the stepper
stepper = BYJstepper(SPR, stepPins, True, GPIO.BCM)
stepper.setSpeedPc(stepSpeed)

# Set up the IR remote
irin = None
# Scan for IR device
devices = [InputDevice(path) for path in list_devices()]
for device in devices:
    #print(device.path, device.name, device.phys)
    if(device.name=="gpio_ir_recv"):
        irin = device

if(irin == None):
    print("Unable to find IR input device")
else:
    print("IR input device found at", irin.path)

# Set up the display screen
i2c = busio.I2C(SCL, SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
# Clear display.
disp.fill(0)
disp.show()
dispTime=0          # Time the display went on
dispOn=False        # Track if the display is on

# Load default font.
font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 24)

# ****** Functions ***************
def readIR(device):
    # Reads events from the IR device, or returns none
    # Ketcode is returned as a string. Uses async io to avoid blocking
    rtnCode = None
    r,w,x = select([device.fd], [], [], 0.01)   # Short wait to avoid motor stutter

    if r:
        for event in irin.read():
            if(event.type == ecodes.EV_KEY):
                data = categorize(event)
                if(data.keystate==data.key_down):
                    rtnCode = data.keycode

    return rtnCode
# End of readIR()

def displayPosition(disp, pos):
    # Show the current position on the screen
    global dispOn, dispTime

    # If the display is off, turn it on
    if(dispOn==False):
        dispTime=time.time()
        dispOn=True

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    image = Image.new("1", (disp.width, disp.height))
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    draw.text((0,0), "Focus:", font=font, fill=255)
    draw.text((0,22), str(pos), font=font, fill=255)
    disp.image(image)
    disp.show()

def blankDisplay(disp):
    # Create blank image for drawing.
    global dispOn
    # Make sure to create image with mode '1' for 1-bit color.
    image = Image.new("1", (disp.width, disp.height))
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
    dispOn=False
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=0)
    disp.image(image)
    disp.show()


# ******* Main code **************


vquit = False
netMsg = ""         # Message from network input

# Main loop
while vquit == False:
    # Read from IR remote
    irKey = readIR(irin)

    newPos = None       # Check for change of position
    if(irKey != None):
        # Keydown detected
        #print("Read a key ", irKey)

        # Regex match for numeric key, tested later
        keyMatch = re.search("KEY_([1-9])", irKey)

        if(irKey == "KEY_RIGHT" or netMsg == "CW"):
            dir = 1
        elif(irKey == "KEY_LEFT" or netMsg == "ACW"):
            dir = -1
        elif(irKey == "KEY_OK" or netMsg == "STOP"):
            dir = 0
        elif(irKey == "KEY_UP" or netMsg == "SPU"):
            stepSpeed+=10
            if(stepSpeed>100):
                stepSpeed=100
            print("Speed =", stepSpeed)
            stepper.setSpeedPc(stepSpeed)
        elif(irKey == "KEY_DOWN" or netMsg == "SPD"):
            stepSpeed-=10
            if(stepSpeed<10):
                stepSpeed=10    # 10 min speed as 0 is useless
            print("Speed =", stepSpeed)
            stepper.setSpeedPc(stepSpeed)
        elif(irKey == "KEY_0"):
            stepSpeed=100
            print("Speed =", stepSpeed)
            stepper.setSpeedPc(stepSpeed)
            minStep=32
        elif(keyMatch):
            sp = keyMatch.group(1)
            stepSpeed=int(sp)*10
            print("Speed =", stepSpeed)
            stepper.setSpeedPc(stepSpeed)
        elif((irKey == "KEY_NUMERIC_STAR" or netMsg == "SSA") and dir==0):
            # Nudge anti-clockwise. Will not do this while the motor is in motion
            newPos = stepper.step(-minStep)
            print("ACW nudge")
        elif((irKey == "KEY_NUMERIC_POUND" or netMsg == "SSC") and dir==0):
            # Nudge anti-clockwise. Will not do this while the motor is in motion
            newPos = stepper.step(minStep)
            print("CW nudge")
        elif(netMsg == "GPOS"):
            # Get position request. If we set newPos then comms is handled below, same as move
            newPos = stepper.getPosition()

    # If the direction is not zero, turn a single minStep, keep calling in
    # order to allow for remote response
    if(dir!=0):
        newPos = stepper.step(dir*minStep)

    if(newPos!=None):
        # Position has changed. Updated screen and report to network clients
        #print("Position=",newPos)
        displayPosition(disp, newPos)

    # Blank the display?
    if(dispOn==True):
        if(time.time() > dispTime+SOFF):
            blankDisplay(disp)
