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
#   Command   Remote    Function
#   STOP      OK        Stops the motor
#   CW        Right     Start turning clockwise
#   ACW       Left      Start turning anti-clockwise
#   SPU       Up        Increase speed, returns speed as %
#   SPD       Down      Decrease speed, returns speed as %
#   SETS x              Set speed
#             1-9,0     Set speed 10%-90%,100%
#   SSA       *         Single movement anticlockwise
#   SSC       #         Single movement clockwise
#   GPOS                Get motor position, returns an integer
#   QUIT                Quit the network client
#   SQUIT               Quit the server
#
# Network connections send the commands in the above format
# IR is translated
#
# To Do:
#  Network input
#  Change step rate with speed
#  Speed command
#  Multithread continuous movement
#  Network connection terminate
#  Server shutdown

from stepperLib import BYJstepper
import time
import os
from evdev import *
from select import select
import re
from queue import Queue
from threading import Thread

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
DUPDATE=1     # How often to update the screen when active. Too often hits performance

SERVER_PORT=3030    # Port to connect to
SERVER_HOST='localhost' # ** need this to default to any

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
def irServer(cmdQueue, device):
    # A loop to read input from the IR device and put appropriate command on the queue
    while True:
        # Read from IR. Blocks until input is received
        keyPress = readIR(device)
        if(keyPress!=None):
            msg=None

            # Rexex match for numeric key, tested later
            keyMatch = re.search("KEY_([1-9])", keyPress)

            # Translate keypress into message
            if(keyPress=="KEY_RIGHT"):
                msg="CW"
            elif(keyPress=="KEY_LEFT"):
                msg="ACW"
            elif(keyPress=="KEY_OK"):
                msg="STOP"
            elif(keyPress=="KEY_UP"):
                msg="SPU"
            elif(keyPress=="KEY_DOWN"):
                msg="SPD"
            elif(keyPress=="KEY_0"):
                msg="SETS 100"
            elif(keyPress=="KEY_NUMERIC_STAR"):
                msg="SSA"
            elif(keyPress=="KEY_NUMERIC_POUND"):
                msg="SSC"
            elif(keyMatch):
                # Matched another numeric key
                sp = keyMatch.group(1)
                stepSpeed=int(sp)*10
                msg="SETS "+str(stepSpeed)
            # Put message on queue, or do nothing if unknown key
            if(msg!=None):
                cmdQueue.put(msg)

def readIR(device):
    # Reads events from the IR device, or returns none
    # Keycode is returned as a string, with None returned for things other than a key down
    rtnCode = None
    r,w,x = select([device.fd], [], [])   # Functions blocks

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
        dispOn=True
        dispTime=time.time()
    else:
        # Are we ready for an update?
        if( time.time() > (dispTime+DUPDATE)):
            # Yes update the clock
            dispTime=time.time()
        else:
            # No, quit
            return

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
netMsg = ""

# Set up messaging queue for input commands
cmdQueue = Queue()

# Start IR thread
irThread = Thread(target=irServer, args=(cmdQueue, irin, ))
irThread.start()

# Temp main loop
while vquit == False:
    newPos = None       # Check for change of position

    # Anything on the qeueue?
    if(cmdQueue.empty()==False):
        cmdIn=cmdQueue.get()
        print("Command received ", cmdIn)
        # Process command actions
        if(cmdIn == "CW"):
            print("Clockwise motor")
            dir = 1
        elif(cmdIn == "ACW"):
            print("Anti-clockwise motor")
            dir = -1
        elif(cmdIn == "STOP"):
            dir = 0
        elif(cmdIn == "SPU"):
            stepSpeed+=10
            if(stepSpeed>100):
                stepSpeed=100
            print("Speed =", stepSpeed)
            stepper.setSpeedPc(stepSpeed)
        elif(cmdIn == "SPD"):
            stepSpeed-=10
            if(stepSpeed<10):
                stepSpeed=10    # 10 min speed as 0 is useless
            print("Speed =", stepSpeed)
            stepper.setSpeedPc(stepSpeed)
        elif(cmdIn.startswith("SETS")):
            s = cmdIn.split()
            stepSpeed=int(s[1])
            print("Direct speed set to ", stepSpeed)
            stepper.setSpeedPc(stepSpeed)
            #minStep=32
        elif((cmdIn == "SSA") and dir==0):
            # Nudge anti-clockwise. Will not do this while the motor is in motion
            newPos = stepper.step(-minStep)
            print("ACW nudge")
        elif((cmdIn == "SSC") and dir==0):
            # Nudge anti-clockwise. Will not do this while the motor is in motion
            newPos = stepper.step(minStep)
            print("CW nudge")
        elif(cmdIn == "GPOS"):
            # Get position request. If we set newPos then comms is handled below, same as move
            newPos = stepper.getPosition()
    # End of processing new messages

    # If the direction is not zero, turn a single minStep, keep calling in
    # order to allow for command response
    if(dir!=0):
        newPos = stepper.step(dir*minStep)

    if(newPos!=None):
        # Position has changed. Updated screen and report to network clients
        # Forking off into own short lived thread to stop motor pulsing
        #print("Position=",newPos)
        duThread = Thread(target=displayPosition, args=(disp, newPos,))
        duThread.start()

    # Blank the display?
    if(dispOn==True):
        if(time.time() > dispTime+SOFF):
            blankDisplay(disp)
