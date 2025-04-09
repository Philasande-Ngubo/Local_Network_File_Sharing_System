import tkinter as GUI
from PIL import Image, ImageDraw, ImageTk
import Utils

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

tracker_var = None
share_var = None
lbl_Message = None

entry_Tracker = None
entry_share_name = None

selected_option = None


def close_window():
    frame.destroy()
    exit(0)

def move_window(event):
    frame.geometry(f'+{event.x_root}+{event.y_root}')

def minimize_window():
    frame.lower()
   
def btn_connect_clicked(event):
    
    if len(entry_Tracker.get())> 7:
        
        if ( len(entry_share_name.get()) > 4):
            if (Utils.isIP( entry_Tracker.get().strip().upper())):
                    client_name = entry_share_name.get()
                    tracker = Utils.toIP(entry_Tracker.get().strip().upper())

                    selected_option.get()
                    if selected_option.get() == 1:
                        frame.destroy()
                        import Seeder as Seed
                        Seed.setParams(tracker.strip(),client_name.strip())
                        Seed.init()
                        
                    else:
                        frame.destroy()
                        import Leecher as Seed
                        Seed.setParams(tracker.strip(),client_name.strip())
                        Seed.init()
                        
                        Seed.NAME = client_name
                        Seed.TRACKER = tracker
            else:
                lbl_Message.configure(text = "invalid token")
                
                
        else:
            lbl_Message.configure(text = "incomplete client Token")
    else:
        lbl_Message.configure(text = "incomplete token")
    
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

def on_text_change(*args):
    try:
        if len(entry_Tracker.get()) < 3:
            entry_Tracker.insert(0, " "*3+entry_Tracker.get().strip())
        
        if len(entry_share_name.get()) < 3:
            entry_share_name.insert(0, " "*3+entry_share_name.get().strip())
    except:
        pass
    
    

            
