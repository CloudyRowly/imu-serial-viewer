import datetime
from decimal import Decimal
from decimal import InvalidOperation
import os
import pathlib
import sys
from ctypes import WinDLL
import customtkinter as ctk
import serial
from PIL import Image, ImageTk
from tkinter import Label
import argparse
import math
import threading

class Serial_Viewer(ctk.CTk):

    def __init__(self, serial_port, serial_baudrate):
        super().__init__()

        # Set app basic UI config
        self.title("1.0 - IMU Serial Viewer")
        self.geometry("300x300")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.wm_attributes("-transparentcolor", 'grey')
        
        # Set app icon
        if getattr(sys, 'frozen', False):  # Check if we're running as a PyInstaller bundle
            # We're running in a PyInstaller bundle
            self.base_dir = sys._MEIPASS
            # base_dir = os.path.dirname(sys.argv[0])
        else:
            # We're running in a normal Python environment
            self.base_dir = os.path.abspath(os.path.join(pathlib.Path(__file__).parent.resolve(), 'assets'))
        icon_path = os.path.join(self.base_dir, 'icon.ico')
        self.iconbitmap(icon_path)
        
        # Basic parameters and initializations
        # Supported modes : Light, Dark, System
        ctk.set_appearance_mode("System")
        # Supported themes : green, dark-blue, blue
        ctk.set_default_color_theme("dark-blue")

        #serial setup
        self.serial = serial.Serial(serial_port, serial_baudrate)

        #arrow image setup
        self.arrow_size = 100

        self.arrow_dark = Image.open(os.path.join(self.base_dir, "arrow_dark.png"))
        self.arrow_dark = self.arrow_dark.rotate(45, expand=True)

        self.arrow_light = Image.open(os.path.join(self.base_dir, "arrow_light.png"))
        self.arrow_light = self.arrow_light.rotate(45, expand=True)

        # compass image setup
        self.compass_dark = Image.open(os.path.join(self.base_dir, "compass_dark.png"))
        self.compass_light = Image.open(os.path.join(self.base_dir, "compass_light.png"))
        self.compass_scale = math.sqrt(2 * pow(self.arrow_size, 2)) / self.arrow_size
        self.compass_size = int(self.arrow_size * self.compass_scale) + 100

        # Setup ui
        self.setup_ui()
        self.heading = 0
        
        self.loop()


    def loop(self):      
        temp_heading = self.serial.readline().decode().strip()
        if(len(temp_heading) > 0):
            if temp_heading[0] == 'H' and temp_heading[1:4].isdigit():
                self.heading = int(temp_heading[1:])
        
        img_dark = self.arrow_dark.rotate(self.heading, expand=False)
        img_light = self.arrow_light.rotate(self.heading, expand=False)
        img_obj = ctk.CTkImage(light_image = img_light, dark_image = img_dark,
                           size=(self.arrow_size, self.arrow_size))
        self.image_label.configure(image=img_obj)

        self.label_heading.configure(text = str(self.heading))
        #self.heading += 1

        self.after(10, self.loop)


    def setup_ui(self):
        self.frame = ctk.CTkFrame(self)
        self.frame.grid(padx = 5, pady = 5, sticky="nsew")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=2)
        self.frame.rowconfigure(0, weight=1)

        img = ctk.CTkImage(light_image=self.compass_light, dark_image = self.compass_dark,
                           size=(self.compass_size, self.compass_size))
        self.compass_label = ctk.CTkLabel(self.frame, width = self.compass_size, height = self.compass_size, image=img, text="", fg_color = "transparent")
        self.compass_label.grid(row=0)

        img = ctk.CTkImage(light_image=self.arrow_light, dark_image = self.arrow_dark,
                           size=(self.arrow_size, self.arrow_size))
        self.image_label = ctk.CTkLabel(self.frame, width = self.arrow_size, height = self.arrow_size, image=img, text="", fg_color = "transparent", bg_color = "transparent")  # display image with a CTkLabel
        self.image_label.grid(row=0)

        self.label_heading = ctk.CTkLabel(self.frame, text = "0", font = ("Arial Rounded MT Bold", 50), fg_color = "transparent")
        self.label_heading.grid(row = 1)


    def on_closing(self):
        self.destroy()


baudrate = 115200
com_port = "COM3"

arg_parser = argparse.ArgumentParser(description="IMU heading visualiser")
arg_parser.add_argument("-p", "--com", type=str, help="COM port to listen to serial")
arg_parser.add_argument("-r", "--baudrate", type=int, help="Serial baud rate")

def parse_args():
    global baudrate, com_port
    args = arg_parser.parse_args()
    if args.com:
        com_port = args.com
    if args.baudrate:
        baudrate = args.baudrate

if __name__ == "__main__":
    parse_args()
    app = Serial_Viewer(com_port, baudrate)
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()