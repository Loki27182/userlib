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
    ProbeVCOVoltage = np.array(df["single_gaussian_analysis", "ProbeVCOVoltage"])
except:
    print('couldn\'t create ProbeVCOVoltage' )
try:
    N = np.array(df["single_gaussian_analysis", "atomNumber"])
except:
    print('couldn\'t create N' )

idx = np.argsort(ProbeVCOVoltage)
ProbeVCOVoltage = ProbeVCOVoltage[idx]
N = N[idx]

N_min = np.min(N)
N_max = np.max(N)
dN = N_max - N_min
N_cutoff = N_min + dN/2

N_fit = np.delete(N,np.where(N<N_cutoff))
f_fit = np.delete(ProbeVCOVoltage,np.where(N<N_cutoff))
df = np.max(f_fit) - np.min(f_fit)

initial_guess = (-dN*2/df**2,np.average(f_fit[np.argmax(N_fit)]),N_max)
#print(initial_guess)

fitresult, fitresult_con = curve_fit(parabola, f_fit, N_fit, p0=initial_guess, 
                                     bounds=([-np.inf, np.min(f_fit), N_min], [0, np.max(f_fit),N_max + dN]))

fig = plt.figure()
fig.suptitle("Scanning Probe VCO Voltage - Peak @ " + str(fitresult[1]) + " V")

ax = fig.add_subplot(111)

ax.plot(ProbeVCOVoltage, N)
ax.plot(f_fit, parabola(f_fit, *fitresult))
ax.set_xlabel("Blue Beatnote Frequency (MHz)")
ax.set_ylabel("Atom Number (arb)")

