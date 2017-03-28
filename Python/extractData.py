# Note Ctrl+C is Keyboard interrupt

import urllib.request
import matplotlib.pyplot as plt
import numpy as np
from numpy import fft
from datetime import datetime
from matplotlib import style
from scipy import signal

##style.use('fivethirtyeight')

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
betaSum = 0;
alphaIndexes = []
alphaSum = 0;
thetaIndexes = []
thetaSum = 0;
deltaIndexes = []
deltaSum = 0

window = 200;
previousNumberValues = 0;
currentNumberValues = 0;
currentIndex = 0;
numDiff = 0;

fig = plt.figure()
ax1 = fig.add_subplot(1,3,1)
ax2 = fig.add_subplot(1,3,2)
ax3 = fig.add_subplot(1,3,3)

while(1):
	
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
            values1 = values1 + [convData[j:j+n] for j in range(endIndex0+1, endIndex1-1, n)]
            values2 = [convData[k:k+n] for k in range(endIndex1+1, endIndex2-1, n)]
            values3 = [convData[m:m+n] for m in range(endIndex2+1, endIndex3, n)]

            currentNumberValues = len(values);
            numDiff = currentNumberValues - previousNumberValues;
  
            if(numDiff > window): # only do analysis for a short period of time

                currentIndex = currentNumberValues-1;
                print(currentIndex);
                ps = np.abs(np.fft.fft(values[previousNumberValues:currentIndex]))**2 # only fft the most recent values
                freqs = np.fft.fftfreq(window, time_step)
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
                    elif(freqs[idx][i] >= 1 and freqs[idx][i] <= 4): # Delta frequencies
                        deltaSum += ps[idx][i]

                sums = [gammaSum, betaSum, alphaSum, thetaSum, deltaSum]
                """
                if len(values)>30:
                    del values[:1]
                    plt.clf()
                """
##                ax1.clear()
##                ax2.clear()
##                ax3.clear()
##                if(currentNumberValues > 300):
##                    del values[:(currentNumberValues-300)]
                # Plot values
                ax1.plot(values)
                
                # Plot frequency spectrum
                plt.subplot(132)  
                ax2.plot(freqs[idx], ps[idx]) # freqs[idx] go from -100 to 100 Hz

                # Plot desired frequency sums
                ind = np.arange(len(sums))
                width = 0.7
                ax3.bar(ind, sums, width)
                ax3.set_xticks(ind)
                ax3.set_xticklabels(("Gamma", "Beta", "Alpha", "Theta", "Delta"))

                plt.draw()
                
                plt.pause(0.00001)
                previousNumberValues = currentNumberValues
				

	
	
            
        
    
