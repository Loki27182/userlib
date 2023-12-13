from lyse import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import scipy.constants as constants
import AnalysisSettings
import SrConstants
#from Subroutines.FitFunctions import linear_y_offset

def linear_with_saturation(x, *p):
    m, ysat = p
    y = m*x
    y[y>ysat] = ysat
    return y

camera = AnalysisSettings.Camera

df = data()
dataLength = len(df['run number'])

exposure = np.array(df['camera_linearity_analysis_single', 'n_max'])
PulseDuration = np.array(df['camera_linearity_analysis_single', 'PulseDuration'])*1e6

idx = np.argsort(PulseDuration)
PulseDuration = PulseDuration[idx]
exposure = exposure[idx]
idx_max = np.argmax(exposure)
exp_max = exposure[idx_max]

p_opt, p_cov = curve_fit(linear_with_saturation, PulseDuration, exposure, p0=(exp_max/idx_max,2**16))
exposure_fit = linear_with_saturation(PulseDuration, *p_opt)
residuals = exposure - exposure_fit
ss_res = np.sum(residuals**2)
ss_tot = np.sum((exposure - np.mean(exposure))**2)
r_square = 1-(ss_res/(exposure.size-2))/(ss_tot/(exposure.size-1))

fig = plt.figure()
plt.rcParams['text.usetex'] = True



ax = fig.add_subplot(111)

ax.plot(PulseDuration, exposure,'x')
ax.plot(PulseDuration, exposure_fit,'--')
ax.set_xlabel('Pulse Duration ($\mu$s)')
ax.set_ylabel('Average Pixel Value')
ax.grid(True)
ax.title.set_text('CCD Response\nSlope = ' + '{:0.2f}'.format(p_opt[0]) + ', $R^2$ = ' + '{:0.4f}'.format(r_square))
# ', Offset = ' + '{:0.2f}'.format(p_opt[1]) + 


datapath = df['filepath'][0].split('\\')

savepath = '\\'.join(datapath[0:-1]) + '\\linear_fit.png'

plt.savefig(savepath)