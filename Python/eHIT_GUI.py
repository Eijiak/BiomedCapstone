import sys
import urllib
import json
import matplotlib
import tkinter as tk
import matplotlib.animation as animation
import numpy as np
import pickle
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style
import matplotlib.pyplot as plt
#from PIL import Image,ImageTk
from numpy import fft
from datetime import datetime
import time
import comparison

matplotlib.use("TkAgg")
print("Loading..")

HUGE_FONT=("RobotoCondensed",30)
LARGE_FONT=("Verdana",12)
TITLE_FONT=("RobotoCondensed",12)
NORM_FONT=("Verdana",10)
SMALL_FONT=("Verdana",8)

style.use("ggplot")
elec1=[]
elec2=[]
accX=[]
accY=[]

elec1Baseline=[]
elec2Baseline=[]
elec1Impact=[]
elec2Impact=[]

n = 3 # A data point comes every 3 chars
time_step = 0.00675 # ESP samples 1 sample/6ms (adjust to get accurate FFT)
window = 200
previousNumberValues = 0
currentNumberValues = 0
currentIndex = 0
numDiff = 0
impactIndex = 0
isConky = False
recordTime = 500
impactDataRecorded = False

# Figure for main page
mainFig = Figure()
a1 = mainFig.add_subplot(121)
a2 = mainFig.add_subplot(122)

# Figure for report page
reportFig = plt.figure(figsize=(10,7))
sub1 = reportFig.add_subplot(311)
sub2 = reportFig.add_subplot(312)
sub3 = reportFig.add_subplot(313)

def getData():
    global elec1
    global elec2
    global accX
    global accY

    dataLink = 'http://192.168.4.1/'
    data = urllib.request.urlopen(dataLink)
    data = data.readall().decode("utf-8")

    endIndex0 = data.find(',')
    endIndex1 = data.find(',', endIndex0 + 1)
    endIndex2 = data.find(',', endIndex1 + 1)
    endIndex3 = len(data) - 1

    if (endIndex0 > 0):  # Checks that there is a comma
        # Break data into chunks of n chars
        elec1 = elec1 + [float(data[i:i + n]) for i in range(0, endIndex0 - 1, n)]  # Differential input 1
        elec2 = elec2 + [float(data[j:j + n]) for j in range(endIndex0 + 1, endIndex1 - 1, n)]  # Differential input 2
        accX = accX + [float(data[k:k + n]) for k in range(endIndex1 + 1, endIndex2 - 1, n)]  # X-axis of accelerometer
        accY = accY + [float(data[m:m + n]) for m in range(endIndex2 + 1, endIndex3, n)]  # Y-axis of accelerometer
        # print(str(max(accX)) + " " + str(max(accY)))
        return True
    return False

def plotData(i):

    global n
    global time_step
    global window
    global previousNumberValues
    global currentNumberValues
    global currentIndex
    global numDiff
    global impactIndex
    global accX
    global accY
    global isConky
    global elec1Impact
    global elec2Impact
    global impactDataRecorded
    global sub1
    global sub2
    global sub3
    global reportFig

    if (getData()):
        print("getting data")
        # Impact Checking
        if (isConky != True and impactDataRecorded != True):
            impactIndex = comparison.isImpact(accX, accY)
            if (impactIndex >= 0):
                impactText = mainFig.text(0.5, 0.5, "Impact Detected!", fontsize=40, ha='center',
                                          bbox={'facecolor': 'red', 'alpha': 0.8, 'pad': 10})
                print("done impact fcn")
                isConky = True
        if (isConky):
            if(currentIndex - impactIndex > recordTime):
                elec1Impact = elec1[impactIndex:(impactIndex + recordTime)]
                elec2Impact = elec2[impactIndex:(impactIndex + recordTime)]
                comparison.compare(elec1Baseline, elec2Baseline, elec1Impact, elec2Impact, 0.006, reportFig, sub1, sub2, sub3)
                print('Recorded impact!')
                print(elec1Impact)
                print(elec2Impact)
                isConky = False
                impactDataRecorded = True

        # Data plotting
        if (i % 3 == 0):  # Only graph data every 3 iterations
            currentNumberValues = len(elec1)
            numDiff = currentNumberValues - previousNumberValues
            currentIndex = currentNumberValues - 1

            # Plot elec1 values
            a1.clear()
            a1.plot(elec1[previousNumberValues:currentNumberValues],
                    "r")
            a1.set_xlabel("Time")
            a1.set_ylabel("Magnitude")
            title="EEG Input 1"
            a1.set_title(title)

            # Plot elec2 values
            a2.clear()
            a2.plot(elec2[previousNumberValues:currentNumberValues],
                    "b")
            a2.set_xlabel("Time")
            a2.set_ylabel("Magnitude")
            title="EEG Input 2"
            a2.set_title(title)

            previousNumberValues = currentNumberValues
    return

