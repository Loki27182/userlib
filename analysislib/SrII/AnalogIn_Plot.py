from lyse import *
import matplotlib.pyplot as plt
from matplotlib import rcParams
from pprint import pp as pprint
import numpy as np
import h5py
from scipy.ndimage import gaussian_filter
from scipy.signal import medfilt2d
from matplotlib.patches import Ellipse
from helper_functions import saveAnalysisImage, basic_gaussian_fit
import re as regexp

import AnalysisSettings
import warnings
warnings.filterwarnings('ignore')
#data_series = data()
run_data = data(path)
run = Run(path)

instance_variables = run.get_globals()

field_values = np.array(run.get_trace('field_readout'))

pprint(np.shape(field_values))
plt.rcParams['text.usetex'] = True
plt.rc('font', family='serif')

x_var = field_values[0,:]
y_var = -25*field_values[1,:]
fig= plt.figure(figsize=(4, 3), dpi=200)
axImage = fig.add_subplot(1,1,1)
image = axImage.plot(x_var,y_var)


#    if run_data['FitData']:
#        try:
#            print('Fitting data in ' + camera + ' image...')
#            xData = x_plot
#            yData = np.sum(imageData,0)
#
#            p_x, dp_x = basic_gaussian_fit(x_plot,np.sum(imageData,0))
#            p_y, dp_y = basic_gaussian_fit(np.flip(y_plot),np.sum(imageData,1))
#
#            x_0[camera] = (p_x[1],p_y[1])
#            dx_0[camera] = (dp_x[1],dp_y[1])
#            w[camera] = [p_x[2],p_y[2]]
#            dw[camera] = [dp_x[2],dp_y[2]]
#            a[camera] = [p_x[0],p_y[0]]
#            da[camera] = [dp_x[0],dp_y[0]]
#        except Exception:
#            print('Error fitting data in ' + camera + ' image...')
#            x_0[camera] = (0,0)
#            dx_0[camera] = (0,0)
#            w[camera] = [0,0]
#            dw[camera] = [0,0]
#            a[camera] = [0,0]
#            da[camera] = [0,0]
#
#    print('Plotting ' + camera + ' image...')
#    rcParams.update({'font.size': 6})
#    figs[camera] = plt.figure(figsize=(4, 3), dpi=200)
#    axImage = figs[camera].add_subplot(1,1,1)
#
#    c_min = np.min(imageData)
#    c_max = np.max(imageData)
#    
#    image = axImage.imshow(imageData,extent=[np.min(x_plot),np.max(x_plot),np.min(y_plot),np.max(y_plot)],vmin=c_min,vmax=c_max)
#    
#    #axImage.invert_yaxis()
#    cb = figs[camera].colorbar(image, ax=axImage)
#    cb.set_label('Optical depth',fontsize=14)
#
#    axImage.set_xlabel("X-position ($\mu$m)",fontsize=14)
#    axImage.set_ylabel("Z-position ($\mu$m)",fontsize=14)
#    if run_data['FitData']:
#        axImage.add_patch(Ellipse(xy=x_0[camera], width=4*w[camera][0], height=4*w[camera][1], edgecolor='r', fc='None', lw=1))
#        titleString = ' = {:1.2f} million'.format(atomNumbers[camera]/10**6) + \
#            '\n$x_0$ = {:0.0f} $\mu$m, $\sigma_x$ = {:0.0f} $\mu$m'.format(x_0[camera][0],w[camera][0]) + \
#            '\n$z_0$ = {:0.0f} $\mu$m, $\sigma_z$ = {:0.0f} $\mu$m'.format(x_0[camera][1],w[camera][1])
#    else:
#        titleString = (' = {:.2E}').format(atomNumbers[camera])
#    axImage.title.set_text('N_' + camera + titleString)
#    
#    plt.tight_layout()
#    print('    Done plotting ' + camera + ' image.')
#
#print('Saving data...')
#for camera, N in atomNumbers.items():
#    run.save_result(camera + "/atomNumber", N)
#    if run_data['FitData']:
#        run.save_result(camera + '/x_position', x_0[camera][0]/(1*10**6))
#        run.save_result(camera + '/y_position', x_0[camera][1]/(1*10**6))
#        run.save_result(camera + '/x_width', w[camera][0]/(1*10**6))
#        run.save_result(camera + '/y_width', w[camera][1]/(1*10**6))
#        run.save_result(camera + '/x_fit_N', a[camera][0]*w[camera][0])
#        run.save_result(camera + '/y_fit_N', a[camera][1]*w[camera][1])
#        run.save_result(camera + '/fit_N', (a[camera][1]*w[camera][1]+a[camera][0]*w[camera][0])/2)
#for camera, imageData in densityImages.items():
#    if run_data['SaveImage']:
#        datapath = path.split('\\')
#        #m = path.split('\\')
#        m = datapath[-1].split('_')
#        rep_number = m[-1][0:-3]
#        savepath = '\\'.join(datapath[0:-1]) + '\\' + rep_number + '_density.png'
#        plt.savefig(savepath)
#        saveAnalysisImage(path,'single_shot_analysis',camera,imageData)
#
#print('    Data saved.')
#print('Done') 