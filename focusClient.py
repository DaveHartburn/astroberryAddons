# Python tkinter test
import tkinter as tk
from tkinter import ttk

# Create window
window = tk.Tk()

# Connection defaults
server = "127.0.0.1"
port = "3030"

# Variables to display
fpos=-1024
fspeed=50

# Element padding
px=5
py=5

######## Functions ################
def appQuit():
    global vQuit
    print("Quitting")
    vQuit=True
    exit(0)

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
    style='Dark.TButton'
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
    image=acwIcon
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
    state="disabled"
)
#ACWbutton.pack(side=tk.LEFT)
#posLabel.pack(side=tk.LEFT)
#CWbutton.pack(side=tk.LEFT)
ACWbutton.grid(row=0, column=0,padx=px, pady=py)
posLabel.grid(row=0, column=1,padx=px, pady=py)
CWbutton.grid(row=0, column=2,padx=px, pady=py)

acwNIcon = tk.PhotoImage(file="FCicons/acw_nudge_48x48.png")
ACW_nudge_btn = ttk.Button(
    style='DarkIcon.TButton',
    master=posFrame,
#    text="<|",
    width=5,
    state="disabled",
    image=acwNIcon,
)
get_pos_btn = ttk.Button(
    style='Dark.TButton',
    master=posFrame,
    text="Get Position",
    width=10,
    state="disabled"
)
cwNIcon = tk.PhotoImage(file="FCicons/cw_nudge_48x48.png")
CW_nudge_btn = ttk.Button(
    style='DarkIcon.TButton',
    master=posFrame,
#    text="|>",
    width=5,
    state="disabled",
    image=cwNIcon
)
ACW_nudge_btn.grid(row=1, column=0,padx=px, pady=py)
get_pos_btn.grid(row=1, column=1,padx=px, pady=py)
CW_nudge_btn.grid(row=1, column=2,padx=px, pady=py)

# Define speed icons
upIcon = tk.PhotoImage(file="FCicons/up_arr_48x48.png")
sp_up_btn = ttk.Button(
    style='DarkIcon.TButton',
    master=posFrame,
#    text="U",
    width=5,
    state="disabled",
    image=upIcon
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
)
sp_up_btn.grid(row=2, column=0,padx=px, pady=py)
speedLabel.grid(row=2, column=1,padx=px, pady=py)
sp_down_btn.grid(row=2, column=2,padx=px, pady=py)

quit_btn = ttk.Button(
    style='Dark.TButton',
    master=posFrame,
    text="Quit",
    width=5,
    command=appQuit
)
quit_btn.grid(row=3, column=1,padx=px, pady=py)
posFrame.pack(fill=tk.X, padx=3, pady=3)

######### End of window layout ###############


# Start the main loop
window.mainloop()

vQuit == False
while vQuit == False:
    # Check for window events
    pass

print("Exiting")
