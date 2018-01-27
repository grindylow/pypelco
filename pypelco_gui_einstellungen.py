#!/usr/bin/python3

import os
import tkinter as tk
import tkinter.ttk
from helpers import *


class appsettings(tk.Frame):
    def __init__(self, master=None):
        self.master = master
        super().__init__(master)
        self.create_widgets()
        
    def create_widgets(self):
        self.check_buttons = []
        self.create_ask_con_frame()
        self.create_ok()
        
    def create_ask_con_frame(self):
        self.ask_con_frame = tk.LabelFrame(self)
        self.ask_con_frame["text"] = "AutoConnection"
        self.ask_con_frame.grid(column=0,columnspan=2,row=0,sticky=tk.W+tk.E,
                                    padx=5,pady=5,ipady=5,ipadx=5)

        self.con_check = Checki(master=self.master, text="Autoconnect at Startup",
                            filename='con_check.txt')
        self.check_buttons.append(self.con_check)
        self.con_check.grid(column=0, row=0)
        
        
        
    def create_ok(self):
        # Creates the Button that sets the Settings
        
        self.ok_button = tk.Button(self.master)
        self.ok_button["text"] = "Ok"
        self.ok_button["command"] = self.set_settings
        self.ok_button.grid(column=3,row=2)


    def set_settings(self):
        # Sets the Settings

        for check in self.check_buttons:
            print("Checking:%s   Value: %s" % (check.vari,check.vari.get()))
            if check.vari.get() == 1:
                print("Checked")
            if check.vari.get() == str():
                print("Yeah")
            open(check.filename, 'w').write(str(check.vari.get()))
            print("writing into %s : %s" % (check.filename, str(check.vari.get())))
            del check.vari
        #print(self.con_checked.get())
        
        #if self.con_checked.get() == True:
        #    print("Don't check it, you pups!!")
        
        self.master.destroy()
        
        
        

if __name__=='__main__':
    root=tk.Tk()
    apop = appsettings(master=root)
    apop.mainloop()
