from lyse import *
import numpy as np
import h5py
import matplotlib.pyplot as plt
from pprint import pp as pprint
from helper_functions import load_iterated_data

variable_info, result_info, save_paths = load_iterated_data()
visible_results_info = {name: val for name, val in result_info.items() if val['plot_flag']}


try:
    if len(variable_info)==1:
        if variable_info[0]['name'] != 'Time':
            x = variable_info[0]['values']*variable_info[0]['axis_scale']
            x = x.round(decimals=15)
            x_range = variable_info[0]['range']*variable_info[0]['axis_scale']
        else:
            x = variable_info[0]['values']
            x_range = variable_info[0]['range']
        x_label = variable_info[0]['axis_label']
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
            try:
                axs[multi_name].set_ylim([np.min([0,np.min(y_u)*1.1]),np.max([0,np.max(y_u)*1.1])])
            except:
                pass
            try:
                axs[multi_name].set_xlim(x_range)
            except:
                pass
            axs[multi_name].grid(True)
            axs[multi_name].set_xscale(x_scale_type)
            plt.tight_layout()
            plt.savefig(save_paths[-1] + multi_name + '.png')
    if len(variable_info)==2:
        x = variable_info[0]['values']*variable_info[0]['axis_scale']
        x_range = variable_info[0]['range']
        x_label = variable_info[0]['axis_label']
        x_scale_type = variable_info[0]['loglin']

        y = variable_info[1]['values']*variable_info[1]['axis_scale']
        y_range = variable_info[1]['range']
        y_label = variable_info[1]['axis_label']
        y_scale_type = variable_info[1]['loglin']

        figs = dict()
        axs = dict()
        plt.rcParams['text.usetex'] = True
        plt.rc('font', family='serif')
        for name, val in visible_results_info.items():
            z = val['values']*val['axis_scale']
            z_label = val['axis_label']
            #y_scale_type = val['loglin']
            multi_name = val['result_type'] + '_' + val['imaging_axis']
            figs[multi_name] = plt.figure(multi_name)
            axs[multi_name] = figs[multi_name].add_subplot(1,1,1)
            x_u = np.unique(x)
            print(len(x_u))
            y_u = np.unique(y)
            print(len(y_u))
            z_u = np.zeros([len(y_u),len(x_u)])
            for idx_x in range(len(x_u)):
                for idx_y in range(len(y_u)):
                    mask = np.logical_and(x==x_u[idx_x],y==y_u[idx_y]);
                    if any(mask):
                        z_u[idx_y,idx_x] = np.mean(z[mask])
            c_min = np.min(z_u)
            c_max = np.max(z_u)
            im = axs[multi_name].imshow(z_u,extent=[np.min(x_u),np.max(x_u),np.max(y_u),np.min(y_u)],vmin=c_min,vmax=c_max,aspect=(np.max(x_u)-np.min(x_u))/(np.max(y_u)-np.min(y_u))/1.25)

            cb = figs[multi_name].colorbar(im, ax=axs[multi_name])
            cb.set_label(z_label,fontsize=14)

            axs[multi_name].set_xlabel(x_label,fontsize=14)
            axs[multi_name].set_ylabel(y_label,fontsize=14)
            #axs[multi_name].plot(x_u,y_u,'--x')
            #axs[multi_name].set_xlabel(x_label,fontsize=20)
            #axs[multi_name].set_ylabel(y_label,fontsize=20)
            #
            #axs[multi_name].tick_params(axis='x', labelsize=12)
            #axs[multi_name].tick_params(axis='y', labelsize=12)
    #
            #try:
            #    axs[multi_name].set_ylim([np.min([0,np.min(y_u)*1.1]),np.max([0,np.max(y_u)*1.1])])
            #except:
            #    pass
            #try:
            #    axs[multi_name].set_xlim(x_range)
            #except:
            #    pass
            #axs[multi_name].grid(True)
            #axs[multi_name].set_xscale(x_scale_type)
            plt.tight_layout()
            plt.savefig(save_paths[-1] + multi_name + '.png')
except:
    pass

print('done multi')
