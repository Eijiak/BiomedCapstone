# Note Ctrl+C is Keyboard interrupt

import matplotlib.pyplot as plt
import numpy as np
import scipy
from numpy import fft
from datetime import datetime
from matplotlib import style
from scipy import signal

def removeDC(signal, time_step):

	fs = 1/time_step
	
	return

def isImpact():

	return

def compare(baseline1, baseline2, elec1, elec2, time_step):

	warnCount = 0  # how many times we have weird frequency lelel changes
	
	warnValue = 10 # how many changes in frequency levels do we tolerate before sending out warning

	# remove DC compnents
	baseline1 = removeDC(baseline1, time_step)
	baseline2 = removeDC(baseline2, time_step)
	elec1 = removeDC(elec1, time_step)
	elec2 = removeDC(elec2, time_step)
	
	# freq is the same for everything
	
	# collect power spectral density related statistics
	# PSD for each differential eeg input pair
	# see ft_compare() for more details
	freq, PSD_base1, PSD_impact1, sumsBasePSD1, sumsImpactPSD1, relDiffPSD1 = ft_compare(baseline1, elec1, time_step)
	freq, PSD_base2, PSD_impact2, sumsBasePSD2, sumsImpactPSD2, relDiffPSD2 = ft_compare(baseline2, elec2, time_step)
	
	# collect coherence related statistics
	# coherence for baseline and post-impact
	# see xcoh_compare() for more details
	freqBase, C_base, C_impact, sumsBaseC, sumsImpactC, relDiffC = xcoh_compare(baseline1, baseine2, elec1, elec2, time_step)
	
	# go through the relative differences in frequency level and 
	# increment warnCount if relDiff >= 0.5
	for i in range(0,5):
		if (relDiffPSD1[i] >= 0.5):
			warnCount += 1
	for j in range(0.5):
		if (relDiffPSD2[j] >= 0.5):
			warnCount += 1
	for k in range(0.5):
		if (relDiffC[k] >= 0.5):
			warnCount += 1
	
	# send out warning if there are too many frequency level changes	
	if (warnCount >= 10):
		# <inster warning msg code>
		# <code for saving all PSD and coherence data
		ft_plot(freq, PSD_base1, PSD_impact1, sumsBasePSD1, sumsImpactPSD1)
		ft_plot(freq, PSD_base2, PSD_impact2, sumsBasePSD2, sumsImpactPSD2)
		xcoh_plot(freq, C_base, C_impact, sumsBaseC, sumsImpactC)
		
	return

def ft_compare(baseline, elec, time_step):
	"""
	function computes power spectran densities of two signals and compares them
	comparison is done via looking at gamma, beta, alpha, theta, delta components
	DOES NOT PLOT

	Inputs:
	baseline - list of baseline eeg input values
	elec - list of post-impact eeg input values
	time_step - sampling stem of our signal
	IMPORTANT: BASELINE AND ELEC LIST MUST HAVE SAME LENGTH

	Outputs:
	freqBase - PSD x-axis
	PSD_base - Baseline PSD y-axis
	PSD_impact - post-impact y-axis
	sumsBase - baseline gamma, beta, alpha, theta, delta components
	sumsImpact - post-impact gamma, beta, alpha, theta, delta components
	relDiff - (abs (sumsBase - sumsDiff) )/ sumsBase

	Format:
	freqBase, PSD_base, PSD_impact, sumsBase, sumsImpact, sumsDiff = ft_compare(baseline, elec, time_step)
	"""

	# variables for different baseline eeg frequency groups
	gammaSumBase = 0
	betaSumBase = 0
	alphaSumBase = 0
	thetaSumBase = 0
	deltaSumBase = 0
	
	# variables for differnt post-impact eeg frequency groups
	gammaSumImpact = 0
	betaSumImpact = 0
	alphaSumImpact = 0
	thetaSumImpact = 0
	deltaSumImpact = 0

	fs = 1/time_step  # sampling frequency
	
	# baseline power spectral density
	freqBase, PSD_base = scipy.signal.periodogram(baseline, fs)
	# post-impact power sectral density
	freqImpact, PSD_impact = scipy.signal.periodogram(elec, fs)
	# freqBase and freqImpact should be idendical 
	
	# for loops used to calculate different eeg frequency types
	# two loops - baseline PSD and post-impact PSD
	# when adding up the PSD components, use log10 values for better linearity
	for i in range(0,len(freqBase)):
		if ((freqBase[i] > 30) and (freqBase[i] <= 50)): #gamma
			gammaSumBase += np.log10(PSD_base[i])
		elif ((freqBase[i] > 14) and (freqBase[i] <= 30)): #beta
			betaSumBase += np.log10(PSD_base[i])
		elif ((freqBase[i] > 8) and (freqBase[i] <= 14)): #alpha
			alphaSumBase += np.log10(PSD_base[i])
		elif ((freqBase[i] > 4) and (freqBase[i] <= 8)): #theta
			thetaSumBase += np.log10(PSD_base[i])
		elif ((freqBase[i] >= 1) and (freqBase[i] <= 4)): #delta
			deltaSumBase += np.log10(PSD_base[i])
			
	sumsBase = [gammaSumBase, betaSumBase, alphaSumBase, thetaSumBase, deltaSumBase]
	
	for j in range(0,len(freqImpact)):
		if ((freqImpact[j] > 30) and (freqImpact[j] <= 50)): #gamma
			gammaSumImpact += np.log10(PSD_impact[j])
		elif ((freqImpact[j] > 14) and (freqImpact[j] <= 30)): #beta
			betaSumImpact += np.log10(PSD_impact[j])
		elif ((freqImpact[j] > 8) and (freqImpact[j] <= 14)): #alpha
			alphaSumImpact += np.log10(PSD_impact[j])
		elif ((freqImpact[j] > 4) and (freqImpact[j] <= 8)): #theta
			thetaSumImpact += np.log10(PSD_impact[j])
		elif ((freqImpact[j] >= 1) and (freqImpact[j] <= 4)): #delta
			deltaSumImpact += np.log10(PSD_impact[j])
			
	sumsImpact = [gammaSumImpact, betaSumImpact, alphaSumImpact, thetaSumImpact, deltaSumImpact]
	
	# difference in the gamma, beta, alpha, theta, and delta levels 
	# of baseline and post-impact
	relDiff = range(0,5)
	for k in range(0, 4):
		relDiff[k] = (abs(sumsBase[k] - sumsImpact[k]))/sumsBase[k]
		
	return freqBase, PSD_base, PSD_impact, sumsBase, sumsImpact, relDiff
		
	
