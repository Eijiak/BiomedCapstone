
import sys
import urllib.request
import matplotlib.pyplot as plt
import matplotlib.animation as animation 
import numpy as np
import pickle
import sys
from tkinter import *
from numpy import fft
from datetime import datetime
from matplotlib import style

class Window(Frame):
    def __init__ (self, master= None):
        Frame.__init__(self,master)
        self.master=master
        self.init_window()

    def init_window(self):
        self.master.title("GUI")
        self.pack(fill=BOTH,expand=1)


        # Menu buttons
        menu=Menu(self.master)
        self.master.config(menu=menu)

        file=Menu(menu)
        file.add_command(label='Save')
        file.add_command(label='Exit',command=self.client_exit)
        menu.add_cascade(label='File',menu=file)

        edit=Menu(menu)
        edit.add_command(label='Undo Last Baseline')
        menu.add_cascade(label='Edit',menu=edit)

        # Baseline Button
        baselineButton=Button(self,text="Take Baseline!")
        baselineButton.place(relx=0.5,rely=0.8,anchor=CENTER)



    def client_exit(self):
        exit()

root=Tk()
root.geometry("1000x600")
app = Window(root)
root.mainloop()
