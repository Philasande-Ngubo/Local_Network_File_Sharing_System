import tkinter as GUI
import socket
import subprocess
import re
import time
from tkinter import ttk
from matplotlib import font_manager
import aServer as Tracker_back
import Utils as Utils
import threading

#Primary colors
DARK_BLUE = "#0D1B2A"
CHARCOAL_BLACK  = "#1B263B"
DEEP_GRAY = "#415A77"

#ACCENT COLORS
NEON_CYAN = "#00FFFF"
ELECTRIC_BLUE = "#0096FF"
NEON_PURPLE = "#8A2BE2"

#TEXT_AND_ICONS
SOFT_WHITE = "#E0E1DD"
COOL_GRAY = "#A1A6B4"
BRIGHT_GREEN = "#39FF14"
WARNING_ORANGE = "#FF914D"

DNS = socket.getfqdn()
SEND_TIME = 1;
RECIEVE_TIME =1;
bg_frame = None

font_title = { 'weight': 'bold', 'size': 12,'color': COOL_GRAY}
font_labels = { 'weight': 'normal', 'size': 8, 'color' :COOL_GRAY}
font_ticks = {'family': 'DejaVu Sans', 'weight': 'light', 'size': 2}

frame = GUI.Tk()
bg = GUI.PhotoImage(file="assets/Frame.png")

lbls = []

pnl_Files = None
pnl_IPs = None
canvas_u = None


def close_window():
    frame.destroy()
    exit(0)

def numForm(num):
        return f"{num:02}"
        
def update_ui():       #Blinks the tracker in 2 seconds intervals to update the stats
    
    while True:
        time.sleep(2)
        for lbl in lbls:
            lbl.destroy()
        
        lbs = []
            
        for file in Tracker_back.fileList():
            label = GUI.Label(pnl_Files, text=file, width = 36 , font=("Courier", 13) ,bg =DEEP_GRAY, fg = SOFT_WHITE )
            label.pack(pady=5)
            lbls.append(label)
    
        pnl_Files.update_idletasks()
        canvas_u.config(scrollregion=canvas_u.bbox("all"))
        
        for ip in Tracker_back.names:
            label = GUI.Label(pnl_IPs, text=ip, width = 25 , font=("Courier", 13) ,bg =DEEP_GRAY, fg = SOFT_WHITE )
            label.pack(pady=5)
            lbls.append(label)
    
        pnl_IPs.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        test_files =[]
        
        lbl_Dev.configure(text=" "+numForm( len(Tracker_back.names))+" online\n Devices")
        lbl_files.configure(text=" "+numForm( len(Tracker_back.fileList()))+" available\n files")
   
        
def move_window(event):
    frame.geometry(f'+{event.x_root}+{event.y_root}')


    
def init():

    midx = int((frame.winfo_screenwidth() - 1078) /2)
    midy = int ((frame.winfo_screenheight() - 820) /2)
    frame.geometry ("1078x820+"+str(midx)+"+"+str(midy))
    frame.resizable(False, False)
    frame.configure(background=DARK_BLUE)

    #Remove TitleBar
    frame.overrideredirect(True)
    
    # Custom titleBar
    title_bar = GUI.Frame(frame, bg= DARK_BLUE , relief='flat', bd=2)
    title_bar.pack(fill=GUI.X)

    #close Button on Custom title bar
    close_button = GUI.Button(title_bar, text='⛌', command=close_window, bg= DARK_BLUE, fg='white', activebackground='red' ,relief='flat')
    close_button.pack(side= GUI.RIGHT, padx=5)

    #Adding Components
    global bg_frame
    bg_frame = GUI.Label(frame, image=bg, bd=0, highlightthickness=0)
    bg_frame.place( y =20)
    
    #Token
    lbl_Token = GUI.Label(bg_frame, text=" Token \n "+Utils.toCali(socket.gethostbyname(socket.gethostname())), font=("Trebuchet MS", 24, "bold"), fg= SOFT_WHITE , bg = DARK_BLUE )
    lbl_Token.place(x = 440, y = 15);
    
    global canvas_u
    #Files
    canvas_u = GUI.Canvas(width = 385, height = 480, bg = CHARCOAL_BLACK ,bd =0 ,highlightthickness=0)
    canvas_u.place(x = 50, y = 180)
    
    global pnl_Files
    pnl_Files = GUI.Frame(canvas_u, bg = CHARCOAL_BLACK, bd =0, highlightthickness=0)
    
    scrlbar_style_u = ttk.Style()
    scrlbar_style_u.theme_use("clam")
    scrlbar_style_u.configure("Vertical.TScrollbar", background= CHARCOAL_BLACK , troughcolor= DEEP_GRAY, bordercolor= CHARCOAL_BLACK, arrowcolor=DEEP_GRAY)
    
    scrollbar_u = GUI.ttk.Scrollbar(pnl_Files , orient="vertical", command=canvas_u.yview, style="Vertical.TScrollbar")
    
    canvas_u.create_window((0, 0), window=pnl_Files, anchor="nw")
    canvas_u.configure(yscrollcommand=scrollbar_u.set)
    
    scrollbar_u.pack(side="right", fill="y")
    
    for file in Tracker_back.fileList():
        label = GUI.Label(pnl_Files, text=file, width = 36 , font=("Courier", 13) ,bg =DEEP_GRAY, fg = SOFT_WHITE )
        label.pack(pady=5)
    
    pnl_Files.update_idletasks()
    canvas_u.config(scrollregion=canvas_u.bbox("all"))
    
    #Active downloads
    
    #Devices menu
    global canvas
    canvas = GUI.Canvas(width = 270, height = 198, bg = CHARCOAL_BLACK, bd =0 ,highlightthickness=0)
    canvas.place(x = 768, y = 180)
    
    global pnl_IPs
    pnl_IPs = GUI.Frame(canvas, bg = CHARCOAL_BLACK, bd =0, highlightthickness=0)
    
    scrlbar_style = ttk.Style()
    scrlbar_style.theme_use("clam")
    scrlbar_style.configure("Vertical.TScrollbar", background= CHARCOAL_BLACK , troughcolor= DEEP_GRAY, bordercolor= CHARCOAL_BLACK, arrowcolor=DEEP_GRAY)
    
    scrollbar = GUI.ttk.Scrollbar(pnl_IPs , orient="vertical", command=canvas.yview, style="Vertical.TScrollbar")
    
    canvas.create_window((0, 0), window=pnl_IPs, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    scrollbar.pack(side="right", fill="y")
    
    for ip in Tracker_back.names:
        label = GUI.Label(pnl_IPs, text= ip , width = 25 , font=("Courier", 13) ,bg =DEEP_GRAY, fg = SOFT_WHITE )
        label.pack(pady=5)
    
    pnl_IPs.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Footer Stats
    
    global lbl_files
    lbl_files = GUI.Label(bg_frame, text=" 00 available\n files" , font=("Courier", 10), fg= SOFT_WHITE , bg = DARK_BLUE )
    lbl_files.place(x = 523, y = 759);
    
    global lbl_Dev
    lbl_Dev = GUI.Label(bg_frame, text=" 00 online\n Devices" , font=("Courier", 10), fg= SOFT_WHITE , bg = DARK_BLUE )
    lbl_Dev.place(x = 660, y = 759);
    

    title_bar.bind('<B1-Motion>',move_window)

init()
threading.Thread(target = update_ui, daemon = True).start()
frame.mainloop()