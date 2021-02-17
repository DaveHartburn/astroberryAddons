# basicFocus.py - Very basic focus control using the keyboard
# Dave Hartburn - January 2021

from stepperLib import BYJstepper
import time
import curses
import os

# Define the stepper pins, the mis-ordering is intentional
stepPins=[29,33,31,35]
# How many steps per revolution does this motor perform?
SPR=32
# Steps per output revolution = 32 * 64
SPOR=2048

# Init the stepper
stepper = BYJstepper(SPR, stepPins, True)

# Init the curses library for keyboard input and display
stdscr = curses.initscr()
curses.noecho()
stdscr.keypad(1)    # Required for cursor keys to work
stdscr.nodelay(1)   # Run in non-blocking mode
curses.curs_set(0)  # Set cursor to invisible

def quit():
    # Quit cleanly resetting the terminal
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    exit(0)

# Set some defaults
stepSpeed = 20
dir = 0
direction = "Stopped"   # Text string
minStep = 8             # Steps of less give poor motor performance, 1&2 don't work
vquit = False

stepper.setSpeedPc(stepSpeed)

while vquit == False:
    stdscr.addstr(0,0,"Use left and right arrow keys to change direction")
    stdscr.addstr(1,0,"Use up and down arrow keys to change speed, z & x to change step")
    stdscr.addstr(2,0,"n and m to nudge one step anti-clockwise or clockwise")
    stdscr.addstr(3,0,"Q to quit and S to stop")
    stdscr.addstr(4,0,"Direction: "+direction)
    stdscr.clrtoeol()
    stdscr.addstr(5,0,"Speed: {}%  step={}".format(stepSpeed,minStep))
    stdscr.clrtoeol()
    stdscr.addstr(6,0,"Position: "+str(stepper.position))
    stdscr.clrtoeol()
    stdscr.refresh()

    c = stdscr.getch()
    if c == ord('q') or c == ord('Q'):
        vquit=True
    elif c == ord('s') or c == ord('S'):
        dir = 0
        direction = "Stopped"
    elif c == curses.KEY_RIGHT:
        dir = -1
        direction = "Clockwise"
    elif c == curses.KEY_LEFT:
        dir = 1
        direction = "Anti-clockwise"
    elif c == curses.KEY_UP:
        stepSpeed+=5;
        if(stepSpeed>100):
            stepSpeed=100
        stepper.setSpeedPc(stepSpeed)
    elif c == curses.KEY_DOWN:
        stepSpeed-=5
        if(stepSpeed<5):
            stepSpeed=5
        stepper.setSpeedPc(stepSpeed)
    elif c == ord('z'):
        minStep-=1
    elif c == ord('x'):
        minStep+=1
    elif c == ord('n') and dir==0:
        stepper.step(minStep)
    elif c == ord('m') and dir==0:
        stepper.step(-minStep)

    # If the direction is not zero, turn a single step. Keep calling in order
    # to allow for keyboard response
    if(dir!=0):
        stepper.step(dir*minStep)

# End of main loop
quit()
