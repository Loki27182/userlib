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
from helper_functions import basic_gaussian_fit, saveAnalysisImage, plot_the_thing,plot_the_thing_2D
import AnalysisSettings
from lyse_setup import load_data
import os
import shutil
import warnings

warnings.filterwarnings('ignore')

variables, iterated_variables, results, filepaths, all_iterated_variables = load_data()

display_variable_info = dict()
for name, val in iterated_variables.items():
    try:
        plot_title = AnalysisSettings.variable_info[name]['plot_title']
        axis_label = AnalysisSettings.variable_info[name]['axis_label']
        axis_scale = AnalysisSettings.variable_info[name]['scale']
    except:
        plot_title = 'Varying ' + name
        axis_label = name
        axis_scale = 1
    display_variable_info[name] = dict()
    display_variable_info[name]['plot_title'] = plot_title
    display_variable_info[name]['axis_label'] = axis_label
    display_variable_info[name]['axis_scale'] = axis_scale
    display_variable_info[name]['values'] = val
    display_variable_info[name]['unique_values'] = np.sort(np.unique(val))

N = results['atomNumber']
wx = results['x_width']
wz = results['y_width']

plt.rcParams['text.usetex'] = True
plt.rc('font', family='serif')

fig = plt.figure()

ax_N = fig.add_subplot(3,1,1)
ax_wx = fig.add_subplot(3,1,2)
ax_wz = fig.add_subplot(3,1,3)
try:
    n_sm = variables['Smooth2D'][0]
except:
    n_sm = 0
#n_sm = 10
try:
    var_0 = display_variable_info[list(display_variable_info.keys())[0]]
    var_1 = display_variable_info[list(display_variable_info.keys())[1]]

    x = np.array(var_0['values'])*var_0['axis_scale']
    x_u = np.array(var_0['unique_values'])*var_0['axis_scale']
    y = np.array(var_1['values'])*var_1['axis_scale']
    y_u = np.array(var_1['unique_values'])*var_1['axis_scale']

    N_plot = np.zeros([len(y_u),len(x_u)])
    wx_plot = np.zeros([len(y_u),len(x_u)])
    wz_plot = np.zeros([len(y_u),len(x_u)])


    for ii, x_u_ii in enumerate(x_u):
        for jj, y_u_jj in enumerate(y_u):
            mask = (x==x_u_ii)*(y==y_u_jj)
            if np.sum(mask)>0:
                N_plot[jj,ii] = np.mean(N[mask])/10**6
                wx_plot[jj,ii] = np.mean(wx[mask])*10**3
                wz_plot[jj,ii] = np.mean(wz[mask])*10**3

    wx_plot[N_plot==0] = np.mean(wx_plot[N_plot!=0])
    wz_plot[N_plot==0] = np.mean(wz_plot[N_plot!=0])
    N_plot[N_plot==0] = np.mean(N_plot[N_plot!=0])

    if n_sm>0:
        N_plot = gaussian_filter(N_plot,n_sm)
        wx_plot = gaussian_filter(wx_plot,n_sm)
        wz_plot = gaussian_filter(wz_plot,n_sm)

    plot_the_thing_2D(ax_N,fig,np.log10(y_u),np.log10(x_u),np.transpose(N_plot),
                   var_1['axis_label'],
                   var_0['axis_label'],
                   'N ($\\times10^6$)','log scale','log scale')
    plot_the_thing_2D(ax_wx,fig,np.log10(y_u),np.log10(x_u),np.transpose(wx_plot),
               var_1['axis_label'],
               var_0['axis_label'],
               '$\sigma_x$ (mm)','log scale','log scale')
    plot_the_thing_2D(ax_wz,fig,np.log10(y_u),np.log10(x_u),np.transpose(wz_plot),
               var_1['axis_label'],
               var_0['axis_label'],
               '$\sigma_z$ (mm)','log scale','log scale')

    plt.tight_layout()
    for path in filepaths:
        plt.savefig(path + '.png')
        plt.savefig('G:\\My Drive\\SrII\\Misc\\temp_log_files\\temp.png')
except Exception as e:
    print(e)

