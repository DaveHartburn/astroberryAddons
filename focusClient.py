# Stepper motor based telescopt focuser client
# Dave Hartburn - February 2021
#
# Connects to focusServer.py
import tkinter as tk
from tkinter import ttk
import time
from threading import Thread
import socket

# Create window
window = tk.Tk()

# Connection defaults
#server = "127.0.0.1"
server = "astropi.local"
port = "3030"
connected=False

# Element padding
px=2
py=2

# Variables for networking
svrSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Tracking position changes
lastPoll=0      # Time of pass poll
pollInt=1

######## Functions ################
def appQuit():
    print("Quitting")
    global vQuit
    vQuit=True
    exit(0)

def toggleConnect():
    # Connects or disconnects from the network
    global svrSock

    print("Toggling connect")
    if connected==False:
        # Assume input is sensible
        server=svr_entry.get()
        port=port_entry.get()
        addr = (server, int(port))
        print("Attempting to connect to", addr)
        status_lbl_indicator['text']="Connecting"
        try:
            svrSock.connect(addr)
        except socket.error as msg:
            print("Error connecting ", msg)
            # Set status message in display
            status_lbl_indicator['text']=msg
            return

        if(svrSock):
            print("Connected")
            showConnected(True)
        else:
            print("Failed to connect")
    else:
        # Are connected, disconnect
        svrSock.close()
        # Reinit socket for next connect
        svrSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        showConnected(False)
        print("Disconnected")
# End of toggleConnect

def showConnected(s):
    # Changes the display to show we are connected, depending on the true
    # or false status of s
    global connected

    if(s):
        connected=True
        #print("showing connected")
        status_lbl_indicator['text']="Connected"
        connect_btn['text']="Disconnect"
        ACWbutton.state(["!disabled"])
        CWbutton.state(["!disabled"])
        ACW_nudge_btn.state(["!disabled"])
        CW_nudge_btn.state(["!disabled"])
        get_pos_btn.state(["!disabled"])
        stop_btn.state(["!disabled"])
        sp_up_btn.state(["!disabled"])
        sp_down_btn.state(["!disabled"])
        # Get position and speed
        sendCmd("GPOS")
        sendCmd("GSPD")
    else:
        connected=False
        #print("showing disconnected")
        status_lbl_indicator['text']="Disconnected"
        connect_btn['text']="Connect"
        ACWbutton.state(["disabled"])
        CWbutton.state(["disabled"])
        ACW_nudge_btn.state(["disabled"])
        CW_nudge_btn.state(["disabled"])
        get_pos_btn.state(["disabled"])
        stop_btn.state(["disabled"])
        sp_up_btn.state(["disabled"])
        sp_down_btn.state(["disabled"])

# End of showConnected

def sendCmd(cmd):
    # Send a command and process the results
    global lastPoll, pollInt
    #print("Sending command", cmd)
    toSend=cmd.encode('UTF-8')
    svrSock.sendall(toSend)
    data = svrSock.recv(1024)
    #print("Received", data)
    # Convert the data received to string. Should not fail, but abandon if it does
    try:
        rtnMsg = data.decode('UTF-8').strip()
    except:
        print("Unable to decode return data ", data)
        return None

    # We know we are active, kick the polling timer
    lastPoll=time.time()

    # Check the return message
    if(rtnMsg=="ACK"):
        # Fine, nothing to do
        return None
    elif(rtnMsg=="ERRCMD"):
        print("Error: We sent an invalid command")
        return None
    else:
        # Got something to process
        sp=rtnMsg.split('=')
        if(sp[0]=="pos"):
            showPos(sp[1])
            return sp[1]
        elif(sp[0]=="speed"):
            showSpeed(sp[1])
            return sp[1]
# End of sendCmd

def showPos(posStr):
    # Show the position
    posLabel["text"]=posStr

def showSpeed(spdStr):
    # Show the speed
    speedLabel["text"]=spdStr

