# testing for the compare library

import comparison
import matplotlib.pyplot as plt
import numpy as np
import scipy
from numpy import fft
from datetime import datetime
from matplotlib import style
from scipy import signal

fs = 166.67 # same sampling time for all four signals
N = 1e4 # same number of data points for all signals
time = np.arange(N)/fs # discrete time
noise_power = 0.5*fs/2

freq1 = 40 # random assortment of frequencies 
freq2 = 45 # will be used to construct four unique signals
freq3 = 23
freq4 = 20
freq5 = 10
freq6 = 12
freq7 = 5
freq8 = 7
freq9 = 2
freq10 = 3

# construction of signal 1
sig1 = (2*np.sqrt(2))*np.sin(2*np.pi*freq1*time)  #gamma
sig1 += (2*np.sqrt(3))*np.sin(2*np.pi*freq3*time) #beta
sig1 += (2*np.sqrt(3))*np.sin(2*np.pi*freq4*time) #beta
sig1 += (2*np.sqrt(1.5))*np.sin(2*np.pi*freq6*time) #alpha
sig1 += (2*np.sqrt(2))*np.sin(2*np.pi*freq5*time) #alpha
sig1 += (2*np.sqrt(3))*np.sin(2*np.pi*freq7*time) #theta
sig1 += (2*np.sqrt(5))*np.sin(2*np.pi*freq10*time) #delta
sig1 += np.random.normal(scale=np.sqrt(noise_power), size=time.shape) #add noise

# construction of signal 2
sig2 = (2*np.sqrt(2))*np.sin(2*np.pi*freq1*time)  #gamma
sig2 += (2*np.sqrt(1))*np.sin(2*np.pi*freq3*time) #beta
sig2 += (2*np.sqrt(1.5))*np.sin(2*np.pi*freq6*time) #alpha
sig2 += (2*np.sqrt(1))*np.sin(2*np.pi*freq7*time) #theta
sig2 += (2*np.sqrt(2.5))*np.sin(2*np.pi*freq10*time) #delta
sig2 += np.random.normal(scale=np.sqrt(noise_power), size=time.shape) #add noise

# construction of signal 3
sig3 = (2*np.sqrt(5))*np.sin(2*np.pi*freq1*time)  #gamma
sig3 += (2*np.sqrt(3))*np.sin(2*np.pi*freq2*time) #gamma
sig3 += (2*np.sqrt(1))*np.sin(2*np.pi*freq4*time) #beta
sig3 += (2*np.sqrt(5))*np.sin(2*np.pi*freq6*time) #alpha
sig3 += (2*np.sqrt(3))*np.sin(2*np.pi*freq5*time) #alpha
sig3 += (2*np.sqrt(3))*np.sin(2*np.pi*freq8*time) #theta
sig3 += (2*np.sqrt(1))*np.sin(2*np.pi*freq10*time) #delta
sig3 += np.random.normal(scale=np.sqrt(noise_power), size=time.shape) #add noise

# construction of signal 4
sig4 = (2*np.sqrt(3))*np.sin(2*np.pi*freq4*time) #beta
sig4 += (2*np.sqrt(1.5))*np.sin(2*np.pi*freq6*time) #alpha
sig4 += (2*np.sqrt(3))*np.sin(2*np.pi*freq7*time) #theta
sig4 += (2*np.sqrt(5))*np.sin(2*np.pi*freq10*time) #delta
sig4 += np.random.normal(scale=np.sqrt(noise_power), size=time.shape) #add noise



