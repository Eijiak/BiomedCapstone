# Note Ctrl+C is Keyboard interrupt

import urllib.request
import matplotlib.pyplot as plt
import numpy as np
from numpy import fft
from datetime import datetime

# Initialize variables
values=[]
n = 3 # A data point comes every 3 chars
time_step = 0.006;

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

plt.plot(values)

while(1):
	
    with urllib.request.urlopen('http://192.168.4.1/') as f: # Reads analog data from ESP
        y=f.read(2000)
        convData = y.decode("utf-8") # Convert from byte
        values = values + [convData[i:i+n] for i in range(0, len(convData),n)] # Break data into chunks of n chars
        #print(values)
        currentNumberValues = len(values);
        numDiff = currentNumberValues - previousNumberValues;
        print(numDiff)
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
                elif(freqs[idx][i] >= 0.1 and freqs[idx][i] <= 4): # Delta frequencies
                    deltaSum += ps[idx][i]

            sums = [gammaSum, betaSum, alphaSum, thetaSum, deltaSum]
            """
            if len(values)>30:
                del values[:1]
                plt.clf()
            """
            # Plot values
            plt.figure(1)
            plt.subplot(131)
            plt.plot(values)
            
            # Plot frequency spectrum
            plt.subplot(132)  
            plt.plot(freqs[idx], ps[idx]) # freqs[idx] go from -100 to 100 Hz

            # Plot desired frequency sums
            ax = plt.subplot(133)
            ind = np.arange(len(sums))
            width = 0.7
            ax.bar(ind, sums, width)
            ax.set_xticks(ind)
            ax.set_xticklabels(("Gamma", "Beta", "Alpha", "Theta", "Delta"))

            plt.draw()
            
            plt.pause(0.001)
            previousNumberValues = currentNumberValues
            
        
    
