
import sys
import urllib.request
import matplotlib.pyplot as plt
import matplotlib.animation as animation 
import numpy as np
import pickle
import tkinter as tk
from PIL import Image,ImageTk
from numpy import fft
from datetime import datetime
from matplotlib import style

LARGE_FONT=("RobotoCondensed",12)


class eHIT(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container=tk.Frame(self)

        container.pack(side="top", fill="both",expand=True)

        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames={}
        frame = StartPage(container, self)
        self.frames[StartPage]=frame
        frame.grid(row=0,column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self,cont):
        frame=self.frames[cont]
        frame.tkraise()



class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label=tk.Label(self,text="eHIT", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1=tk.Button(self,text="Let's get started!",
                          command=lambda: controller.show_frame(baselinePage))
        button1.pack()

class baselinePage(tk.Frame):
    def __init__(self,parent,controller):



print("Loading..")
app=eHIT()
app.geometry("800x400")
app.mainloop()


# Basic testing for window, buttons, and menus
'''
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
        edit.add_command(label='Show Logo',command=self.showImg)
        edit.add_command(label='Show Text', command=self.showTxt)
        menu.add_cascade(label='Edit',menu=edit)

        # Baseline Button
        baselineButton=Button(self,text="Take Baseline!")
        baselineButton.place(relx=0.5,rely=0.8,anchor=CENTER)


    def client_exit(self):
        exit()

    def showImg(self):
        load=Image.open('logo.png')
        render=ImageTk.PhotoImage(load)
        img=Label(self,image=render)
        img.image=render
        img.place(relx=0.5,rely=0.2,anchor=CENTER)

    def showTxt(self):
        text=Label(self,text='EEG Head Injury Tool')
        text.pack()

root=Tk()
root.geometry("1000x600")
app = Window(root)
root.mainloop()
'''