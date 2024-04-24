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
    N = np.array(df["single_gaussian_analysis", "atomNumber"])
except:
    try:
        N = np.array(df["continuous_fluorescence_single", "atomNumber"])
    except:
        print('couldn\'t create N' )

fig = plt.figure()

ax = fig.add_subplot(111)

ax.plot(N)
ax.set_xlabel("Run number")
ax.set_ylabel("Atom Number (arb)")
ax.set_ylim([np.min([0,np.min(N)*1.1]),np.max([0,np.max(N)*1.1])])
ax.grid(True)

datapath = df['filepath'][0].split('\\')

savepath = '\\'.join(datapath[0:-1]) + '\\continuous_run.png'

plt.savefig(savepath)