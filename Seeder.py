import tkinter as GUI
from PIL import Image, ImageDraw, ImageTk
import aClient as Client
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

frame = None 
bg =  None 
bg_frame = None
inner_container = None

NAME = "Noobie"
TRACKER = "BOOM"



test_files = [
    ("The Dark Knight Rises.mp4", 15),
    ("Vacation_Sunset.png", 0),
    ("Drake_OneDance.mp3", 12),
    ("Inception.mkv", 0),
    ("Annual_Report_2024.pdf", 9),
    ("Billie_Eilish_Bad_Guy.mp3", 10),
    ("Wedding_Photo.jpg", 0),
    ("Wildlife_Documentary.mp4", 0),
    ("Business_Proposal.pdf", 3),
    ("Pop_Stars_Album.wav", 8),
    ("Meeting_Notes.txt", 6),
    ("Quarterly_Presentation.pptx", 1),
    ("Nature_Landscape.gif", 5),
    ("Python_Script.py", 13),
    ("Software_Installer.zip", 15),
    ("Project_Report.docx", 14),
    ("Action_Movie_Clip.mp4", 0),
    ("Best_Seller_Ebook.epub", 4),
    ("Game_Backup.rar", 7),
    ("Personal_Backup.tar", 9),
    ("Homepage_Design.html", 3)
]

def setParams(tra, name):
    global TRACKER
    global NAME
    TRACKER = tra
    NAME = name
    
def close_window():
    frame.destroy()
    exit(0)
    
def move_window(event):
    frame.geometry(f'+{event.x_root}+{event.y_root}')

def minimize_window():
    frame.lower()

def create_smooth_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, fill="white", outline="black", outline_width=2):
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
    
def update_scroll_bar(event):
    inner_container.configure(scrollregion=inner_container.bbox("all"))

def startClient():
    print(TRACKER)
    Client.go(TRACKER.strip(), NAME, "a")
       
def init():
    global frame
    frame  = GUI.Tk()
    threading.Thread(target = startClient).start()
   
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
    
    title_c = GUI.Label(bg_frame, text = "Files you are seeding",font=("Courier", 18), bg = DARK_BLUE, fg = '#767E83', bd =0 )
    title_c.place(x= 270, y =80)

    #close Button on Custom title bar
    close_button = GUI.Button(title_bar, text='⛌', command=close_window, bg= DARK_BLUE, fg= SOFT_WHITE, activebackground=WARNING_ORANGE ,relief='flat')
    close_button.place( y = 5, x=770)
    
    minimize_button = GUI.Button(title_bar, text='—', command=minimize_window, bg= DARK_BLUE, fg=SOFT_WHITE, activebackground='white' ,relief='flat')
    minimize_button.place( y = 5, x=745)
    
    title = GUI.Label(bg_frame, text = "NeighbourShare",font=("Segoe UI", 23,"bold"), bg = DARK_BLUE, fg = '#767E83', bd =0 )
    title.place(x= 40, y =8)
    
    
    # Files_bar
    container = GUI.Frame(width = 720, height = 380, bg = DARK_BLUE,bd =0,highlightthickness=0)
    container.place(x= 40, y = 120)
    
    global inner_container
    inner_container = GUI.Canvas(container,width = 710, height = 380, bg = DARK_BLUE,bd =0,highlightthickness=0 )
    inner_container.pack(side="left", fill="both", expand=True)
    
    scrollbar = GUI.Scrollbar(container, orient=GUI.VERTICAL, command=inner_container.yview)
    scrollbar.pack(side=GUI.RIGHT, fill=GUI.Y)
    inner_container.configure(yscrollcommand=scrollbar.set)
    
    inner_frame = GUI.Frame(inner_container, bg = DARK_BLUE,bd =0,highlightthickness=0)
    canvas_window = inner_container.create_window((0, 0), window=inner_frame, anchor="nw")
    
    for file in Client.getFiles():
        frame_s = GUI.Frame(inner_frame, width = 710, height= 40, bd=2,bg = SOFT_WHITE, relief=GUI.RIDGE)
        frame_s.pack(pady=5, padx=10, fill="x")
        
        lbl = GUI.Label(frame_s, text = file,font=("Segoe UI", 14), bg =SOFT_WHITE , fg = DARK_BLUE, bd =0)
        lbl.place(x = 20, y = 5)
        
        
        
    #Download Stats
   
    
    
    #events
    title_bar.bind('<B1-Motion>',move_window)
    inner_frame.bind("<Configure>", update_scroll_bar)
   
    frame.mainloop()
