from PIL import Image
from PIL import ImageGrab
import tkinter as tk
from tkinter import colorchooser
import serial
import time

# -----------------------------------------

# PC SIDE TILE CONTROL SOFTWARE
# TAMUhack 2021

# Written by Harrison Potter

# -----------------------------------------



def send_to_bt(rgb_str):
    print(rgb_str)
    bluetooth.write(str.encode(rgb_str) + b"\n")#These need to be bytes not unicode, plus a number


# -------- Housekeeping Functions ---------

# Converts a tuple containing RGB values to hexidecimal
def rgb_to_hex(rgb):
    r, g, b = rgb
    r = int(r)
    g = int(g)
    b = int(b)
    return f'#{r:02x}{g:02x}{b:02x}'

# Converts a tuple containing RGB values to a 9 character string
def rgb_to_str(rgb):
    r, g, b = rgb
    r = int(r)
    g = int(g)
    b = int(b)
    return (add_leading_zeros(r) + add_leading_zeros(g) + add_leading_zeros(b))
    
# FOR THE rgb_to_str() FUNCTION
# Converts an int to a 3 character string with leading zeros    
def add_leading_zeros(number):
    if int(number / 10) == 0 :
        return ("00" + str(number))
    elif int(number / 100) == 0:
        return ("0" + str(number))
    else:
        return str(number)



# -------- GUI Reaction Functions ---------

def toggle_active():
    # Kill currently running loops
    if button_rainbowAnimation.config('relief')[-1] == 'sunken':
        button_rainbowAnimation.config(relief="raised")
    
    if button_active.config('relief')[-1] == 'sunken':
        button_active.config(relief="raised")
    else:
        button_active.config(relief="sunken")

def toggle_rainbow():
    # Kill currently running loops
    if button_active.config('relief')[-1] == 'sunken':
        button_active.config(relief="raised")

    if button_rainbowAnimation.config('relief')[-1] == 'sunken':
        button_rainbowAnimation.config(relief="raised")
    else:
        button_rainbowAnimation.config(relief="sunken")
        send_to_bt("a1")
        update_prev((255, 255, 255))

def open_select():
    # Kill currently running loops
    if button_rainbowAnimation.config('relief')[-1] == 'sunken':
        button_rainbowAnimation.config(relief="raised")
    if button_active.config('relief')[-1] == 'sunken':
        button_active.config(relief="raised")

    color_code = colorchooser.askcolor(title ="Choose color")
    rgb_final_select = color_code[0]
    send_to_bt(rgb_to_str(rgb_final_select))
    update_prev(rgb_final_select)

# Updates the GUI backgroud with the current color
def update_prev(rgb):
    window.config(background = rgb_to_hex(rgb))



# -------- Active Color Detection ---------

# Actively determines the primary color shown on screen
def send_rep_color():
    screenshot = ImageGrab.grab()
    screenshot = screenshot.resize((20, 20))

    r_total = 0 
    g_total = 0 
    b_total = 0
    count = 0

    for x in range(5, 7):
        for y in range(3, 5):
            r_val, g_val, b_val = screenshot.getpixel((x,y))
            r_total += r_val
            g_total += g_val
            b_total += b_val
            count += 1

    final_rgb_active = (r_total/count, g_total/count, b_total/count)
    send_to_bt(rgb_to_str(final_rgb_active))
    update_prev(final_rgb_active)



# -------- GUI CODE ---------

window = tk.Tk()
window.title("Tile Control Suite")
window.columnconfigure([0, 1], minsize=150)
window.rowconfigure([0, 1, 2], minsize=80)

label_bt = tk.Label(
    text="Waiting for Connection",
    width=37,
    height=2
)
button_active = tk.Button(
    text="Reflect Screen",
    width=15,
    height=3,
    relief="raised",
    command=toggle_active
)
button_select = tk.Button(
    text="Select Specific Color",
    width=15,
    height=3,
    command=open_select
)
button_rainbowAnimation = tk.Button(
    text="Rainbow Animation",
    width=37,
    height=3,
    relief="raised",
    command=toggle_rainbow
)

label_bt.grid(row=0, column=0, columnspan = 2)
button_active.grid(row=1, column=0)
button_select.grid(row=1, column=1)
button_rainbowAnimation.grid(row=2, column=0, columnspan = 2)

port="com4" 
bluetooth=serial.Serial(port, 115200)
label_bt.config(text="Connected!")

while True:
    window.update()
    if (button_active.config('relief')[-1] == 'sunken'):
        window.after(100, send_rep_color())