def ft_plot(freq, PSD_base, PSD_impact, sumsBasePSD, sumsImpactPSD):
	'''
	function plots PSD of baseline and post-impact eeg data
	also plots frequency groups in a bar graph

	Inputs:
	freq - frquency/x-axis for PSD plots
	PSD_base - baseline PSD y-axis
	PSD_impact - post-impact PSD y-axis
	sumsBasePSD - list of gamma, beta, alpha, theta, delta levels - baseline
	sumsImpactPSD - list of gamma, beta, alpha, theta, delta levels - post-impact
	'''

	fig = plt.figure(figsize=(4,3))
	
	sub1 = fig.add_subplot(131)  # PSD of baseline
	sub1.set_title('Power Spectral Density - Baseline')
	sub1.set_xlabel('f[Hz]')
	sub1.set_ylabel('PSD[V^2/Hz]')
	sub1.set_xticks([-60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60])
	sub1.plot(freq, PSD_base)
	
	sub2 = fig.add_subplot(132)  # PSD of post-impact data
	sub2.set_title('Power Spectral Density - Post-Impact')
	sub2.set_xlabel('f[Hz]')
	sub2.set_ylabel('PSD[V^2/Hz]')
	sub2.set_xticks([-60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60])
	sub2.plot(freq, PSD_impact)
	
	# levels of different frequency groups
	# display baseline and post-impact info in one bar graph
	ind = np.arange(len(sumsBasePSD))
        width = 0.15
	sub3 = fig.add_subplot(133) 
	rects1 = sub3.bar(ind, sumsBasePSD, width, color='b')
	rects2 = sub3.bar(ind + width, sumsImpactPSD, width, color='r')
	sub3.set_title("Levels of Frequency Groups")
	sub3.set_xticks(ind + width / 2)
	sub3.set_xticklabels(("Gamma", "Beta", "Alpha", "Theta", "Delta"))
	sub3.legend((rects1[0], rects2[0]), ('Baseline', 'Post-Impact'))
	
	plt.tight_layout()
	plt.show()
	
	return

