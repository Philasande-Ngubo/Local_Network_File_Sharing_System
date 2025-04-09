import tkinter as GUI
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk
import aClient as Client
import threading
import time

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

frame = None 
bg =  None 
bg_frame = None
inner_container = None
NAME = "Noobie"
TRACKER = "BOOM"
txt_down_status = None
progDown = None
inner_frame = None
curFile = None
global msg_box

def setParams(tra, name):
    global TRACKER
    global NAME
    TRACKER = tra
    NAME = name


def messagebox( message):
    
    global msg_box
    msg_box = GUI.Toplevel(frame)
 
    midx = int((frame.winfo_screenwidth() -300 ) /2)
    midy = int ((frame.winfo_screenheight() - 150) /2)
    msg_box.geometry ("300x150+"+str(midx)+"+"+str(midy))
    msg_box.resizable(False, False)
    
    msg_box.configure(background=CHARCOAL_BLACK )
    # Centering the window on screen
    msg_box.overrideredirect(True)

    GUI.Label(msg_box, text=message, fg = SOFT_WHITE, font=("Segoe UI", 13), bg = DARK_BLUE, padx=10, pady=10).pack(pady=10)

    # Close button
    GUI.Button(msg_box, text="Seeder", command=toSeeder).pack(pady=10)
    GUI.Button(msg_box, text="Exit", command=close_window).pack(pady=10)

    msg_box.transient(frame)  # Keep on top
    msg_box.grab_set()  # Make modal
    frame.wait_window(msg_box)  # Wait for user to close


def chose():       # After the client chose a file to download
    files = Client.outFile() 
    
    for item in inner_frame.winfo_children():
        item.destroy()
        
    for file in files:
        frame_s = GUI.Frame(inner_frame, width = 710, height= 40, bd=2,bg = SOFT_WHITE, relief=GUI.RIDGE)
        frame_s.pack(pady=5, padx=10, fill="x")
        
        lbl = GUI.Label(frame_s, text = file,font=("Segoe UI", 14), bg =SOFT_WHITE , fg = DARK_BLUE, bd =0)
        lbl.place(x = 20, y = 5)

def toSeeder():
    msg_box.destroy()
    frame.destroy()
    import Seeder as Seed
    Seed.setParams(TRACKER,NAME)
    Seed.init()
    

def prog():                         # deals with the progress bar
    while Client.totSize() ==0 :
        pass
    while  Client.totSize() > Client.progress():
        progDown['value'] = int (100*( Client.progress()/ Client.totSize()))
        frame.update_idletasks() 
    
    txt_down_status.configure(text = "Succesfully downloaded "+curFile)
    messagebox( "Become a Seeder or Exit")
        
        
def download_pressed(event, file, i):        
    chose()
    global curFile
    curFile = file
    global txt_down_status
    txt_down_status.configure(text = "downloading "+file)
    threading.Thread(target = prog).start()
    Client.setIndex(i+1)
    
    
    
def close_window():
    frame.destroy()
    exit(0)

def move_window(event):
    frame.geometry(f'+{event.x_root}+{event.y_root}')

def minimize_window():
    frame.lower()

def create_smooth_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, fill="white", outline="black", outline_width=2): #Draws rounded canva for styling the buttons
    width = x2 - x1
    height = y2 - y1

    # Create a transparent image with anti-aliasing
    img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Draw a rounded rectangle with anti-aliasing
    draw.rounded_rectangle((0, 0, width, height), radius=radius, fill=fill, outline=outline, width=outline_width)

    # Convert to Tkinter format
    tk_img = ImageTk.PhotoImage(img)
    
    # Place it on the canvas
    img_id = canvas.create_image(x1, y1, anchor="nw", image=tk_img)
    
    # Prevent garbage collection
    canvas.image = tk_img  

    return img_id

def startClient():
    
    Client.go(TRACKER.strip(), NAME, "b")

    
def update_scroll_bar(event):
    inner_container.configure(scrollregion=inner_container.bbox("all"))
    
