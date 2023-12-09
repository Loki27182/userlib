from lyse import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import scipy.constants as constants
import AnalysisSettings
import SrConstants
from Subroutines.FitFunctions import temp_fit


camera = AnalysisSettings.Camera
pixelSize = SrConstants.pixelSizeDict[camera]

df = data()
dataLength = len(df['run number'])
# Get Relevant Data
try:
    TimeOfFlight = np.array(df["single_gaussian_analysis", "TimeOfFlight"])
except:
    print('couldn\'t create TimeOfFlight' )
try:
    widthX = np.array(df["single_gaussian_analysis", "sigma_x"])
except:
    print('couldn\'t create widthX' )
try:
    widthZ = np.array(df["single_gaussian_analysis", "sigma_z"])
except:
    print('couldn\'t create widthZ' )


TimeOfFlight=np.delete(TimeOfFlight,-1)
widthX=np.delete(widthX,-1)
widthZ=np.delete(widthZ,-1)
initial_guess_x=(widthX[0], SrConstants.mass*(widthX[-1]/TimeOfFlight[-1])**2/constants.k)
initial_guess_z=(widthZ[0], SrConstants.mass*(widthZ[-1]/TimeOfFlight[-1])**2/constants.k)
t_fit_x, t_fit_x_con = curve_fit(temp_fit, TimeOfFlight, widthX, p0=initial_guess_x,
                             bounds=([0, 0], [np.inf, np.inf]))
t_fit_z, t_fit_z_con = curve_fit(temp_fit, TimeOfFlight, widthZ, p0=initial_guess_z,
                             bounds=([0, 0], [np.inf, np.inf]))
print(t_fit_x)
print(t_fit_z)
avgTemp=(t_fit_x[1]+t_fit_z[1])/2


fig = plt.figure()
fig.suptitle("$T_X= "+ '{:0.1f}'.format(t_fit_x[1]*1e3) + "$ mK\n$T_Z= "+ '{:0.1f}'.format(t_fit_z[1]*1e3) + "$ mK\n" + r"$T_\mathrm{avg}= " + '{:0.1f}'.format(avgTemp*1e3) + "$ mK", fontsize=12)

#fig.suptitle((pOptX[0] + pOptZ[0])/2, fontsize=70)
ax_x = fig.add_subplot(121)
ax_z = fig.add_subplot(122)

ax_x.plot(TimeOfFlight*1e3, widthX*1e3)
ax_x.plot(TimeOfFlight*1e3, temp_fit(TimeOfFlight, *t_fit_x)*1e3)
ax_x.set_xlabel("Time of Flight (ms)")
ax_x.set_ylabel("$\sigma_X$ (mm)")
ax_x.grid(True)
ax_x.set_ylim((0,np.max([widthX,widthZ])*1.2*1e3))
ax_z.plot(TimeOfFlight*1e3, widthZ*1e3)
ax_z.plot(TimeOfFlight*1e3, temp_fit(TimeOfFlight, *t_fit_z)*1e3)
ax_z.set_xlabel("Time of Flight (ms)")
ax_z.set_ylabel("$\sigma_Z$ (mm)")
ax_z.grid(True)
ax_z.set_ylim((0,np.max([widthX,widthZ])*1.2*1e3))

#ax_z.set_ylabel("width")
fig.tight_layout()

datapath = df['filepath'][0].split('\\')

savepath = '\\'.join(datapath[0:-1]) + '\\temp_measurement.png'

plt.savefig(savepath)
