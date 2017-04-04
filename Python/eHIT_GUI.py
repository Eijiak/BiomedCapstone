
import sys
import urllib.request
import matplotlib
import tkinter as tk
from tkinter import ttk
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation 
import numpy as np
import pickle
from PIL import Image,ImageTk
from numpy import fft
from datetime import datetime
from matplotlib import style
print("Loading..")

LARGE_FONT=("RobotoCondensed",12)


class eHIT(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self,default="logo.ico")
        tk.Tk.wm_title(self,"eHIT")

        container=tk.Frame(self)
        container.pack(side="top", fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames={}
        for F in (homePage,baselinePage,reportPage):
            frame = F(container, self)
            self.frames[F]=frame
            frame.grid(row=0,column=0, sticky="nsew")
        self.show_frame(homePage)

    def show_frame(self,cont):
        frame=self.frames[cont]
        frame.tkraise()



class homePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label1=ttk.Label(self,text="eHIT", font=LARGE_FONT)
        label1.pack(pady=10,padx=10)
        label2 = ttk.Label(self, text="EEG Head Injury Tool", font=LARGE_FONT)
        label2.pack(pady=10, padx=10)

        button1=ttk.Button(self,text="Let's get started!",
                          command=lambda: controller.show_frame(baselinePage))
        button1.pack()


class baselinePage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Baseline Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # Plot EEG input
        f=Figure(figsize=(5,5),dpi=100)
        a=f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8],[5,3,4,3,7,8,2,1])
        canvas=FigureCanvasTkAgg(f,self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)


        button1 = ttk.Button(self, text="View More On EEG Data",
                            command=lambda: controller.show_frame(reportPage))
        button1.pack()

        button2 = ttk.Button(self, text="Return to Home Page",
                            command=lambda: controller.show_frame(homePage))
        button2.pack()


class reportPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Concussion Report Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Return to Baseline",
                            command=lambda: controller.show_frame(baselinePage))
        button1.pack()



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