def init():
    global frame
    frame  = GUI.Tk()
    
    midx = int((frame.winfo_screenwidth() - 460) /2)
    midy = int ((frame.winfo_screenheight() - 480) /2)
    frame.geometry ("460x480+"+str(midx)+"+"+str(midy))
    frame.resizable(False, False)
    frame.configure(background=DARK_BLUE)
    
    global bg 
    bg = GUI.PhotoImage(file="assets/options.png")
    
    global bg_frame
    bg_frame = GUI.Label(frame, image=bg, bd=0, highlightthickness=0)
    bg_frame.place( y =0)
    
    #Remove TitleBar
    frame.overrideredirect(True)
    
    
    # Custom titleBar
    title_bar = GUI.Frame(bg_frame, bg= DARK_BLUE , relief='flat', width = 500, height =30)
    title_bar.place( x= 0, y =0)

    #close Button on Custom title bar
    close_button = GUI.Button(title_bar, text='⛌', command=close_window, bg= DARK_BLUE, fg= SOFT_WHITE, activebackground=WARNING_ORANGE ,relief='flat')
    close_button.place( y = 5, x=420)
    
    minimize_button = GUI.Button(title_bar, text='—', command=minimize_window, bg= DARK_BLUE, fg=SOFT_WHITE, activebackground='white' ,relief='flat')
    minimize_button.place( y = 5, x=390)
    
    global tracker_var
    global share_var
    
    tracker_var = GUI.StringVar()
    share_var = GUI.StringVar()
    
    tracker_var.trace_add("write", on_text_change)
    share_var.trace_add("write", on_text_change)
    #Adding components
    #Tracker Token
    
    prompt_Tracker = GUI.Label(bg_frame, text = "Enter Tracker Token:",font=("Segoe UI", 16), bg = DARK_BLUE, fg = SOFT_WHITE, bd =0 )
    prompt_Tracker.place(x= 40, y =100)
    
    tracker_canva = GUI.Canvas(bg_frame, width=400, height=50, bg= DARK_BLUE, highlightthickness=0 )
    tracker_canva.place(x= 40, y =130)
    
    create_smooth_rounded_rectangle(tracker_canva, 1, 4, 399, 45 , radius=8, fill= DEEP_GRAY, outline= DEEP_GRAY)
    
    global entry_Tracker
    entry_Tracker = GUI.Entry(bg_frame, width = 30, insertbackground=SOFT_WHITE, font=("Consolas", 18), bg = DEEP_GRAY, fg = SOFT_WHITE , bd =0 ,highlightthickness=0 ,textvariable =tracker_var)
    entry_Tracker.place(x= 46, y =140)
    entry_Tracker.insert(0, "   ")
    
    # ShareName
    prompt_Share_Name = GUI.Label(bg_frame, text = "Enter your ShareName:",font=("Segoe UI", 16), bg = DARK_BLUE, fg = SOFT_WHITE, bd =0 )
    prompt_Share_Name.place(x= 40, y =200)
    
    share_name_canva = GUI.Canvas(bg_frame, width=400, height=50, bg= DARK_BLUE, highlightthickness=0 )
    share_name_canva.place(x= 40, y =230)
    
    create_smooth_rounded_rectangle(share_name_canva, 1, 4, 399, 45 , radius=8, fill= DEEP_GRAY, outline= DEEP_GRAY)
    
    global entry_share_name
    entry_share_name = GUI.Entry(bg_frame, width = 30, insertbackground=SOFT_WHITE, font=("Consolas", 18), bg = DEEP_GRAY, fg = SOFT_WHITE , bd =0 ,highlightthickness=0 ,textvariable =share_var)
    entry_share_name.place(x= 46, y =240)
    entry_share_name.insert(0, "   ")
    
    #Role
    
    canva_role = GUI.Canvas(bg_frame, width=400, height=80, bg= DARK_BLUE, highlightthickness=1 )
    canva_role.place(x= 40, y =314)
    
    prompt_role = GUI.Label(bg_frame, text = "Choose your role",font=("Segoe UI", 16), bg = DARK_BLUE, fg = SOFT_WHITE, bd =0 )
    prompt_role.place(x= 50, y =300)
    
    global selected_option
    selected_option = GUI.IntVar(value=1)
    
    seeder_radio = GUI.Radiobutton(bg_frame, text="Seeder", value=1,variable=selected_option, bg=DARK_BLUE, fg=SOFT_WHITE , selectcolor=DARK_BLUE, font=("Segoe UI", 15))
    seeder_radio.place(x = 60, y = 330)
    
    leecher_radio = GUI.Radiobutton(bg_frame, text="Leecher",variable=selected_option, value=0, bg=DARK_BLUE, fg=SOFT_WHITE , selectcolor=DARK_BLUE, font=("Segoe UI", 15))
    leecher_radio.place(x = 180, y = 330)
                                
    #connect Button
    
    btn_Canva = GUI.Canvas(bg_frame, width=150, height=60, bg= DARK_BLUE, highlightthickness=0 )
    btn_Canva.place(x= 310, y = 410 )
    
    create_smooth_rounded_rectangle(btn_Canva, 8, 4, 133, 46 , radius=8, fill= ELECTRIC_BLUE, outline= SOFT_WHITE)
    
    btn_connect = GUI.Button(bg_frame, text = "Connect",font=("Consolas", 16), bg = ELECTRIC_BLUE, fg = DARK_BLUE, bd =0 )
    btn_connect.place(x = 330,y = 416)
    
    global lbl_Message
    lbl_Message = GUI.Label(bg_frame, text = "",font=("Segoe UI", 13,"italic"), bg = DARK_BLUE, fg = '#767E83', bd =0 )
    lbl_Message.place(x = 40, y= 405)
      
    #events
    title_bar.bind('<B1-Motion>',move_window)
    btn_connect.bind("<ButtonPress-1>", btn_connect_clicked)
    
   
    frame.mainloop()
init()