import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.optimize import curve_fit
from Subroutines.FitFunctions import exp_decay

T = np.insert(np.insert(np.arange(300,430,10),0,275),0,250)
N = np.array([-.0196,.0356,0.208,0.375,0.578,0.871,1.31,1.61,2.17,3.02,3.8,4.75,6.2,7.62,9.58])*10
date = '2023-10-31'

fitresult, p_cov_z = curve_fit(exp_decay, T[1:], N[1:], p0=(.00037,-41,0), bounds=([0, -np.inf, -1e-16], [np.inf,0 , 1e-16]))
print(fitresult)

fig = plt.figure()
fig.suptitle("Atom Number vs Oven Temperature")

ax = fig.add_subplot(111)

ax.plot(T, N,'x')
ax.plot(T,exp_decay(T, *fitresult),'--')
#ax.plot(f_fit, parabola(f_fit, *fitresult))
ax.set_xlabel("Oven temperature ($^\circ$C)")
ax.set_ylabel("Atom Number (millions)")
ax.grid(True)
ax.set_ylim((-5,100))
ax.set_xlim((240,440))
ax.legend({'Exponential Fit','Data'})

x_major_ticks = np.arange(240, 441, 20)
x_minor_ticks = np.arange(240, 441, 5)
y_major_ticks = np.arange(0, 101, 20)
y_minor_ticks = np.arange(-5,101, 5)

ax.set_xticks(x_major_ticks)
ax.set_xticks(x_minor_ticks, minor=True)
ax.set_yticks(y_major_ticks)
ax.set_yticks(y_minor_ticks, minor=True)

ax.grid(which='both')

ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)

fig.show()

if input('Save (y/n)?: ').lower()=='y':
    savepath = 'D:\\labscript\\Experiments\\SrMain\\basic_blue_MOT\\' + date[0:4] + '\\' + date[5:7] + '\\' + date[8:10] + '\\oven_temp_plot.png'
    fig.savefig(savepath)
