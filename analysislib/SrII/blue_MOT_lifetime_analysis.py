from lyse import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import scipy.constants as constants
import AnalysisSettings
import SrConstants
from Subroutines.FitFunctions import super_exp_decay, exp_decay


camera = AnalysisSettings.Camera

df = data()
dataLength = len(df['run number'])

try:
    BlueMOTHoldTime = np.array(df["single_gaussian_analysis", "BlueMOTHoldTime"])
except:
    print('couldn\'t create TimeOfFlight' )
try:
    N = np.array(df["single_gaussian_analysis", "atomNumber"])
except:
    print('couldn\'t create N' )

idx = np.argsort(BlueMOTHoldTime)
BlueMOTHoldTime = BlueMOTHoldTime[idx]
N = N[idx]

N_fit = N/np.max(N)
f_fit = BlueMOTHoldTime


initial_guess = (N_fit[0],.7,1,N_fit[-1])
#print(initial_guess)

fitresult1, fitresult_con1 = curve_fit(super_exp_decay, f_fit, N_fit, p0=initial_guess, 
                                     bounds=([0, 0, 0, -np.Inf], [np.Inf, np.Inf, np.Inf, np.Inf]))

fitresult2, fitresult_con2 = curve_fit(exp_decay, f_fit, N_fit, p0=initial_guess[0:3], 
                                     bounds=([0, 0, -np.Inf], [np.Inf, np.Inf, np.Inf]))

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": "Helvetica",
})

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

fig = plt.figure()
fig.suptitle("Blue MOT lifetime",fontsize=16)

ax = fig.add_subplot(111)

ax.plot(f_fit, exp_decay(f_fit, *fitresult2) - fitresult1[3],label=r'Exponential fit: $N = N_0 e^{-t/\tau}$: $\tau = ' + "{:.2f}".format(fitresult2[1]) + r'$ s',color=colors[1])
ax.plot(f_fit, super_exp_decay(f_fit, *fitresult1) - fitresult1[3],label=r'Super-exponential fit: $N = N_0 e^{-(t/\tau)^\alpha}$: $\tau = ' + "{:.2f}".format(fitresult1[1]) + r'$ s, $\alpha = ' + "{:.2f}".format(fitresult1[2]) + r'$',color=colors[2])
ax.plot(BlueMOTHoldTime, N_fit - fitresult1[3],marker='x',linestyle='None',label='Data',color=colors[0])
ax.set_xlabel("Time (s)",fontsize=12)
ax.set_ylabel("Atom Number (arb)",fontsize=12)
ax.grid(True)
ax.legend(("Exponential Fit: ", "Super-exponential Fit:", "Data"))

handles, labels = ax.get_legend_handles_labels()
labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
ax.legend(handles, labels,fontsize=12)

datapath = df['filepath'][0].split('\\')

savepath = '\\'.join(datapath[0:-1]) + '\\blue_MOT_lifetime.png'

plt.savefig(savepath)