def recordBaseline():
    global elec1Baseline
    global elec2Baseline
    global recordTime
    print('got here')
    baselineIndex = currentIndex
    i = 0
    previousTime = time.time()
    while True:
        now = time.time()
        if(now-previousTime>0.001):
            plotData(i)
            previousTime = now
            i=i+1
        if (currentIndex - baselineIndex >= recordTime):
            elec1Baseline = elec1[baselineIndex:(baselineIndex+recordTime)]
            elec2Baseline = elec2[baselineIndex:(baselineIndex + recordTime)]
            print('Recorded baseline!')
            print(elec1Baseline)
            print(elec2Baseline)
            break
    # recBasPopup = tk.Tk()
    # recBasPopup.wm_title("Baseline done!")
    # label = ttk.Label(recBasPopup, text="Baseline Done!", font=NORM_FONT)
    # label.pack(side="top", fill="x", pady=10)
    # recBasPopup.mainloop()
    # recpopup.destroy()

def popupmsg(msg):
    popup=tk.Tk()
    popup.wm_title("Error!")
    label=ttk.Label(popup,text=msg,font=NORM_FONT)
    label.pack(side="top",fill="x",pady=10)
    B1=ttk.Button(popup,text="Okay",command=popup.destroy())
    B1.pack()
    popup.mainloop()

def rec_and_pop():
    recordBaseline()
    recBasePopupMsg("Baseline recording completed!")

def recBasePopupMsg(msg):
    recpopup=tk.Tk()
    recpopup.wm_title("Baseline completed!")
    label=ttk.Label(recpopup,text=msg,font=NORM_FONT)
    label.pack(side="top",fill="x",pady=10)
    recpopup.after(2000, lambda: recpopup.destroy())
    recpopup.mainloop()

class eHIT(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self,default="logo.ico")
        tk.Tk.wm_title(self,"eHIT")

        container=tk.Frame(self)
        container.pack(side="top", fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        menubar=tk.Menu(container)
        filemenu=tk.Menu(menubar,tearoff=1)
        filemenu.add_command(label="Main Page",
                             command=lambda:self.show_frame(mainPage))
        filemenu.add_separator()
        filemenu.add_command(label="Exit",command=quit)
        menubar.add_cascade(label="File",menu=filemenu)

        tk.Tk.config(self,menu=menubar)

        self.frames={}
        for F in (homePage,mainPage,reportPage):
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
                          command=lambda: controller.show_frame(mainPage))
        button1.pack()

    def homeLoop(self, parent, controller):
        global isConky
        if(isConky):
            print ("concussion!")
        else:
            print("no concussion!")
        self.after(1000, self.homeLoop())


class mainPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Main Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # Plot EEG input
        mainCanvas=FigureCanvasTkAgg(mainFig,self)
        mainCanvas.show()
        mainCanvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)


        toolbar=NavigationToolbar2TkAgg(mainCanvas,self)
        toolbar.update()
        mainCanvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        button1 = ttk.Button(self, text="Record Baseline",
                             command=lambda: rec_and_pop())
        button1.pack()

        button2 = ttk.Button(self, text="View More On EEG Data",
                            command=lambda: controller.show_frame(reportPage))
        button2.pack()

        button3 = ttk.Button(self, text="Return to Home Page",
                            command=lambda: controller.show_frame(homePage))
        button3.pack()

        print ('hi')



class reportPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Concussion Report Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        canvasReport = FigureCanvasTkAgg(reportFig, self)
        canvasReport.show()
        canvasReport.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        print("initializing report page")

        button1 = ttk.Button(self, text="Return to Baseline",
                            command=lambda: controller.show_frame(mainPage))
        button1.pack()


app=eHIT()
app.geometry("1280x720")
ani=animation.FuncAnimation(mainFig,plotData,interval=1000)
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

def animate0(i):
    pullData=open("test.txt","r").read()
    dataList=pullData.split('\n')
    xList=[]
    yList=[]
    for eachLine in dataList:
        if len(eachLine)>1:
            x,y=eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))
    a.clear()
    a.plot(xList,yList)
    #a.xlabel("Time (s)")
    #a.ylabel("Magnitude")

def animate1(i):
    dataLink = 'http://192.168.4.1/'
    data = urllib.request.urlopen(dataLink)
    data = data.readall().decode("utf-8")
    data = json.loads(data)
    data = data["btc_usd"]
    data = pd.DataFrame(data)

    buys = data[(data['type'] == "bid")]
    buys["datestamp"] = np.array(buys["timestamp"]).astype("datetime64[s]")
    buyDates = (buys["datestamp"]).tolist()

    sells = data[(data['type'] == "ask")]
    sells["datestamp"] = np.array(sells["timestamp"]).astype("datetime64[s]")
    sellDates = (sells["datestamp"]).tolist()

    a.clear()
    a.plot_date(buyDates, buys["price"])
    a.plot_date(sellDates, sells["price"])