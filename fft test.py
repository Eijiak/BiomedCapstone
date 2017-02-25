import urllib.request
import matplotlib.pyplot as plt
import numpy as np
from numpy import fft
from datetime import datetime

time_step = 1/200; # corresponds to 200 Hz

array = [1, 2, 3, 4, 5]
del array[1:2]
print(array)
"""
x = np.arange(0,2000)

w1 = 50.0 # wavelength (meters)
w2 = 20.0 # wavelength (meters)
fx = np.sin(np.pi*x/w1)+ np.sin(np.pi*x/w2)# + 2*np.cos(2*np.pi*x/w2) # signal


ps = np.abs(np.fft.fft(fx))**2
freqs = np.fft.fftfreq(2000, time_step)
idx = np.argsort(freqs)

# Variables
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

for i in range (0, len(freqs[idx])):

    if(freqs[idx][i] > 30 and freqs[idx][i] <= 50):
        gammaIndexes.append(i)
    if(freqs[idx][i] > 14 and freqs[idx][i] <= 30):
        betaIndexes.append(i)
    if(freqs[idx][i] > 8 and freqs[idx][i] <= 14):
        alphaIndexes.append(i)
    if(freqs[idx][i] > 4 and freqs[idx][i] <= 8):
        thetaIndexes.append(i)
    elif(freqs[idx][i] >= 0.1 and freqs[idx][i] <= 4):
        deltaIndexes.append(i)

for i in range (0, len(gammaIndexes)):
    gammaSum += ps[idx][gammaIndexes[i]]

for i in range (0, len(betaIndexes)):
    betaSum += ps[idx][betaIndexes[i]]

for i in range (0, len(alphaIndexes)):
    alphaSum += ps[idx][alphaIndexes[i]]

for i in range (0, len(thetaIndexes)):
    thetaSum += ps[idx][thetaIndexes[i]]

for i in range (0, len(deltaIndexes)):
    deltaSum += ps[idx][deltaIndexes[i]]

sums = [gammaSum, betaSum, alphaSum, thetaSum, deltaSum]

plt.figure(1)
plt.subplot(131)
plt.plot(fx)



plt.subplot(132)

plt.plot(freqs[idx], ps[idx])

ax = plt.subplot(133)
print(len(sums))
ind = np.arange(len(sums))
width = 0.7
ax.bar(ind, sums, width)
ax.set_xticks(ind)
ax.set_xticklabels(("Gamma", "Beta", "Alpha", "Theta", "Delta"))
axes = plt.gca()
axes.set_ylim([0, 1000])
plt.show()

"""
"""
w = np.fft.fft(fx)
freqs = np.fft.fftfreq(len(fx), time_step)

print(freqs.min(), freqs.max())

idx = np.argmax(np.abs(w))
freq = freqs[idx]
print(freq)
"""
