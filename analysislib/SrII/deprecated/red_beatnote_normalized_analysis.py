from lyse import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import scipy.constants as constants
import AnalysisSettings
import SrConstants
from Subroutines.FitFunctions import gauss, lorentzian_with_offset


camera = AnalysisSettings.Camera

df = data()
dataLength = len(df['run number'])

try:
     RedCoolingBeatnote = np.array(df["single_gaussian_analysis", "RedCoolingBeatnote"])
except:
    print('couldn\'t create t' )
try:
    N = np.array(df["single_gaussian_analysis", "atomNumber"])
except:
    print('couldn\'t create N' )

idx = np.argsort(RedCoolingBeatnote)
RedCoolingBeatnote = RedCoolingBeatnote[idx]
N = N[idx]

#idx_dip = np.argmin(N)
#
#a = np.min(N)-np.max(N)
#x0 = RedCoolingBeatnote[idx_dip]
#offset = np.max(N)
#width = 20
#
#p_opt, p_cov = curve_fit(gauss, RedCoolingBeatnote, N, p0=(a,x0,width,offset), bounds=([-np.inf, np.min(RedCoolingBeatnote), 0, 0], [0, np.max(RedCoolingBeatnote), np.inf, 2]))
#RedCoolingBeatnote_fit = np.linspace(np.min(RedCoolingBeatnote),np.max(RedCoolingBeatnote),200)
#N_fit = gauss(RedCoolingBeatnote_fit,*p_opt)
#
#dp = np.sqrt(np.diag(p_cov))

fig = plt.figure()
#fig.suptitle("Center = {:0.2f}({:0.0f}) MHz, width = {:0.2f}({:0.0f}) MHz".format(p_opt[1],dp[1]*100,p_opt[2],dp[2]*100))

ax = fig.add_subplot(111)

ax.plot(RedCoolingBeatnote, N*100)
#ax.plot(RedCoolingBeatnote_fit, N_fit*100)
#ax.plot(blueMOTPower,N)

#ax.plot(f_fit, parabola(f_fit, *fitresult))
ax.set_xlabel("Red MOT beatnote frequency (MHz)")
ax.set_ylabel("Atom number (arb)")
#ax.set_ylim([0,110])
ax.grid(True)

datapath = df['filepath'][0].split('\\')

savepath = '\\'.join(datapath[0:-1]) + '\\red_response.png'

plt.savefig(savepath)