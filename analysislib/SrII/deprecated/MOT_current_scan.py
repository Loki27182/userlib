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
     BlueMOTField = np.array(df["single_gaussian_analysis", "BlueMOTField"])
    #blueMOTPower = np.array(df["single_gaussian_analysis","BlueMOTPower"])
except:
    print('couldn\'t create BlueMOTField' )
try:
    N = np.array(df["single_gaussian_analysis", "atomNumber"])
except:
    print('couldn\'t create N' )

idx = np.argsort(BlueMOTField)
BlueMOTField = BlueMOTField[idx]
N = N[idx]
#N_min = np.min(N)
#N_max = np.max(N)
#dN = N_max - N_min
#N_cutoff = N_min + dN/2
#
#N_fit = np.delete(N,np.where(N<N_cutoff))
#f_fit = np.delete(BlueMOTLoadTime,np.where(N<N_cutoff))
#df = np.max(f_fit) - np.min(f_fit)
#
#initial_guess = (-dN*2/df**2,np.average(f_fit[np.argmax(N_fit)]),N_max)
##print(initial_guess)
#
#fitresult, fitresult_con = curve_fit(parabola, f_fit, N_fit, p0=initial_guess, 
#                                     bounds=([-np.inf, np.min(f_fit), N_min], [0, np.max(f_fit),N_max + dN]))
#
fig = plt.figure()
fig.suptitle("Scanning MOT Field")

ax = fig.add_subplot(111)

ax.plot(BlueMOTField, N)
#ax.plot(blueMOTPower,N)

#ax.plot(f_fit, parabola(f_fit, *fitresult))
ax.set_xlabel("MOT Field (G/cm)")
ax.set_ylabel("Atom Number (arb)")
ax.grid(True)

datapath = df['filepath'][0].split('\\')

savepath = '\\'.join(datapath[0:-1]) + '\\MOT_field_scan.png'

plt.savefig(savepath)