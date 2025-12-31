from lyse import *
import matplotlib.pyplot as plt
from pprint import pp as pprint
import numpy as np
import h5py
from scipy.ndimage import gaussian_filter
from scipy.signal import medfilt2d
import scipy.constants as constants
from matplotlib.widgets import Cursor, Slider, CheckButtons, TextBox, Button
from time import perf_counter as pc
from matplotlib.patches import Ellipse
from helper_functions import saveAnalysisImage, basic_gaussian_fit
import re as regexp

import AnalysisSettings
import warnings
warnings.filterwarnings('ignore')
data_series = data()
run_data = data(path)
run = Run(path)

variables = {name: data_series[name].values for name, value in run.get_globals().items()}
iterated_variables = {name: value for name, value in variables.items() if len(value)>1 and len(value)==len(np.unique(value))}
static_variables = {name: value[0] for name, value in variables.items() if not (len(value)>1 and len(value)==len(np.unique(value)))}

pixel_size = AnalysisSettings.camera['GH']['pixel_size']
sensor_size = AnalysisSettings.camera['GH']['sensor_size']
mass = AnalysisSettings.Sr['mass']
sigma0 = AnalysisSettings.Sr['sigma0']

if 'ROI' in variables.keys():
    if run_data['ROI'] in AnalysisSettings.ROI.keys():
        ROI = AnalysisSettings.ROI[run_data['ROI']]
    else:
        matches = regexp.findall('\[(\d+),(\d+),(\d+),(\d+)\]',run_data['ROI'])
        
        if len(matches)==1 and len(matches[0])==4:
            ROI_0 = np.array([int(match) for match in matches[0]])
            if any(ROI_0 < 0) or any(ROI_0[0:1] >= sensor_size[0]) or any(ROI_0[2:3] >= sensor_size[1]):
                print('ROI out of range. Turning off')
                ROI = []
            else:
                ROI = ROI_0
        else:
            ROI = []
else:
    ROI = []

gaussian_filter_size = AnalysisSettings.filters['gaussian']['large']
median_filter_size = AnalysisSettings.filters['median']['small']
binning_size = AnalysisSettings.filters['binning']['none']

imaging_types = []
if ('horizontal', 'absorption', 'atoms','CLASS') in run_data.index:
    imaging_types.append('absorption')
elif ('horizontal', 'fluorescence', 'atoms','CLASS') in run_data.index:
    imaging_types.append('fluorescence')

print('Detected Imaging Types:')
for name in imaging_types:
    print('    ' + name)

densityImages = dict()
atomNumbers = dict()
if 'absorption' in imaging_types:
    print('Processing absorption image...')
    atomImage = run.get_image('horizontal','absorption','atoms').astype('float') - run.get_image('horizontal','absorption','background').astype('float')
    refImage = run.get_image('horizontal','absorption','reference').astype('float') - run.get_image('horizontal','absorption','background').astype('float')
    refNorm = refImage.copy()
    atomNorm = atomImage.copy()

    if len(ROI)>0:
        refNorm[ROI[2]:ROI[3],ROI[0]:ROI[1]] = 0
        atomNorm[ROI[2]:ROI[3],ROI[0]:ROI[1]] = 0
        atomImage = atomImage[ROI[2]:ROI[3],ROI[0]:ROI[1]]
        refImage = refImage[ROI[2]:ROI[3],ROI[0]:ROI[1]]
        if 'NormalizeProbe' in variables.keys() and run_data['NormalizeProbe']:
            print('    Normalizing probe...')
            refImage = refImage*np.sum(atomNorm)/np.sum(refNorm)

    atomImage = np.clip(medfilt2d(atomImage,median_filter_size),1.0,np.Inf)
    refImage = np.clip(medfilt2d(refImage,median_filter_size),1.0,np.Inf)
    
    densityImages['absorption'] = gaussian_filter(np.log(refImage/atomImage),gaussian_filter_size)

    atomNumbers['absorption'] = np.sum(densityImages['absorption'])*(pixel_size**2)/sigma0

    print('    Absorption image processed.')

