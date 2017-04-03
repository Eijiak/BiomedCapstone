
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

root=Tk()
app = Window(root)
root.mainloop()
