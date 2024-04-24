from lyse import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import scipy.constants as constants
import AnalysisSettings
import SrConstants
from Subroutines.FitFunctions import parabola
from scipy.ndimage import gaussian_filter


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

if len(np.unique(BlueMOTShimX)) > 1 and len(np.unique(BlueMOTShimY)) > 1 :
    plotDataX = BlueMOTShimX
    plotDataY = BlueMOTShimY
    xLabel = 'X-Trim Current (A)'
    yLabel = 'Y-Trim Current (A)'
    pltTitle = 'XY-Trim'
if len(np.unique(BlueMOTShimX)) > 1 and len(np.unique(BlueMOTShimZ)) > 1 :
    plotDataX = BlueMOTShimX
    plotDataY = BlueMOTShimZ
    xLabel = 'X-Trim Current (A)'
    yLabel = 'Z-Trim Current (A)'
    pltTitle = 'XZ-Trim'
if len(np.unique(BlueMOTShimY)) > 1 and len(np.unique(BlueMOTShimZ)) > 1 :
    plotDataX = BlueMOTShimY
    plotDataY = BlueMOTShimZ
    xLabel = 'Y-Trim Current (A)'
    yLabel = 'Z-Trim Current (A)'
    pltTitle = 'YZ-Trim'


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
##

plotDataX_u = np.unique(plotDataX)
plotDataY_u = np.unique(plotDataY)
nData = np.zeros((len(plotDataY_u),len(plotDataX_u)),N[0])

for ii, X_u in np.ndenumerate(plotDataX_u):
    for jj, Y_u in np.ndenumerate(plotDataY_u):
        mask = np.logical_and(plotDataX==X_u,plotDataY==Y_u)
        if mask.any():
            nData[jj,ii] = np.mean(N[mask])

nData = gaussian_filter(nData, .01)
ind = np.unravel_index(np.argmax(nData, axis=None), nData.shape)

xOpt = plotDataX_u[ind[1]]
yOpt = plotDataY_u[ind[0]]

fig = plt.figure()
ax = fig.add_subplot(111)

#ax.plot(plotData, N)
imagePlot = ax.imshow(nData, 
                      vmin=np.min(nData[nData>0]), vmax=np.max(nData),
                      extent = (np.min(plotDataX_u),np.max(plotDataX_u),np.max(plotDataY_u),np.min(plotDataY_u)))
ax.plot(xOpt,yOpt,'x')
ax.set_xlabel(xLabel)
ax.set_ylabel(yLabel)
fig.colorbar(imagePlot, ax=ax)
fig.suptitle("Scanning " + pltTitle + " Current: Max at ({:1.3f},{:1.3f}) A".format(xOpt,yOpt))

ax.grid(True)

datapath = df['filepath'][-1].split('\\')

savepath = '\\'.join(datapath[0:-2]) + '\\{:0.0f}_trim_coil_2D_scan.png'.format(df['sequence_index'][-1])

plt.savefig(savepath)