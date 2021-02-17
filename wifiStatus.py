# wifiStatus.py - Dave Hartburn, January 2021
#
# Displays the wifi network status on a small 0.96" OLED (128x64)
# on start up and on the push of a button.
#
# For screen connection and library set up, see the Adafruit guide at:
# https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi/usage
#
# For connection and background in relation to an Astroberry install, see my
# blog at:
# https://samndave.org.uk/ourdoc/wp-admin/post.php?post=370
#
# Initial screen init, taken from the Adafruit example program referenced above.

import time
import subprocess
import re
import RPi.GPIO as GPIO


from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# How many seconds before the screen powers off?
SOFF=20
UDATE=5 # How often to update the display info when on

# Set up the button
GPIO.setmode(GPIO.BCM)
BPIN = 4
GPIO.setup(BPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Set updates and time out timers
dispTime=time.time()      # Time the display went on
dispOn=True               # The display is on
nextUd=0                # Time of next data update

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Load default font.
font = ImageFont.load_default()
# Define a line height
lh = 10
while True:

    # Read the button
    but = GPIO.input(BPIN)
    if(but == False):
        # Button pressed, set the time the display turned on
        dispTime=time.time()
        dispOn=True

        # Force a data update
        nextUd=0

    if(dispOn==True):

        # Is the display on?
        if(time.time() < dispTime + SOFF):
            # Are we due an update?
            if(time.time()>nextUd):
                # Host & IP
                cmd = "hostname -I | cut -d' ' -f1"
                IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
                cmd = "hostname | cut -d'.' -f1"
                HOST = subprocess.check_output(cmd, shell=True).decode("utf-8")
                # Wireless LAN details
                cmd = "iwconfig wlan0"
                IWCONF = subprocess.check_output(cmd, shell=True).decode("utf-8")
                m = re.search("ESSID:\"(\S+)\".*Signal level=(-\d+)", IWCONF, re.DOTALL)
                if(m == None):
                        # No connection? Are we in hotspot mode?
                        RSSI="n/a"
                        cmd="/usr/bin/nmcli | grep wlan0"
                        NMCLI = subprocess.check_output(cmd, shell=True).decode("utf-8")
                        # Is it connected
                        if("connected" in NMCLI):
                                if("HotSpot" in NMCLI):
                                        SSID="*hotspot*"
                                else:
                                        SSID="*unknown*"
                        else:
                                SSID="disconnected"
                        
                else:
                        SSID=m[1]
                        RSSI=m[2]
                # CPU temp
                cmd = "cat /sys/class/thermal/thermal_zone0/temp"
                T = float(subprocess.check_output(cmd, shell=True).decode("utf-8"))
                TEMP = T/1000

                # Draw a black filled box to clear the image.
                draw.rectangle((0, 0, width, height), outline=0, fill=0)


                draw.text((0, 0), HOST, font=font, fill=255)
                draw.text((0, lh), "IP: " + IP, font=font, fill=255)
                draw.text((0, 2*lh), "SSID: " + SSID, font=font, fill=255)
                draw.text((0, 3*lh), "RSSI: " + RSSI, font=font, fill=255)
                draw.text((0, 4*lh), "CPU temp: {:.1f}".format(TEMP) + u'\N{DEGREE SIGN}' + 'c', font=font, fill=255)
                nextUd=time.time()+UDATE
        else:
            # Time out, set the display off
            dispOn=False
            # Draw a black filled box to clear the image.
            draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # Display image.
        disp.image(image)
        disp.show()
    # End of if(disp==True)
    time.sleep(0.1)
