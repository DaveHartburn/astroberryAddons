# keyPressTest.py
# Detects key presses in a loop
# Uses the curses library - see https://docs.python.org/3.3/howto/curses.html
# Reference at https://docs.python.org/3/library/curses.html

import curses
import time

stdscr = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.noecho()
stdscr.keypad(1)    # Required for cursor keys to work
stdscr.nodelay(1)   # Run in non-blocking mode
curses.curs_set(0)  # Set cursor to invisible

def quit():
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    print("Bye bye")
    exit(0)




i=0
j=0
c=0
limit=256
msg="Will count to "+str(limit)+" then exit"
while True:
    stdscr.addstr(0,0,"I = {}, J = {}".format(i, j), curses.A_BOLD)
    stdscr.addstr(1,0,"Keypress c = {}".format(c))
    stdscr.addstr(2,0,msg)
    stdscr.clrtoeol()
    stdscr.refresh()
    time.sleep(0.5)
    c = stdscr.getch()
    if c == ord('g'):
        msg = "Ohh a g"
    elif c == curses.KEY_UP:
        msg = "j++"
        j+=1
    elif c == curses.KEY_DOWN:
        msg = "j--"
        j-=1
    elif c == ord('q'):
        quit()
    elif c == -1:
        # No keypress, ignore
        c = 0
    else:
        msg = "Unknown key pressed"
    i+=1
    if(i==limit):
        quit()
