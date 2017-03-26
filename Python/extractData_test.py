# Note Ctrl+C is Keyboard interrupt

import urllib.request
import matplotlib.pyplot as plt
import matplotlib.animation as animation 
import numpy as np
from numpy import fft
from datetime import datetime
from matplotlib import style


#style.use('fivethirtyeight')

# Initialize variables
values=[]
values1=[]
values2=[]
values3=[]
n = 3 # A data point comes every 3 chars
time_step = 0.006; # ESP samples 1 sample/6ms

gammaIndexes = []
gammaSum = 0
betaIndexes =[]
betaSum = 0
alphaIndexes = []
alphaSum = 0
thetaIndexes = []
thetaSum = 0
deltaIndexes = []
deltaSum = 0

window = 200;
previousNumberValues = 0;
currentNumberValues = 0;
currentIndex = 0;
numDiff = 0;

fig = plt.figure()
##ax1 = fig.add_subplot(1,1,1)
ax1 = fig.add_subplot(1,3,1)
ax2 = fig.add_subplot(1,3,2)
ax3 = fig.add_subplot(1,3,3)

def animate(i):
    global values
    global values1
    global values2
    global values3
    global n
    global time_step

    global gammaIndexes 
    global gammaSum 
    global betaIndexes 
    global betaSum 
    global alphaIndexes 
    global alphaSum 
    global thetaIndexes
    global thetaSum
    global deltaIndexes 
    global deltaSum
    
    global window
    global previousNumberValues
    global currentNumberValues
    global currentIndex 
    global numDiff
    
    with urllib.request.urlopen('http://192.168.4.1/') as f: # Reads analog data from ESP
        y=f.read(2000)
        convData = y.decode("utf-8") # Convert from byte
##        print (convData)
        
        # Get indexes of different data
        endIndex0 = convData.find(',')
        endIndex1 = convData.find(',', endIndex0+1)
        endIndex2 = convData.find(',', endIndex1+1)
        endIndex3 = len(convData)-1

        if (endIndex0 > 0): # Weak check the data is in the right format
            values = values + [convData[i:i+n] for i in range(0, endIndex0-1, n)] # Break data into chunks of n chars
##            print(values)
            values1 = values1 + [convData[j:j+n] for j in range(endIndex0+1, endIndex1-1, n)]
            values2 = values2 + [convData[k:k+n] for k in range(endIndex1+1, endIndex2-1, n)]
            values3 = values3 + [convData[m:m+n] for m in range(endIndex2+1, endIndex3, n)]
            print(len(values))
            if (i%4 == 0):
                currentNumberValues = len(values)
                numDiff = currentNumberValues - previousNumberValues                        
                currentIndex = currentNumberValues-1;
                
##                print(numDiff)
                ps = np.abs(np.fft.fft(values[previousNumberValues:currentNumberValues]))**2 # only fft the most recent values
                freqs = np.fft.fftfreq(numDiff, time_step)
                idx = np.argsort(freqs)

                for i in range (0, len(freqs[idx])):
                    if(freqs[idx][i] > 30 and freqs[idx][i] <= 50): # Gamma frequencies
                        gammaSum += ps[idx][i]
                    elif(freqs[idx][i] > 14 and freqs[idx][i] <= 30): # Beta frequencies
                            betaSum += ps[idx][i]
                    elif(freqs[idx][i] > 8 and freqs[idx][i] <= 14): # Alpha frequencies
                        alphaSum += ps[idx][i]
                    elif(freqs[idx][i] > 4 and freqs[idx][i] <= 8): # Theta frequencies
                        thetaSum += ps[idx][i]
                    elif(freqs[idx][i] >= 0.1 and freqs[idx][i] <= 4): # Delta frequencies
                        deltaSum += ps[idx][i]

                sums = [gammaSum, betaSum, alphaSum, thetaSum, deltaSum]
                
                # Plot values
                ax1.clear()
                ax1.plot(values[previousNumberValues:currentNumberValues])

                # Plot frequency spectrum
                ax2.clear()
                ax2.plot(freqs[idx], ps[idx]) # freqs[idx] go from -100 to 100 Hz
                

                # Plot desired frequency sums
                ind = np.arange(len(sums))
                width = 0.7
                ax3.clear()
                ax3.bar(ind, sums, width)
                ax3.set_xticks(ind)
                ax3.set_xticklabels(("Gamma", "Beta", "Alpha", "Theta", "Delta"))

                previousNumberValues = currentNumberValues
                 
            
            
            

                                            
            

print ('hi')
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show();
        
    
