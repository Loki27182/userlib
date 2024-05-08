from lyse import *
import numpy as np
import h5py
import matplotlib.pyplot as plt
from pprint import pp as pprint
import scipy.constants as constants
from matplotlib.widgets import Cursor, Slider, CheckButtons, TextBox, Button
from scipy.ndimage import gaussian_filter
from scipy.signal import medfilt2d
from time import perf_counter as pc
import matplotlib.patches as patches
from helper_functions import basic_gaussian_fit, saveAnalysisImage, temp_fit, expansion_TOF, freefall_fit
import AnalysisSettings
from lyse_setup import load_data
import os

import warnings

warnings.filterwarnings('ignore')

variables, iterated_variables, results, filepaths = load_data()

display_variable_info = dict()
t = iterated_variables['TimeOfFlight']
N = results['atomNumber']
w_x = results['x_width']
w_z = results['y_width']
r_x = results['x_position']
r_z = results['y_position']

t_plot = np.sort(np.unique(t))

N_plot = np.array([np.mean(N[t==t_i])/10**6 for t_i in t_plot])
w_x_plot = np.array([np.mean(w_x[t==t_i])/10**6 for t_i in t_plot])
w_z_plot = np.array([np.mean(w_z[t==t_i])/10**6 for t_i in t_plot])
r_x_plot = np.array([np.mean(r_x[t==t_i])/10**6 for t_i in t_plot])
r_z_plot = np.array([np.mean(r_z[t==t_i])/10**6 for t_i in t_plot])

plt.rcParams['text.usetex'] = True
plt.rc('font', family='serif')

fig = plt.figure()
ax_N = fig.add_subplot(1,3,1)
ax_w = fig.add_subplot(1,3,2)
ax_r = fig.add_subplot(1,3,3)

ax_N.plot(t_plot*10**3,N_plot,'--x')
ax_N.grid(True)
ax_N.set_ylim([0,25])
ax_N.set_xlabel('Time of flight (ms)',fontsize=14)
ax_N.set_ylabel('Atom number ($\\times 10^6$)',fontsize=14)

t_fit = np.linspace(0,np.max(t_plot),200)
[p, dp, w_fit] = temp_fit(t_plot,w_z_plot/10**6,t_fit)
w_fit = w_fit*10**6

[p2, dp2, w_fit2] = temp_fit(t_plot,w_x_plot/10**6,t_fit)
w_fit2 = w_fit2*10**6

line_wx, = ax_w.plot(t_plot*10**3,w_x_plot,'x',label='X-Axis')
line_wz, = ax_w.plot(t_plot*10**3,w_z_plot,'x',label='Z-Axis')
line_wf, = ax_w.plot(t_fit*10**3,w_fit,'--',label='$T_{\mathrm{fit}-z} = ' + '{:1.2f}'.format(p[1]*10**6) + '$ $\mu$K, $\sigma_0 = ' + '{:1.0f}'.format(p[0]*10**6) + '$ $\mu$m')
line_wf2, = ax_w.plot(t_fit*10**3,w_fit2,'--',label='$T_{\mathrm{fit}-x} = ' + '{:1.2f}'.format(p2[1]*10**6) + '$ $\mu$K, $\sigma_0 = ' + '{:1.0f}'.format(p2[0]*10**6) + '$ $\mu$m')
ax_w.grid(True)
ax_w.set_ylim([0,500])
ax_w.set_xlabel('Time of flight (ms)',fontsize=14)
ax_w.set_ylabel('Cloud widths ($\mu$m)',fontsize=14)
ax_w.legend(handles=[line_wx,line_wz,line_wf,line_wf2],fontsize=12)

[p_g, dp_g, r_fit] = freefall_fit(t_plot,r_z_plot/10**6,t_fit)
r_fit = r_fit*10**6

line_rx, = ax_r.plot(t_plot*10**3,r_x_plot,'x',label='X-Axis')
line_rz, = ax_r.plot(t_plot*10**3,r_z_plot,'x',label='Z-Axis')
labelText = '$g_{\mathrm{fit}} = ' + '{:1.2f}'.format(p_g[1]) + '$ $\\frac{\mathrm{m}}{\mathrm{s}}$'
line_rf, = ax_r.plot(t_fit*10**3,r_fit,'--',label=labelText)

ax_r.grid(True)
ax_r.set_ylim([-1500,300])
ax_r.set_xlabel('Time of flight (ms)',fontsize=14)
ax_r.set_ylabel('Cloud positions ($\mu$m)',fontsize=14)
ax_r.legend(handles=[line_rx,line_rz,line_rf],fontsize=12)

plt.tight_layout()

if len(filepaths)>0:
    plt.savefig(filepaths[-1] + '.png')