def posPoller() :
    # Polling loop to keep the position counter updated
    # Will run in a thread while tkinter mainloop is running
    global lastPoll, pollInt
    while vQuit==False:
        # Don't do anything if not connected
        if(connected):
            # Time to poll?
            if(time.time() > (lastPoll+pollInt)):
                sendCmd("GPOS")
                sendCmd("GSPD")
        time.sleep(0.2) # Don't need to hammer CPU
# End of pos poller

# ############ Window layout ########################
s=ttk.Style()
s.theme_names()
s.theme_use('clam')
# Colours
# Guide - high emphasis 87%, medium 60%, disabled=38%
frameBg="#282c34"
windowBg="#21252b"
#buttonBg="#860100"
buttonBg="#bb86fc"
buttonFg=frameBg
buttonBgDisabled=frameBg
buttonBgActive="#3700b3"
fgCol="#abb2bf"
dataBg="#202945"

s.configure('Dark.TFrame', background=frameBg)
s.configure('Dark.TButton', foreground=buttonFg, background=buttonBg, relief='flat', font=('Helvetica Bold', 14))
s.map("Dark.TButton",
    foreground=[('pressed', 'red'), ('active', 'white'), ('disabled', '#be8d60')],
    background=[('pressed', '!disabled', windowBg), ('active', buttonBgActive), ('disabled', windowBg)]
    )
s.configure('DarkIcon.TButton', foreground=buttonFg, background=windowBg, relief='flat')
s.map("DarkIcon.TButton",
    foreground=[('pressed', 'red'), ('active', 'white'), ('disabled', '#be8d60')],
    background=[('pressed', '!disabled', windowBg), ('active', buttonBgActive), ('disabled', frameBg)]
    )
s.configure('Dark.TLabel', background=frameBg, foreground=fgCol)
s.configure('Dark.TEntry', background=windowBg, foreground=fgCol, fieldbackground=buttonBgActive)
s.configure('Data.TLabel', background=dataBg, font=("Helvetica Bold", 18), foreground='white',
  anchor="center", padding=(0,28,0,28))
  # the padding gives a nicer display

window.title("Focus Control")
window["bg"]=windowBg

# Title label
title_lbl = ttk.Label(
    text="Focus Control",
)
title_lbl.configure(background=windowBg, font=('Helvetica', 18), foreground=fgCol)
title_lbl.pack()

# Connection frame
conFrame = ttk.Frame(
    style='Dark.TFrame'
)
svr_lbl = ttk.Label(
    style="Dark.TLabel",
    master=conFrame,
    text="Server:"
)
svr_entry = ttk.Entry(
    style="Dark.TEntry",
    master=conFrame,
)
svr_entry.insert(0, server)
port_lbl = ttk.Label(
    style="Dark.TLabel",
    master=conFrame,
    text="Port:"
)
port_entry = ttk.Entry(
    style="Dark.TEntry",
    master=conFrame,
)
port_entry.insert(0, port)
status_lbl = ttk.Label(
    style="Dark.TLabel",
    master=conFrame,
    text="Status:"
)
status_lbl_indicator = ttk.Label(
    style="Dark.TLabel",
    master=conFrame,
    text="Disconnected"
)
connect_btn = ttk.Button(
    master=conFrame,
    text="Connect",
    style='Dark.TButton',
    command=toggleConnect
)
svr_lbl.grid(row=0,column=0,padx=px, pady=py)
svr_entry.grid(row=0,column=1,padx=px, pady=py)
port_lbl.grid(row=1,column=0,padx=px, pady=py)
port_entry.grid(row=1,column=1,padx=px, pady=py)
status_lbl.grid(row=2,column=0,padx=px, pady=py)
status_lbl_indicator.grid(row=2,column=1,padx=px, pady=py)
connect_btn.grid(row=3, column=1, padx=px, pady=py)
conFrame.pack(fill=tk.X, padx=3, pady=3)

