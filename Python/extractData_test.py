# Note Ctrl+C is Keyboard interrupt

# Errors:
# raise BadStatusLine(line) from urllib.request.urllopen
# TimeoutError: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond

import urllib.request
import matplotlib.pyplot as plt
import matplotlib.animation as animation 
import numpy as np
from numpy import fft
from datetime import datetime
from matplotlib import style


#style.use('fivethirtyeight')

# Initialize variables
elec1=[]
elec2=[]
accX=[]
accY=[]

n = 3 # A data point comes every 3 chars
time_step = 0.00675; # ESP samples 1 sample/6ms (adjust to get accurate FFT)
window = 200;
previousNumberValues = 0;
currentNumberValues = 0;
currentIndex = 0;
numDiff = 0;

# Initialize matplotlib plot
fig = plt.figure()
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2)

def animate(i):
    global elec1
    global elec2
    global accX
    global accY

    global n
    global time_step
    global window
    global previousNumberValues
    global currentNumberValues
    global currentIndex
    global numDiff

    with urllib.request.urlopen('http://192.168.4.1/') as f: # Reads analog data from ESP
        y=f.read(2000)
        convData = y.decode("utf-8") # Convert from byte

        # Get indexes of different data
        endIndex0 = convData.find(',')
        endIndex1 = convData.find(',', endIndex0+1)
        endIndex2 = convData.find(',', endIndex1+1)
        endIndex3 = len(convData)-1

        if (endIndex0 > 0): # Checks that there is a comma
            # Break data into chunks of n chars
            elec1 = elec1 + [convData[i:i+n] for i in range(0, endIndex0-1, n)] # Differential input 1
            elec2 = elec2 + [convData[j:j+n] for j in range(endIndex0+1, endIndex1-1, n)] # Differential input 2
            accX = accX + [convData[k:k+n] for k in range(endIndex1+1, endIndex2-1, n)] # X-axis of accelerometer
            accY = accY + [convData[m:m+n] for m in range(endIndex2+1, endIndex3, n)] # Y-axis of accelerometer
            
            if (i%4 == 0): # Only graph data every 4 iterations
                currentNumberValues = len(elec1)
                numDiff = currentNumberValues - previousNumberValues                        
                currentIndex = currentNumberValues-1

                print(max(accX))
                print(max(accY))
                
                # Plot elec1 values
                ax1.clear()
                ax1.plot(elec1[previousNumberValues:currentNumberValues])

                # Plot elec2 values
                ax2.clear()
                ax2.plot(elec2[previousNumberValues:currentNumberValues])

                previousNumberValues = currentNumberValues
                 
                return                                  
    
print ('About to start...')
ani = animation.FuncAnimation(fig, animate, interval=1000) # Interval determines in ms how often to run animate 
plt.show();
        
    
