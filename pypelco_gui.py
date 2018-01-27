#!/usr/bin/python3

# Graphical User Interface for Controlling a PELCO-D Camera Mount
#
# specifically this seems to work well with a
#   https://www.aliexpress.com/item/Pan-Tilt-motorized-rotation-bracket-stand-holder-PELCO-D-control-for-CCTV-IP-camera-module-RS232/32827664380.html
#

#
# Copyright notices:
#
# - Uses Icons designed by 'Lucy G', 'Freepik' and 'Smashicons' from Flaticon.

info = """
Graphical User Interface for Controlling a PELCO-D Camera Mount

specifically this seems to work well with a
https://www.aliexpress.com/item/Pan-Tilt-motorized-rotation-bracket-stand-holder-PELCO-D-control-for-CCTV-IP-camera-module-RS232/32827664380.html



Copyright notices:

- Uses Icons designed by 'Lucy G', 'Freepik' and 'Smashicons' from Flaticon.


"""
#imports

import serial
import serial.tools.list_ports
import tkinter as tk
import tkinter.ttk
import os

from pelco_mount import *
from pypelco_gui_einstellungen import *


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def init_mount(self,port="com4"):
        ser = serial.Serial(port,timeout=.1,baudrate=2400)
        print(ser)
        self.mount = pelco_mount(ser)
       
        
    def deinit_mount(self):
        self.mount.close_port()

    def create_widgets(self):

        self.winfo_toplevel().title("PELCO-D Controller")
        
        self.createMenu()
        self.create_connection_frame()
        self.create_joystick_frame()
        self.create_additional_controls_frame()
        self.create_memory_buttons()
        if open( os.path.join(os.getcwd(), 'con_check.txt') ).read() == str(1):
            self.do_connect(True)
        
        
        # init
        # speed
        # self.pan_up = tk.Button(self)
        # self.pan_up["text"] = "Select Speed"
        # self.pan_up["command"] = self.update_speed
        # self.pan_up.grid(column=8,row=1)
            
    def createMenu(self):
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)
        
        #file
        self.pelco_menu = tk.Menu(self.menu)
        self.pelco_menu.add_command(label="Info",command=self.print_help)
        self.pelco_menu.add_command(label="Settings",command=self.go_to_settings)
        self.pelco_menu.add_command(label="Exit",command=root.destroy)
        self.menu.add_cascade(label="Pypelco",menu=self.pelco_menu)
        
    
    def create_connection_frame(self):
        self.connectionframe = tk.LabelFrame(self)
        self.connectionframe["text"] = "Connection"
        self.connectionframe.grid(column=0,columnspan=2,row=0,sticky=tk.W+tk.E,
                                    padx=5,pady=5,ipady=5,ipadx=5)

        self.cb_port_label = tk.Label(self.connectionframe)
        self.cb_port_label["text"] = "COM-Port:"
        self.cb_port_label.grid(column=0,row=0,padx=5)

        self.cb_port = tk.ttk.Combobox(self.connectionframe)
        #if self.cb_port.current()!=0:
        #print('Hä')
        self.do_refresh_port_list()
        self.cb_port.grid(column=1,row=0,padx=5)

        self.b_refresh = tk.Button(self.connectionframe)
        self.b_refresh["text"] = "Refresh port list!"
        self.b_refresh["command"] = self.do_refresh_port_list
        self.b_refresh.grid(column=2,row=0,padx=5)
        self.default_color = self.b_refresh.cget("background")
        
        self.b_connect = tk.Button(self.connectionframe)
        self.b_connect["text"] = "Connect!"
        self.b_connect["command"] = self.do_connect
        self.b_connect.grid(column=3,row=0)

        self.b_disconnect = tk.Button(self.connectionframe)
        self.b_disconnect["text"] = "Disconnect!"
        self.b_disconnect["command"] = self.do_disconnect
        self.b_disconnect.grid(column=4,row=0)

        self.connection_status_label = tk.Label(self.connectionframe)
        self.connection_status_label["text"] = "Connection status: not initialised"
        self.connection_status_label.grid(column=0,row=1,columnspan=5,
                                        sticky=tk.W,padx=5,pady=5,ipady=5,ipadx=5)

    def create_joystick_frame(self):
        self.joystickframe = tk.LabelFrame(self)
        self.joystickframe["text"] = "Joystick"
        self.joystickframe.grid(column=0,row=1,sticky=tk.W+tk.E,padx=5,
                                pady=5,ipady=5,ipadx=5)

        # left
        self.pan_left = tk.Button(self.joystickframe)
        self.pan_left.img = tk.PhotoImage(
                file="icons" + os.sep + "play-left.png").subsample(2,2)
        self.pan_left["image"] = self.pan_left.img
        self.pan_left["text"] = "PAN LEFT"
        self.pan_left["command"] = self.do_pan_left
        self.pan_left.grid(column=0,row=4)

        self.pan_left_while_pressed = tk.Button(self.joystickframe)
        self.pan_left_while_pressed.img = tk.PhotoImage(
                file="icons" + os.sep + "while-pressed-left.png").subsample(2,2)
        self.pan_left_while_pressed["image"] = self.pan_left_while_pressed.img
        self.pan_left_while_pressed["text"] = "PAN LEFT (hold)"
        self.pan_left_while_pressed.bind("<ButtonPress>",self.do_pan_left)
        self.pan_left_while_pressed.bind("<ButtonRelease>",self.do_stop)
        self.pan_left_while_pressed.grid(column=1,row=4)

        self.micro_left = tk.Button(self.joystickframe)
        self.micro_left.img = tk.PhotoImage(
                file="icons" + os.sep + "micro-left.png").subsample(2,2)
        self.micro_left["image"] = self.micro_left.img
        self.micro_left["text"] = "µLEFT"
        self.micro_left["command"] = self.do_microstep_left
        self.micro_left.grid(column=2,row=4)

        # right
        self.pan_right = tk.Button(self.joystickframe)
        self.pan_right.img = tk.PhotoImage(
                file="icons" + os.sep + "play-right.png").subsample(2,2)
        self.pan_right["image"] = self.pan_right.img
        self.pan_right["command"] = self.do_pan_right
        self.pan_right.grid(column=6,row=4)

        self.pan_right_while_pressed = tk.Button(self.joystickframe)
        self.pan_right_while_pressed.img = tk.PhotoImage(
                file="icons" + os.sep + "while-pressed-right.png").subsample(2,2)
        self.pan_right_while_pressed["image"] = self.pan_right_while_pressed.img
        self.pan_right_while_pressed["text"] = "PAN RIGHT (hold)"
        self.pan_right_while_pressed.bind("<ButtonPress>",self.do_pan_right)
        self.pan_right_while_pressed.bind("<ButtonRelease>",self.do_stop)
        self.pan_right_while_pressed.grid(column=5,row=4)

        self.micro_right = tk.Button(self.joystickframe)
        self.micro_right.img = tk.PhotoImage(file="icons" + os.sep + "micro-right.png").subsample(2,2)
        self.micro_right["image"] = self.micro_right.img
        self.micro_right["command"] = self.do_microstep_right
        self.micro_right.grid(column=4,row=4)

        # up
        self.pan_up = tk.Button(self.joystickframe)
        self.pan_up.img = tk.PhotoImage(file="icons" + os.sep + "play-up.png").subsample(2,2)
        self.pan_up["image"] = self.pan_up.img
        self.pan_up["text"] = "PAN UP"
        self.pan_up["command"] = self.do_pan_up
        self.pan_up.grid(column=3,row=1)

        self.pan_up_while_pressed = tk.Button(self.joystickframe)
        self.pan_up_while_pressed.img = tk.PhotoImage(file="icons" + os.sep + "while-pressed-up.png").subsample(2,2)
        self.pan_up_while_pressed["image"] = self.pan_up_while_pressed.img
        self.pan_up_while_pressed["text"] = "PAN UP (hold)"
        self.pan_up_while_pressed.bind("<ButtonPress>",self.do_pan_up)
        self.pan_up_while_pressed.bind("<ButtonRelease>",self.do_stop)
        self.pan_up_while_pressed.grid(column=3,row=2)

        self.micro_up = tk.Button(self.joystickframe)
        self.micro_up.img = tk.PhotoImage(file="icons" + os.sep + "micro-up.png").subsample(2,2)
        self.micro_up["image"] = self.micro_up.img
        self.micro_up["text"] = "µUP"
        self.micro_up["command"] = self.do_microstep_up
        self.micro_up.grid(column=3,row=3)

        # down
        self.pan_down = tk.Button(self.joystickframe)
        self.pan_down.img = tk.PhotoImage(file="icons" + os.sep + "play-down.png").subsample(2,2)
        self.pan_down["image"] = self.pan_down.img
        self.pan_down["text"] = "PAN DOWN"
        self.pan_down["command"] = self.do_pan_down
        self.pan_down.grid(column=3,row=7)

        self.pan_down_while_pressed = tk.Button(self.joystickframe)
        self.pan_down_while_pressed.img = tk.PhotoImage(file="icons" + os.sep + "while-pressed-down.png").subsample(2,2)
        self.pan_down_while_pressed["image"] = self.pan_down_while_pressed.img
        self.pan_down_while_pressed["text"] = "PAN DOWN (hold)"
        self.pan_down_while_pressed.bind("<ButtonPress>",self.do_pan_down)
        self.pan_down_while_pressed.bind("<ButtonRelease>",self.do_stop)
        self.pan_down_while_pressed.grid(column=3,row=6)

        self.micro_down = tk.Button(self.joystickframe)
        self.micro_down.img = tk.PhotoImage(file="icons" + os.sep + "micro-down.png").subsample(2,2)
        self.micro_down["image"] = self.micro_down.img
        self.micro_down["text"] = "µDOWN"
        self.micro_down["command"] = self.do_microstep_down
        self.micro_down.grid(column=3,row=5)


        self.b_stop = tk.Button(self.joystickframe)
        self.b_stop.img = tk.PhotoImage(file="icons" + os.sep + "stop.png").subsample(2,2)
        self.b_stop["image"] = self.b_stop.img
        self.b_stop["text"] = "STOP"
        self.b_stop["command"] = self.do_stop
        self.b_stop.grid(column=3,row=4)

    def create_additional_controls_frame(self):
        self.add_contr_frame = tk.LabelFrame(self)
        self.add_contr_frame["text"] = "Controls"
        self.add_contr_frame.grid(column=1,row=1,sticky=tk.N+tk.W+tk.E,
                                    padx=5,pady=5)



        self.NROFSPEEDS = 3
        self.speed_button = [None]*self.NROFSPEEDS
        # init
        for speed in range(0,self.NROFSPEEDS):
            self.speed_button[speed] = tk.Button(self.add_contr_frame)
            self.speed_button[speed]["text"] = "Speed %s" % (speed+1)
            self.speed_button[speed].bind('<Button-1>', self.do_set_speed)
            self.speed_button[speed].grid(column=0,row=(speed+1),
                                            padx=5,sticky=tk.E+tk.W)
            self.speed_button[speed].speednr = speed
        
        # quit
        self.quit = tk.Button(self.add_contr_frame, text="QUIT", fg="red",
                              command=root.destroy, )
        self.quit.grid(column=0,row=4,padx=5,pady=5,sticky=tk.E+tk.W)
        
    def create_memory_buttons(self):
        self.memframe = tk.LabelFrame(self)
        self.memframe["text"] = "Position Memory"
        self.memframe.grid(column=0,columnspan=2,
                    row=2,sticky=tk.W+tk.E,padx=5,pady=5,ipady=5,ipadx=5)
        
        self.NR_OF_SLOTS = 8
        self.mem_name = [None]*self.NR_OF_SLOTS
        self.mem_desc = [None]*self.NR_OF_SLOTS
        self.mem_store = [None]*self.NR_OF_SLOTS
        self.mem_go = [None]*self.NR_OF_SLOTS
        for line in range(0,self.NR_OF_SLOTS):
            self.mem_name[line] = tk.Label(self.memframe)
            self.mem_name[line]["text"] = "Slot %s:" % (line+1)
            self.mem_name[line].grid(column=0,row=0+line,padx=5)
            
            self.mem_desc[line] = tk.Entry(self.memframe)
            self.mem_desc[line].insert(0,"SLOT %s" % (line+1))
            self.mem_desc[line].grid(column=1,row=0+line,padx=5)

            self.mem_store[line] = tk.Button(self.memframe)
            self.mem_store[line]["text"] = "Store Position %s!" % (line+1)
            self.mem_store[line].grid(column=2,row=0+line,padx=5)
            self.mem_store[line].slotnr = line+1
            self.mem_store[line].bind('<Button-1>', self.do_store_position)
           
            self.mem_go[line] = tk.Button(self.memframe)
            self.mem_go[line]["text"] = "Go to Position %s!" % (line+1)
            self.mem_go[line]["underline"] = 15
            self.mem_go[line].grid(column=3,row=0+line,padx=5)
            self.mem_go[line].slotnr = line+1
            self.mem_go[line].bind('<Button-1>', self.do_go_to_position)
        
    def print_help(self):
        print("Info:")
        print()
        print(info)
    
    def go_to_settings(self):
        root.destroy()
        apop = appsettings(master=tk.Tk())
        apop.mainloop()

        
        

    def do_connect(self, Autoconnect=False, event=0):
        # connect to serial port contained in combobox

        portidx = self.cb_port.current()   # returns currently selected index, or -1 if current selection not contained in "values"
        print("PORTIDX=%s"%portidx)
        print("PORT=%s"%self.available_ports[portidx])
        port = self.cb_port.get()
        if portidx==-1:
            # custom text content
            pass
        else:
            port = self.available_ports[portidx].device
        print("Connecting to '%s'..."%port)
        self.init_mount(port)
        if portidx==-1:
            self.connection_status_label["text"] = "Connection status: No available ports found."
        elif Autoconnect == True:
            self.connection_status_label["text"] = "Connection status: Autoconnected to %s."%port
        else:
            self.connection_status_label["text"] = "Connection status: Connected to %s."%port

    def do_disconnect(self,event=0):
        self.deinit_mount()
        self.connection_status_label["text"] = "Connection status: Not connected."

    def do_refresh_port_list(self,event=0):
        self.available_ports = serial.tools.list_ports.comports()
        self.cb_port["values"] = [x.description for x in self.available_ports]

        if len(self.cb_port["values"]) == 0:
            print("No ports found!")
        else:
            self.cb_port.current(0)

    def say_hi(self,event=0):
        print("hi there, everyone!")
        
    def change_bg_speed(self,button, color, event=0):
        button["bg"] = color

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
        
    def do_set_speed(self,event=0):
    
        spnrset = event.widget.speednr
        print(spnrset)
        for x in range(0,self.NROFSPEEDS):
            origin_color = self.speed_button[x].cget("background")
            if x == spnrset:
                self.speed_button[spnrset]["bg"] = "grey"
                self.mount.set_speed(spnrset)
            else:
                self.speed_button[x]["bg"] = self.default_color
        
        
    
    def do_set_speed_high(self,event=0):
        print("setting speed to high")
        self.mount.set_speed(SPEED_HIGH)
        self.change_bg(button=self.speed_high,color="grey")

    def do_set_speed_med(self,event=0):
        print("setting speed to medium")
        self.mount.set_speed(SPEED_MEDIUM)
        self.change_bg(button=self.speed_med,color="grey")

    def do_set_speed_low(self,event=0):
        print("setting speed to slow")
        self.mount.set_speed(SPEED_LOW)
        self.change_bg(button=self.speed_low,color="grey")
        
        
    def do_store_position(self,event=0):
        slotnr = event.widget.slotnr
        print("storing current position to slot %s" % slotnr)
        self.mount.store_position(slotnr)

    def do_go_to_position(self,event=0):
        slotnr = event.widget.slotnr
        print("moving to stored position slot %s" % slotnr)
        self.mount.go_to_position(slotnr)

    def do_stop(self,event=0):
        print("stopping")
        self.mount.stop_moving()

    def do_init(self,event=0):
        self.mount.test_init()


root = tk.Tk()
app = Application(master=root)
app.mainloop()