elif 'fluorescence' in imaging_types:
    print('Processing fluorescence image...')
    atomImage = run.get_image('horizontal','fluorescence','atoms').astype('float') - run.get_image('horizontal','fluorescence','background').astype('float')
    atomImage = medfilt2d(atomImage,median_filter_size)
    
    if len(ROI)>0:
        atomImage = atomImage[ROI[2]:ROI[3],ROI[0]:ROI[1]]
        
    densityImages['fluorescence'] = gaussian_filter(atomImage,gaussian_filter_size)
    atomNumbers['fluorescence'] = np.sum(densityImages['fluorescence'])

    print('    Fluorescence image processed.')


plt.rcParams['text.usetex'] = True
plt.rc('font', family='serif')
figs = dict()
x_0 = dict()
dx_0 = dict()
w = dict()
dw = dict()

for imageType, imageData in densityImages.items():
    plot_size = np.shape(imageData)

    x_plot = np.arange(plot_size[1])*pixel_size*10**6
    y_plot = np.arange(plot_size[0])*pixel_size*10**6
    x_plot -= np.mean(x_plot)
    y_plot -= np.mean(y_plot)

    if run_data['FitData']:
        print('Fitting data in ' + imageType + ' image...')
        xData = x_plot
        yData = np.sum(imageData,0)
        
        p_x, dp_x = basic_gaussian_fit(x_plot,np.sum(imageData,0))
        p_y, dp_y = basic_gaussian_fit(np.flip(y_plot),np.sum(imageData,1))

        x_0[imageType] = (p_x[1],p_y[1])
        dx_0[imageType] = (dp_x[1],dp_y[1])
        w[imageType] = [p_x[2],p_y[2]]
        dw[imageType] = [dp_x[2],dp_y[2]]

    print('Plotting ' + imageType + ' image...')
    figs[imageType] = plt.figure(figsize=(4, 3), dpi=200)
    axImage = figs[imageType].add_subplot(1,1,1)

    c_min = np.min(imageData)
    c_max = np.max(imageData)
    
    image = axImage.imshow(imageData,extent=[np.min(x_plot),np.max(x_plot),np.min(y_plot),np.max(y_plot)],vmin=c_min,vmax=c_max)
    
    #axImage.invert_yaxis()
    cb = figs[imageType].colorbar(image, ax=axImage)
    cb.set_label('Optical depth',fontsize=14)

    axImage.set_xlabel("X-position ($\mu$m)",fontsize=14)
    axImage.set_ylabel("Z-position ($\mu$m)",fontsize=14)
    if run_data['FitData']:
        axImage.add_patch(Ellipse(xy=x_0[imageType], width=4*w[imageType][0], height=4*w[imageType][1], edgecolor='r', fc='None', lw=1))
        titleString = '$N$ = {:1.2f} million'.format(atomNumbers[imageType]/10**6) + \
            '\n$x_0$ = {:0.0f} $\mu$m, $\sigma_x$ = {:0.0f} $\mu$m'.format(x_0[imageType][0],w[imageType][0]) + \
            '\n$z_0$ = {:0.0f} $\mu$m, $\sigma_z$ = {:0.0f} $\mu$m'.format(x_0[imageType][1],w[imageType][1])
    else:
        titleString = '$N$ = {:.2E}'.format(atomNumbers[imageType])
    axImage.title.set_text(titleString)
    
    print('    Done plotting ' + imageType + ' image.')

print('Saving data...')
for imageType in atomNumbers.keys():
    run.save_result(imageType + "/atomNumber", atomNumbers[imageType])
    if run_data['FitData']:
        run.save_result(imageType + '/x_position', x_0[imageType][0]/1*10**6)
        run.save_result(imageType + '/y_position', x_0[imageType][1]/1*10**6)
        run.save_result(imageType + '/x_width', w[imageType][0]/1*10**6)
        run.save_result(imageType + '/y_width', w[imageType][1]/1*10**6)
for imageType, imageData in densityImages.items():
    if run_data['SaveImage']:
        saveAnalysisImage(path,'single_shot_analysis',imageType,imageData)

print('    Data saved.')
print('Done') 