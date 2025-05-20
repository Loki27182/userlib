from lyse import *
import numpy as np
import h5py
import matplotlib.pyplot as plt
from pprint import pp as pprint
from lyse_setup import load_iterated_data

variable_info, result_info, save_paths = load_iterated_data()
visible_results_info = {name: val for name, val in result_info.items() if val['plot_flag']}


if len(variable_info)==1:
    x = variable_info[0]['values']*variable_info[0]['axis_scale']
    x = x.round(decimals=15)

    x_label = variable_info[0]['axis_label']
    pprint(variable_info[0]['range'])
    pprint(variable_info[0]['axis_scale'])
    x_range = variable_info[0]['range']*variable_info[0]['axis_scale']
    x_scale_type = variable_info[0]['loglin']

    figs = dict()
    axs = dict()
    plt.rcParams['text.usetex'] = True
    plt.rc('font', family='serif')
    for name, val in visible_results_info.items():
        
        y = val['values']*val['axis_scale']
        y_label = val['axis_label']
        #y_scale_type = val['loglin']
        multi_name = val['result_type'] + '_' + val['imaging_axis']

        figs[multi_name] = plt.figure(multi_name)
        axs[multi_name] = figs[multi_name].add_subplot(1,1,1)

        x_u = np.unique(x)
        y_u = np.zeros(np.shape(x_u))
        for idx in range(len(x_u)):
            y_u[idx] = np.mean(y[x==x_u[idx]])

        axs[multi_name].plot(x_u,y_u,'--x')
        axs[multi_name].set_xlabel(x_label,fontsize=20)
        axs[multi_name].set_ylabel(y_label,fontsize=20)
        
        axs[multi_name].tick_params(axis='x', labelsize=12)
        axs[multi_name].tick_params(axis='y', labelsize=12)

        axs[multi_name].set_ylim([np.min([0,np.min(y_u)*1.1]),np.max([0,np.max(y_u)*1.1])])
        axs[multi_name].set_xlim(x_range)
        axs[multi_name].grid(True)
        axs[multi_name].set_xscale(x_scale_type)

        plt.tight_layout()
        plt.savefig(save_paths[-1] + multi_name + '.png')

print('done multi')
