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
    BlueMOTBeatnote = np.array(df["single_gaussian_analysis", "BlueMOTBeatnote"])
except:
    print('couldn\'t create BlueMOTBeatnote' )
try:
    N = np.array(df["single_gaussian_analysis", "atomNumber"])
except:
    print('couldn\'t create N' )

idx = np.argsort(BlueMOTBeatnote)
BlueMOTBeatnote = BlueMOTBeatnote[idx]
N = N[idx]

N_min = np.min(N)
N_max = np.max(N)
dN = N_max - N_min
N_cutoff = N_min + dN/2

N_fit = np.delete(N,np.where(N<N_cutoff))
f_fit = np.delete(BlueMOTBeatnote,np.where(N<N_cutoff))
df1 = np.max(f_fit) - np.min(f_fit)

initial_guess = (-dN*2/df1**2,np.average(f_fit[np.argmax(N_fit)]),N_max)
#print(initial_guess)

fitresult, fitresult_con = curve_fit(parabola, f_fit, N_fit, p0=initial_guess, 
                                     bounds=([-np.inf, np.min(f_fit), N_min], [0, np.max(f_fit),N_max + dN]))

fig = plt.figure()
fig.suptitle("Scanning Blue MOT Beatnote Frequency - Peak @ " + str(fitresult[1]))

ax = fig.add_subplot(111)

ax.plot(BlueMOTBeatnote, N)
ax.plot(f_fit, parabola(f_fit, *fitresult))
ax.set_xlabel("Blue Beatnote Frequency (MHz)")
ax.set_ylabel("Atom Number (arb)")
ax.grid(True)

datapath = df['filepath'][0].split('\\')

savepath = '\\'.join(datapath[0:-1]) + '\\beatnote_scan.png'

plt.savefig(savepath)