def init():
    global frame
    frame  = GUI.Tk()
    
    threading.Thread(target = startClient , daemon = True).start()
    
    midx = int((frame.winfo_screenwidth() -800 ) /2)
    midy = int ((frame.winfo_screenheight() - 700) /2)
    frame.geometry ("800x700+"+str(midx)+"+"+str(midy))
    frame.resizable(False, False)
    frame.configure(background=DARK_BLUE)
    
    global bg 
    bg = GUI.PhotoImage(file="assets/client.png")
    
    global bg_frame
    bg_frame = GUI.Label(frame, image=bg, bd=0, highlightthickness=0)
    bg_frame.place( y =0)
    
    #Remove TitleBar
    frame.overrideredirect(True)
    
    
    # Custom titleBar
    title_bar = GUI.Frame(bg_frame, bg= DARK_BLUE , relief='flat', width = 800, height =30)
    title_bar.place( x= 0, y =0)

    #close Button on Custom title bar
    close_button = GUI.Button(title_bar, text='⛌', command=close_window, bg= DARK_BLUE, fg= SOFT_WHITE, activebackground=WARNING_ORANGE ,relief='flat')
    close_button.place( y = 5, x=770)
    
    minimize_button = GUI.Button(title_bar, text='—', command=minimize_window, bg= DARK_BLUE, fg=SOFT_WHITE, activebackground='white' ,relief='flat')
    minimize_button.place( y = 5, x=745)
    
    title = GUI.Label(bg_frame, text = "NeighbourShare",font=("Segoe UI", 23,"bold"), bg = DARK_BLUE, fg = '#767E83', bd =0 )
    title.place(x= 40, y =8)
    
    title_c = GUI.Label(bg_frame, text = "Available Files",font=("Courier", 18), bg = DARK_BLUE, fg = '#767E83', bd =0 )
    title_c.place(x= 290, y =80)
    
    
    # Files_bar
    container = GUI.Frame(width = 720, height = 380, bg = DARK_BLUE,bd =0,highlightthickness=0)
    container.place(x= 40, y = 120)
    
    global inner_container
    inner_container = GUI.Canvas(container,width = 710, height = 380, bg = DARK_BLUE,bd =0,highlightthickness=0 )
    inner_container.pack(side="left", fill="both", expand=True)
    
    scrollbar = GUI.Scrollbar(container, orient=GUI.VERTICAL, command=inner_container.yview)
    scrollbar.pack(side=GUI.RIGHT, fill=GUI.Y)
    inner_container.configure(yscrollcommand=scrollbar.set)
    
    global inner_frame
    inner_frame = GUI.Frame(inner_container, bg = DARK_BLUE,bd =0,highlightthickness=0)
    canvas_window = inner_container.create_window((0, 0), window=inner_frame, anchor="nw")
        
    files = Client.outFile()
    
    for file in files:                                                                          #Loads the Available  files
        frame_s = GUI.Frame(inner_frame, width = 710, height= 40, bd=2,bg = SOFT_WHITE, relief=GUI.RIDGE)
        frame_s.pack(pady=5, padx=10, fill="x")
        
        lbl = GUI.Label(frame_s, text = file,font=("Segoe UI", 14), bg =SOFT_WHITE , fg = DARK_BLUE, bd =0)
        lbl.place(x = 20, y = 5)
        
        btn_Canva = GUI.Canvas(frame_s, width=50, height=20, bg= DARK_BLUE, highlightthickness=0 )
        btn_Canva.place(x= 615, y = 1 )
        
        down_button = GUI.Button(frame_s, text = "Download",font=("Segoe UI", 10), bg = DEEP_GRAY, fg = SOFT_WHITE, bd =0 )
        down_button.place(x = 620, y = 5)
        down_button.bind("<Button-1>", lambda event,file=file, i = files.index(file): download_pressed(event, file,i))

        
        
    container_downloads = GUI.Frame(width = 720, height = 130,bd=2, bg =DARK_BLUE ,relief=GUI.RIDGE)
    container_downloads.place(x= 50, y = 520)
    
    global txt_down_status
    txt_down_status = GUI.Label(container_downloads, text = "No active downloads",font=("Segoe UI", 11), bg = DARK_BLUE, fg = '#767E83', bd =0 )
    txt_down_status.place(x= 8, y = 5)
    
    global progDown
    progDown = ttk.Progressbar(container_downloads,length = 100,mode = 'determinate', )
    progDown.place(x = 10, y = 40 ,width=680)
    
    #Download Stats
    
    #events
    title_bar.bind('<B1-Motion>',move_window)
    inner_frame.bind("<Configure>", update_scroll_bar)
   
    frame.mainloop()