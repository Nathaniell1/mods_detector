import tkinter as tk
import pynput
import time
import winsound
import pygetwindow as gw
from tkinter import Tk
from pynput.keyboard import Key, Controller, Listener, KeyCode

keyboard = Controller()
time_pressed = time.time()

# open bad_mods.txt and save the lines to list
with open('bad_mods.txt') as f:
     bad_mods = f.readlines()

# convert mods to lower case and remove the new line character
for i, mod in enumerate(bad_mods):
    bad_mods[i] = mod.lower().strip('\n')

#########################################################


def process_item():
    
    # get item from the clippboard, convert to lower case
    try:
        item = str(Tk().clipboard_get()).lower()
    except:
        item = ""

    # tries to find any mod specified in bad_mods in the copied items' text
    if any(mod in item for mod in bad_mods):
        frequency = 500
        duration = 250
        # Make beep sound on Windows
        winsound.Beep(frequency, duration)

def process_key(key):
    # only work every 100 ms
    global time_pressed
    if (time.time() - time_pressed > 0.1):
        time_pressed = time.time()
    else:
        return
    
    #ignore key press when PoE is not the active window
    if gw.getActiveWindow().title != "Path of Exile":
        return

    if key == Key.shift_l:
        # press and release cltr+c to make copy of the item to clipboard
        keyboard.press(Key.ctrl_l)
        keyboard.press('c')
        keyboard.release('c')
        keyboard.release(Key.ctrl_l)
        # process the copied item
        process_item()
        
def start_mods_detector():
    global listener
    # Activate listener which will call process_key function every time key is pressed
    listener = Listener(on_press = process_key)
    listener.start()

def stop_mods_detector():
    listener.stop()

########################### ui part ##############################

root= tk.Tk()
canvas1 = tk.Canvas(root, width = 300, height = 300)
canvas1.pack()
running = False

def toggle_mod_detector():  
    global running

    label1 = tk.Label(root, text= 'Script is running!', fg='blue', font=('helvetica', 12, 'bold'))
    label2 = tk.Label(root, text= 'Script is stopped!', fg='blue', font=('helvetica', 12, 'bold'))
    canvas1.create_window(150, 200, window= label2 if running else label1)
   
    if running:
        stop_mods_detector()
    else:
        start_mods_detector()
    running = not running

def main():
    button1 = tk.Button(text='Toggle the script', command=toggle_mod_detector, bg='brown',fg='white')
    canvas1.create_window(150, 150, window=button1)
    root.title("Mod detector")
    root.mainloop()

if __name__ == "__main__":
    main()