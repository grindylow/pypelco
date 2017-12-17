#
# Graphical User Interface for Controlling a PELCO-D Camera Mount
#
# specifically this seems to work well with a 
#   https://www.aliexpress.com/item/Pan-Tilt-motorized-rotation-bracket-stand-holder-PELCO-D-control-for-CCTV-IP-camera-module-RS232/32827664380.html
#

import serial
import tkinter as tk
import tkinter.ttk
from pelco_mount import *

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        #self.init_mount()
        
    def init_mount(self,port="com4"):
        ser = serial.Serial(port,timeout=.1,baudrate=2400)
        print(ser)
        self.mount = pelco_mount(ser)

    def create_widgets(self):
    
        self.create_joystick()
        
        self.cb_port_label = tk.Label(self)
        self.cb_port_label["text"] = "COM-Port:"
        self.cb_port_label.grid(column=0,row=0)
        
        self.cb_port = tk.ttk.Combobox(self,values=["COM1","COM2","COM3","COM4","COM5"])
        self.cb_port.grid(column=1,row=0)

        self.b_connect = tk.Button(self)
        self.b_connect["text"] = "Connect!"
        self.b_connect["command"] = self.do_connect
        self.b_connect.grid(column=2,row=0)

        
        # init
        self.pan_up = tk.Button(self)
        self.pan_up["text"] = "INIT"
        self.pan_up["command"] = self.do_init
        self.pan_up.grid(column=8,row=1)

        # speed
        # self.pan_up = tk.Button(self)
        # self.pan_up["text"] = "Select Speed"
        # self.pan_up["command"] = self.update_speed
        # self.pan_up.grid(column=8,row=1)

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.grid(column=6,row=8)

    def create_joystick(self):
        self.pan_left = tk.Button(self)
        self.pan_left["text"] = "PAN LEFT"
        self.pan_left["command"] = self.do_pan_left
        self.pan_left.grid(column=0,row=4)

        self.pan_left_while_pressed = tk.Button(self)
        self.pan_left_while_pressed["text"] = "PAN LEFT (hold)"
        self.pan_left_while_pressed.bind("<ButtonPress>",self.do_pan_left)
        self.pan_left_while_pressed.bind("<ButtonRelease>",self.do_stop)
        self.pan_left_while_pressed.grid(column=1,row=4)

        self.micro_left = tk.Button(self)
        self.micro_left["text"] = "µLEFT"
        self.micro_left["command"] = self.do_microstep_left
        self.micro_left.grid(column=2,row=4)
        
        self.pan_right = tk.Button(self)
        self.pan_right["text"] = "PAN RIGHT"
        self.pan_right["command"] = self.do_pan_right
        self.pan_right.grid(column=6,row=4)

        self.pan_right_while_pressed = tk.Button(self)
        self.pan_right_while_pressed["text"] = "PAN RIGHT (hold)"
        self.pan_right_while_pressed.bind("<ButtonPress>",self.do_pan_right)
        self.pan_right_while_pressed.bind("<ButtonRelease>",self.do_stop)
        self.pan_right_while_pressed.grid(column=5,row=4)

        self.micro_right = tk.Button(self)
        self.micro_right["text"] = "µRIGHT"
        self.micro_right["command"] = self.do_microstep_right
        self.micro_right.grid(column=4,row=4)

        # up
        self.pan_up = tk.Button(self)
        self.pan_up["text"] = "PAN UP"
        self.pan_up["command"] = self.do_pan_up
        self.pan_up.grid(column=3,row=1)

        self.pan_up_while_pressed = tk.Button(self)
        self.pan_up_while_pressed["text"] = "PAN UP (hold)"
        self.pan_up_while_pressed.bind("<ButtonPress>",self.do_pan_up)
        self.pan_up_while_pressed.bind("<ButtonRelease>",self.do_stop)
        self.pan_up_while_pressed.grid(column=3,row=2)

        self.micro_up = tk.Button(self)
        self.micro_up["text"] = "µUP"
        self.micro_up["command"] = self.do_microstep_up
        self.micro_up.grid(column=3,row=3)

        # down
        self.pan_down = tk.Button(self)
        self.pan_down["text"] = "PAN DOWN"
        self.pan_down["command"] = self.do_pan_down
        self.pan_down.grid(column=3,row=7)

        self.pan_down_while_pressed = tk.Button(self)
        self.pan_down_while_pressed["text"] = "PAN DOWN (hold)"
        self.pan_down_while_pressed.bind("<ButtonPress>",self.do_pan_down)
        self.pan_down_while_pressed.bind("<ButtonRelease>",self.do_stop)
        self.pan_down_while_pressed.grid(column=3,row=6)

        self.micro_down = tk.Button(self)
        self.micro_down["text"] = "µDOWN"
        self.micro_down["command"] = self.do_microstep_down
        self.micro_down.grid(column=3,row=5)

        
        self.b_stop = tk.Button(self)
        self.b_stop["text"] = "STOP"
        self.b_stop["command"] = self.do_stop
        self.b_stop.grid(column=3,row=4)

    def do_connect(self,event=0):
        # connect to serial port contained in combobox
        port = self.cb_port.get()
        print("Connecting to '%s'..."%port)
        self.init_mount(port)

    def say_hi(self):
        print("hi there, everyone!")

    def do_pan_left(self,event=0):
        print("panning left")
        self.mount.pan_left()

    def do_pan_up(self,event=0):
        self.mount.pan_up()

    def do_pan_down(self,event=0):
        self.mount.pan_down()

    def do_microstep_up(self,event=0):
        self.mount.pan_up()
        self.mount.stop_moving()
        
    def do_microstep_down(self,event=0):
        self.mount.pan_down()
        self.mount.stop_moving()
        
    def do_microstep_left(self,event=0):
        self.mount.pan_left()
        self.mount.stop_moving()

    def do_microstep_right(self,event=0):
        self.mount.pan_right()
        self.mount.stop_moving()

    def do_pan_right(self,event=0):
        print("panning right")
        self.mount.pan_right()
        
    def do_stop(self,event=0):
        print("stopping")
        self.mount.stop_moving()

    def do_init(self,event=0):
        self.mount.test_init()

        
root = tk.Tk()
app = Application(master=root)
app.mainloop()
