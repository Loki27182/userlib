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
from helper_functions import basic_gaussian_fit, saveAnalysisImage, plot_the_thing
import AnalysisSettings
from lyse_setup import load_data
import os

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
ax_N = fig.add_subplot(1,3,1)
ax_wx = fig.add_subplot(1,3,2)
ax_wz = fig.add_subplot(1,3,3)

try:
    if len(display_variable_info)==0:

        this_variable = display_variable_info[list(display_variable_info.keys())[0]]


        x_u = np.array(range(len(N)))*this_variable['axis_scale']
        N_plot = N
        wx_plot = wx
        wz_plot = wz

        plot_the_thing(ax_N,x_u,N_plot,
                   'Run number',
                   'N ($\\times10^6$)',
                   'Atom Number')
        plot_the_thing(ax_wx,x_u,wx_plot,
                   'Run number',
                   '$\sigma_x$ ($\mu$m)',
                   'Gaussian Width (X)')
        plot_the_thing(ax_wz,x_u,wz_plot,
                   'Run number',
                   '$\sigma_z$ ($\mu$m)',
                   'Gaussian Width (Z)')

        plt.tight_layout()
    elif len(display_variable_info)==1:
        fig = plt.figure()

        ax_N = fig.add_subplot(1,3,1)
        ax_wx = fig.add_subplot(1,3,2)
        ax_wz = fig.add_subplot(1,3,3)

        this_variable = display_variable_info[list(display_variable_info.keys())[0]]

        x = np.array(this_variable['values'])*this_variable['axis_scale']
        x_u = np.array(this_variable['unique_values'])*this_variable['axis_scale']

        N_plot = np.zeros(len(x_u))
        wx_plot = np.zeros(len(x_u))
        wz_plot = np.zeros(len(x_u))
        for ii, x_u_ii in enumerate(x_u):
            N_plot[ii] = np.mean(N[x==x_u_ii])/10**6
            wx_plot[ii] = np.mean(wx[x==x_u_ii])/10**6
            wz_plot[ii] = np.mean(wz[x==x_u_ii])/10**6

        plot_the_thing(ax_N,x_u,N_plot,
                       this_variable['axis_label'],
                       'N ($\\times10^6$)',
                       '')
        plot_the_thing(ax_wx,x_u,wx_plot,
                   this_variable['axis_label'],
                   '$\sigma_x$ ($\mu$m)',
                   '')
        plot_the_thing(ax_wz,x_u,wz_plot,
                   this_variable['axis_label'],
                   '$\sigma_z$ ($\mu$m)',
                   '')

        plt.tight_layout()

        for path in filepaths:
            plt.savefig(path + '.png')
except Exception as ex:
    print('Error plotting')
    print(ex)