def xcoh_compare(baseline1, baseline2, elec1, elec2, time_step):
	"""
	function computes coherence of two signals and compares them
	comparison is done via looking at gamma, beta, alpha, theta, delta components
	Take coherence of two differential eeg inputs at baseline and at post-impact
	DOES NOT PLOT

	Inputs:
	baseline1 - list of baseline diferential eeg input pair 1 values
	baseline2 - list of baseline diferential eeg input pair 1 values
	elec1 - list of post-impact diferential eeg input pair 1 values
	elec2 - list of post-impact diferential eeg input pair 1 values
	time_step - sampling stem of our signal
	IMPORTANT: ALL LISTS MUST HAVE SAME LENGTH

	Outputs:
	freqBase - PSD x-axis
	C_base - Baseline coherence
	C_impact - post-impact coherence
	sumsBase - baseline gamma, beta, alpha, theta, delta components
	sumsImpact - post-impact gamma, beta, alpha, theta, delta components
	relDiff - (abs (sumsBase - sumsDiff))/sumsBase

	Format:
	freqBase, C_base, C_impact, sumsBase, sumsImpact, relDiff = xcoh_compare(baseline1, baseine2, elec1, elec2, time_step)
	"""

	# variables for different baseline eeg frequency groups
	gammaSumBase = 0
	betaSumBase = 0
	alphaSumBase = 0
	thetaSumBase = 0
	deltaSumBase = 0
	
	# variables for differnt post-impact eeg frequency groups
	gammaSumImpact = 0
	betaSumImpact = 0
	alphaSumImpact = 0
	thetaSumImpact = 0
	deltaSumImpact = 0

	fs = 1/time_step #sampling frequency
	
	# baseline coherence of two differential electrode inputs
	freqBase, C_base = scipy.signal.coherence(baseline1,baseline2,fs)
	# post-impact coherence of two diferential electrode inputs
	freqImpact, C_impact = scipy.signal.coherence(elec1,elec2,fs)
	
	# for loops used to calculate different eeg frequency types in coherence plot
	# two loops - baseline coherence and post-impact coherence
	# Coherence >= 1 at all times
	for i in range(0,len(freqBase)):
		if ((freqBase[i] > 30) and (freqBase[i] <= 50)): #gamma
			gammaSumBase += C_base[i]
		elif ((freqBase[i] > 14) and (freqBase[i] <= 30)): #beta
			betaSumBase += C_base[i]
		elif ((freqBase[i] > 8) and (freqBase[i] <= 14)): #alpha
			alphaSumBase += C_base[i]
		elif ((freqBase[i] > 4) and (freqBase[i] <= 8)): #theta
			thetaSumBase += C_base[i]
		elif ((freqBase[i] >= 1) and (freqBase[i] <= 4)): #delta
			deltaSumBase += C_base[i]
			
	sumsBase = [gammaSumBase, betaSumBase, alphaSumBase, thetaSumBase, deltaSumBase]
	
	for j in range(0,len(freqImpact)):
		if ((freqImpact[j] > 30) and (freqImpact[j] <= 50)): #gamma
			gammaSumImpact += C_impact[j]
		elif ((freqImpact[j] > 14) and (freqImpact[j] <= 30)): #beta
			betaSumImpact += C_impact[j]
		elif ((freqImpact[j] > 8) and (freqImpact[j] <= 14)): #alpha
			alphaSumImpact += C_impact[j]
		elif ((freqImpact[j] > 4) and (freqImpact[j] <= 8)): #theta
			thetaSumImpact += C_impact[j]
		elif ((freqImpact[j] >= 1) and (freqImpact[j] <= 4)): #delta
			deltaSumImpact += C_impact[j]
			
	sumsImpact = [gammaSumImpact, betaSumImpact, alphaSumImpact, thetaSumImpact, deltaSumImpact]
	
	# difference in the gamma, beta, alpha, theta, and delta levels 
	# of baseline and post-impact
	relDiff = range(0,5)
	for k in range(0, 4):
		relDiff[k] = (abs(sumsBase[k] - sumsImpact[k]))/sumsBase
		
	return freqBase, C_base, C_impact, sumsBase, sumsImpact, relDiff

def xcoh_plot(freq, C_base, C_impact, sumsBaseC, sumsImpactC):
	'''
	function plots Coherence of baseline and post-impact eeg data
	also plots coherence in frequency groups in a bar graph

	Inputs:
	freq - frquency/x-axis for PSD plots
	C_base - baseline Coherence y-axis
	C_impact - post-impact Coherence y-axis
	sumsBaseC - list of gamma, beta, alpha, theta, delta levels - baseline
	sumsImpactC - list of gamma, beta, alpha, theta, delta levels - post-impact
	'''

	fig = plt.figure(figsize=(4,3))
	
	sub1 = fig.add_subplot(131)  # Coherence of baseline
	sub1.set_title('Coherence plot - Baseline')
	sub1.set_xlabel('f[Hz]')
	sub1.set_ylabel('Coherence')
	sub1.set_xticks([-60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60])
	sub1.plot(freq, C_base)
	
	sub2 = fig.add_subplot(132)  # Coherence of post-impact data
	sub2.set_title('Coherence plot - Post-Impact')
	sub2.set_xlabel('f[Hz]')
	sub2.set_ylabel('Coherence')
	sub2.set_xticks([-60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60])
	sub2.plot(freq, C_impact)
	
	# levels of Coherence in different frequency groups
	# display baseline and post-impact info in one bar graph
	ind = np.arange(len(sumsBaseC))
	width = 0.15
	sub3 = fig.add_subplot(133) 
	rects1 = sub3.bar(ind, sumsBaseC, width, color='b')
	rects2 = sub3.bar(ind + width, sumsImpactC, width, color='r')
	sub3.set_title("Levels of Coherence in Frequency Groups")
	sub3.set_xticks(ind + width / 2)
	sub3.set_xticklabels(("Gamma", "Beta", "Alpha", "Theta", "Delta"))
	sub3.legend((rects1[0], rects2[0]), ('Baseline', 'Post-Impact'))
	
	plt.tight_layout()
	plt.show()
	
	return

