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
from helper_functions import basic_gaussian_fit, saveAnalysisImage, plot_the_thing, plot_the_thing_2D
import AnalysisSettings
from lyse_setup import load_data
import os
import shutil
import warnings

warnings.filterwarnings('ignore')

variables, iterated_variables, results, filepaths, first_paths = load_data()
all_var_ranges = [{ name: [np.min(np.array(eval(val.replace('linspace','np.linspace').replace('logspace','np.logspace')))), np.max(np.array(eval(val.replace('linspace','np.linspace').replace('logspace','np.logspace'))))]
                                if not isinstance(eval(val.replace('linspace','np.linspace').replace('logspace','np.logspace')),type('')) 
                                else [0,0]
                            for name, val in Run('\\'.join(filepath)).get_globals_raw().items() 
                        if np.size(np.array(eval(val.replace('linspace','np.linspace').replace('logspace','np.logspace')))) > 1 
                    } 
                    for filepath in first_paths
                ]

#all_var_names = [{name for name in var_range} for var_range in all_var_ranges]
#
#for idx, var_names in enumerate(all_var_names):
#    if idx==0:
#        unique_var_names = var_names
#    else:
#        unique_var_names = unique_var_names | var_names


#display_variable_info = dict()
#for name, val in iterated_variables.items():
#    try:
#        plot_title = AnalysisSettings.variable_info[name]['plot_title']
#        axis_label = AnalysisSettings.variable_info[name]['axis_label']
#        axis_scale = AnalysisSettings.variable_info[name]['scale']
#    except:
#        plot_title = 'Varying ' + name
#        axis_label = name
#        axis_scale = 1
#    display_variable_info[name] = dict()
#    display_variable_info[name]['plot_title'] = plot_title
#    display_variable_info[name]['axis_label'] = axis_label
#    display_variable_info[name]['axis_scale'] = axis_scale
#    display_variable_info[name]['values'] = val
#    display_variable_info[name]['unique_values'] = np.sort(np.unique(val))
#
#N = results['atomNumber']
#wx = results['x_width']
#wz = results['y_width']
#
#plt.rcParams['text.usetex'] = True
#plt.rc('font', family='serif')
#
#fig = plt.figure()
#
#ax_N = fig.add_subplot(1,1,1)
#try:
#    n_sm = variables['Smooth2D'][0]
#except:
#    n_sm = 0
#n_sm = 0
#try:
#    var_0 = display_variable_info[list(display_variable_info.keys())[0]]
#    var_1 = display_variable_info[list(display_variable_info.keys())[1]]
#
#    x = np.array(var_0['values'])*var_0['axis_scale']
#    x_u = np.array(var_0['unique_values'])*var_0['axis_scale']
#    y = np.array(var_1['values'])*var_1['axis_scale']
#    y_u = np.array(var_1['unique_values'])*var_1['axis_scale']
#
#    N_plot = np.zeros([len(y_u),len(x_u)])
#
#
#    for ii, x_u_ii in enumerate(x_u):
#        for jj, y_u_jj in enumerate(y_u):
#            mask = (x==x_u_ii)*(y==y_u_jj)
#            if np.sum(mask)>0:
#                N_plot[jj,ii] = np.mean(N[mask])/10**6
#
#    N_plot[N_plot==0] = np.mean(N_plot[N_plot!=0])
#
#    if n_sm>0:
#        N_plot = gaussian_filter(N_plot,n_sm)
#
#    plot_the_thing_2D(ax_N,fig,y_u,x_u,np.transpose(N_plot),
#                   var_1['axis_label'],
#                   var_0['axis_label'],
#                   'N ($\\times10^6$)')
#
#    plt.tight_layout()
#    for path in filepaths:
#        plt.savefig(path + '.png')
#except Exception as e:
#    print(e)

print('done multi')
