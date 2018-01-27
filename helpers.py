import tkinter as tk
import tkinter.ttk
import os

class Checki(tk.Checkbutton):
    def __init__(self, master=None, text="This is the default Text",
     filename="default.txt", func=None):
        try:
            print(self.vari)
        except:
            pass
        self.text = text
        self.filename = filename
        self.vari = tk.IntVar()
        self.filestring = os.path.join(os.getcwd(), self.filename)
        self.value_file = open(self.filestring)
        self.vari.set(self.value_file.read())
        #print("'self.vari' is %s" % self["variable"])
        super().__init__(master, text=self.text, variable=self.vari)
        self.func = func
        #print("var: %s" % self["variable"])
        
        