# Define position frame
posFrame = ttk.Frame(
        style='Dark.TFrame'
)
acwIcon = tk.PhotoImage(file="FCicons/acw_48x48.png")
ACWbutton = ttk.Button(
    style='DarkIcon.TButton',
    master=posFrame,
#    text="<",
    width=5,
    state="disabled",
    image=acwIcon,
    command= lambda arg="ACW" : sendCmd(arg)
)
posLabel = ttk.Label(
    master=posFrame,
    text="",
    width=10,
    style='Data.TLabel',
)
cwIcon = tk.PhotoImage(file="FCicons/cw_48x48.png")
CWbutton = ttk.Button(
    style='DarkIcon.TButton',
    master=posFrame,
#    text=">",
    image=cwIcon,
    width=5,
    state="disabled",
    command= lambda arga="CW" : sendCmd(arga)
)
#ACWbutton.pack(side=tk.LEFT)
#posLabel.pack(side=tk.LEFT)
#CWbutton.pack(side=tk.LEFT)
ACWbutton.grid(row=0, column=0,padx=px, pady=py)
posLabel.grid(row=0, column=1,padx=px, pady=py)
CWbutton.grid(row=0, column=2,padx=px, pady=py)

stopIcon = tk.PhotoImage(file="FCicons/stop_48x48.png")
stop_btn = ttk.Button(
    style='DarkIcon.TButton',
    master=posFrame,
#    text=">",
    image=stopIcon,
    width=5,
    state="disabled",
    command= lambda arga="STOP" : sendCmd(arga)
)
stop_btn.grid(row=1, column=1, padx=px, pady=py)

acwNIcon = tk.PhotoImage(file="FCicons/acw_nudge_48x48.png")
ACW_nudge_btn = ttk.Button(
    style='DarkIcon.TButton',
    master=posFrame,
#    text="<|",
    width=5,
    state="disabled",
    image=acwNIcon,
    command= lambda arg="SSA" : sendCmd(arg)
)
get_pos_btn = ttk.Button(
    style='Dark.TButton',
    master=posFrame,
    text="Get Position",
    width=10,
    state="disabled",
    command= lambda arg="GPOS" : sendCmd(arg)
)
cwNIcon = tk.PhotoImage(file="FCicons/cw_nudge_48x48.png")
CW_nudge_btn = ttk.Button(
    style='DarkIcon.TButton',
    master=posFrame,
#    text="|>",
    width=5,
    state="disabled",
    image=cwNIcon,
    command= lambda arg="SSC" : sendCmd(arg)
)
ACW_nudge_btn.grid(row=2, column=0,padx=px, pady=py)
get_pos_btn.grid(row=2, column=1,padx=px, pady=py)
CW_nudge_btn.grid(row=2, column=2,padx=px, pady=py)

# Define speed icons
upIcon = tk.PhotoImage(file="FCicons/up_arr_48x48.png")
sp_up_btn = ttk.Button(
    style='DarkIcon.TButton',
    master=posFrame,
#    text="U",
    width=5,
    state="disabled",
    image=upIcon,
    command= lambda arg="SPU" : sendCmd(arg)
)
speedLabel = ttk.Label(
    master=posFrame,
    text="",
    width=10,
    style='Data.TLabel',
    justify='center',
)
downIcon = tk.PhotoImage(file="FCicons/down_arr_48x48.png")
sp_down_btn = ttk.Button(
    style='DarkIcon.TButton',
    master=posFrame,
#    text="D",
    width=5,
    state="disabled",
    image=downIcon,
    command= lambda arg="SPD" : sendCmd(arg)
)
sp_up_btn.grid(row=3, column=0,padx=px, pady=py)
speedLabel.grid(row=3, column=1,padx=px, pady=py)
sp_down_btn.grid(row=3, column=2,padx=px, pady=py)

quit_btn = ttk.Button(
    style='Dark.TButton',
    master=posFrame,
    text="Quit",
    width=5,
    command=appQuit
)
quit_btn.grid(row=4, column=1,padx=px, pady=py)
posFrame.pack(fill=tk.X, padx=3, pady=3)

######### End of window layout ###############


# Start the tkinter main loop in its own thread so that we can poll
# position
vQuit=False         # Used to tell poller to die
pollThread = Thread(target=posPoller)
pollThread.start()

window.mainloop()
# Code should not execute beyond this point
