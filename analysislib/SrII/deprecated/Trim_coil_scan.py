from lyse import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import scipy.constants as constants
import AnalysisSettings
import SrConstants
from Subroutines.FitFunctions import parabola


camera = AnalysisSettings.Camera

df = data()
dataLength = len(df['run number'])

try:
    BlueMOTShimX = np.array(df["single_gaussian_analysis", "BlueMOTShimX"])
except:
    print('couldn\'t create BlueMOTShimX' )
try:
    BlueMOTShimY = np.array(df["single_gaussian_analysis", "BlueMOTShimY"])
except:
    print('couldn\'t create BlueMOTShimY' )
try:
    BlueMOTShimZ = np.array(df["single_gaussian_analysis", "BlueMOTShimZ"])
except:
    print('couldn\'t create BlueMOTShimZ' )
try:
    N = np.array(df["single_gaussian_analysis", "atomNumber"])
except:
    print('couldn\'t create N' )

if len(np.unique(BlueMOTShimX)) > 1:
    plotData = BlueMOTShimX
    pltTitle = 'X-Trim'
if len(np.unique(BlueMOTShimY)) > 1:
    plotData = BlueMOTShimY
    pltTitle = 'Y-Trim'
if len(np.unique(BlueMOTShimZ)) > 1:
    plotData = BlueMOTShimZ
    pltTitle = 'Z-Trim'


#if len(N)>5:
#    N_min = np.min(N)
#    N_max = np.max(N)
#    dN = N_max - N_min
#    N_cutoff = N_min + dN/2
#    #
#    #N_fit = np.delete(N,np.where(N<N_cutoff))
#    #f_fit = np.delete(BlueMOTLoadTime,np.where(N<N_cutoff))
#    dx = np.max(plotData) - np.min(plotData)
#    #
#    initial_guess = (-dN*2/dx**2,np.average(plotData[np.argmax(N)]),N_max)
#    ##print(initial_guess)
#    #
#    fitresult, fitresult_con = curve_fit(parabola, plotData, N, p0=initial_guess, 
#                                         bounds=([-np.inf, np.min(plotData), N_min], [0, np.max(plotData),N_max + dN]))
#

idx = np.argsort(plotData)
plotData = plotData[idx]
N = N[idx]

fig = plt.figure()
fig.suptitle("Scanning " + pltTitle + " Current")

ax = fig.add_subplot(111)

ax.plot(plotData, N)
#if len(N) > 5:
#    ax.plot(plotData, parabola(plotData, *fitresult))
#    fig.suptitle("Scanning " + pltTitle + " Current: Max at {:1.3f} A".format(fitresult[1]))
ax.set_xlabel("Shim Coil Setting (A)")
ax.set_ylabel("Atom Number (arb)")
#if len(N)>5:
#    ax.set_ylim(0,N_max*1.1)
ax.grid(True)

datapath = df['filepath'][-1].split('\\')

savepath = '\\'.join(datapath[0:-1]) + '\\trim_coil_scan.png'

plt.savefig(savepath)