from lyse import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import scipy.constants as constants
import AnalysisSettings
import SrConstants
from Subroutines.FitFunctions import lorentzian


camera = AnalysisSettings.Camera

df = data()
dataLength = len(df['run number'])

dfdV = AnalysisSettings.dfdV

try:
    ProbeDetuningVoltage = np.array(df["single_gaussian_analysis", "ProbeVCOVoltage"])
except:
    print('couldn\'t create ProbeDetuningVoltage' )
try:
    N = np.array(df["single_gaussian_analysis", "atomNumber"])
except:
    print('couldn\'t create N' )

p_opt, p_cov = curve_fit(lorentzian, ProbeDetuningVoltage, N, p0=(np.max(N),np.mean(ProbeDetuningVoltage),.2), bounds=([0,np.min(ProbeDetuningVoltage),0], [np.inf, np.max(ProbeDetuningVoltage), np.inf]))
center = p_opt[1]
#
fig = plt.figure()
fig.suptitle("Scanning Blue MOT Beatnote Frequency - Peak @ {:1.3f}V = {:1.3f}MHz".format(p_opt[1],p_opt[1]*dfdV))

ax = fig.add_subplot(111)

ax.plot(ProbeDetuningVoltage*dfdV, N,'x')
ax.plot(ProbeDetuningVoltage*dfdV,lorentzian(ProbeDetuningVoltage, *p_opt),'--')
#ax.plot(f_fit, parabola(f_fit, *fitresult))
ax.set_xlabel("Frequency (MHz)")
ax.set_ylabel("Atom Number (arb)")

ax.grid(True)

datapath = df['filepath'][0].split('\\')

savepath = '\\'.join(datapath[0:-1]) + '\\probe_scan.png'

plt.savefig(savepath)