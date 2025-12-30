from lyse import *
import matplotlib.pyplot as plt
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

pixel_size = {}
sensor_size = {}
quantum_efficiency = {}
other_losses = {}
focal_length = {}
aperture_diameter = {}
solid_angle_fraction = {}
total_efficiency = {}
transpose_image = {}
rotate_image = {}
pixel_size['xz'] = np.array(AnalysisSettings.camera['GH']['pixel_size'])*AnalysisSettings.camera['GH']['magnification']
sensor_size['xz'] = np.array(AnalysisSettings.camera['GH']['sensor_size'])
quantum_efficiency['xz'] = np.array(AnalysisSettings.camera['GH']['quantum_efficiency'])
other_losses['xz'] = np.array(AnalysisSettings.camera['GH']['losses'])
focal_length['xz'] = np.array(AnalysisSettings.camera['GH']['focal_length'])
aperture_diameter['xz'] = np.array(AnalysisSettings.camera['GH']['aperture_diameter'])
solid_angle_fraction['xz'] = np.pi*(aperture_diameter['xz']/2)**2/(4*np.pi*focal_length['xz']**2)
total_efficiency['xz'] = solid_angle_fraction['xz']*quantum_efficiency['xz']*(1-other_losses['xz'])
transpose_image['xz'] = np.array(AnalysisSettings.camera['GH']['transpose'])
rotate_image['xz'] = np.array(AnalysisSettings.camera['GH']['rotate'])
pixel_size['yz'] = np.array(AnalysisSettings.camera['Blackfly']['pixel_size'])*AnalysisSettings.camera['Blackfly']['magnification']
sensor_size['yz'] = np.array(AnalysisSettings.camera['Blackfly']['sensor_size'])
quantum_efficiency['yz'] = np.array(AnalysisSettings.camera['Blackfly']['quantum_efficiency'])
other_losses['yz'] = np.array(AnalysisSettings.camera['Blackfly']['losses'])
focal_length['yz'] = np.array(AnalysisSettings.camera['Blackfly']['focal_length'])
aperture_diameter['yz'] = np.array(AnalysisSettings.camera['Blackfly']['aperture_diameter'])
solid_angle_fraction['yz'] = np.pi*(aperture_diameter['yz']/2)**2/(4*np.pi*focal_length['yz']**2)
total_efficiency['yz'] = solid_angle_fraction['yz']*quantum_efficiency['yz']*(1-other_losses['yz'])
transpose_image['yz'] = np.array(AnalysisSettings.camera['Blackfly']['transpose'])
rotate_image['yz'] = np.array(AnalysisSettings.camera['Blackfly']['rotate'])

mass = AnalysisSettings.Sr['mass']
sigma0 = AnalysisSettings.Sr['sigma0']
decay_time = AnalysisSettings.Sr['tau']


ROI = {}
if 'ROI' in instance_variables.keys():
    if run_data['ROI'] in AnalysisSettings.ROI_GH.keys():
        ROI['xz'] = AnalysisSettings.ROI_GH[run_data['ROI']]
    else:
        matches = regexp.findall('\[(\d+),(\d+),(\d+),(\d+)\]',run_data['ROI'])
        
        if len(matches)==1 and len(matches[0])==4:
            ROI_0 = np.array([int(match) for match in matches[0]])
            if any(ROI_0 < 0) or any(ROI_0[0:1] >= sensor_size['xz'][0]) or any(ROI_0[2:3] >= sensor_size['xz'][1]):
                print('Grasshopper ROI out of range. Turning off')
                ROI['xz'] = []
            else:
                ROI['xz'] = ROI_0
        else:
            ROI['xz'] = []

    if run_data['ROI'] in AnalysisSettings.ROI_BF.keys():
        ROI['yz'] = AnalysisSettings.ROI_BF[run_data['ROI']]
    else:
        matches = regexp.findall('\[(\d+),(\d+),(\d+),(\d+)\]',run_data['ROI'])
        
        if len(matches)==1 and len(matches[0])==4:
            ROI_0 = np.array([int(match) for match in matches[0]])
            if any(ROI_0 < 0) or any(ROI_0[0:1] >= sensor_size['yz'][0]) or any(ROI_0[2:3] >= sensor_size['yz'][1]):
                print('Blackfly ROI out of range. Turning off')
                ROI['yz'] = []
            else:
                ROI['yz'] = ROI_0
        else:
            ROI['yz'] = []
else:
    ROI['xz'] = []
    ROI['yz'] = []

gaussian_filter_size = AnalysisSettings.filters['gaussian']['large']
median_filter_size = AnalysisSettings.filters['median']['small']
binning_size = AnalysisSettings.filters['binning']['none']

imaging_types = []
if run_data['Absorption']:
    imaging_types.append('absorption')
else:
    imaging_types.append('fluorescence')

print('Detected Imaging Types:')
for name in imaging_types:
    print('    ' + name)

densityImages = dict()
atomNumbers = dict()

print(instance_variables['ImagingCamera'])
cameras = instance_variables['ImagingCamera'].lower().split(',')

if 'absorption' in imaging_types:
    atomImages = {}
    refImages = {}
    densityImages = {}
    atomNumbers = {}
    refNorms = {}
    atomNorms = {}
    camera = 1

    for camera in cameras:
        atomImages[camera] = run.get_image(camera,'absorption','atoms').astype('float') - run.get_image(camera,'absorption','background').astype('float')
        refImages[camera] = run.get_image(camera,'absorption','reference').astype('float') - run.get_image(camera,'absorption','background').astype('float')
        refNorms[camera] = refImages[camera].copy()
        atomNorms[camera] = atomImages[camera].copy()

        if transpose_image[camera]:
            atomImages[camera] = np.transpose(atomImages[camera])
            refImages[camera] = np.transpose(refImages[camera])
            refNorms[camera] = np.transpose(refNorms[camera])
            atomNorms[camera] = np.transpose(atomNorms[camera])
        if rotate_image[camera]>0:
            atomImages[camera] = np.rot90(atomImages[camera],rotate_image[camera])
            refImages[camera] = np.rot90(refImages[camera],rotate_image[camera])
            refNorms[camera] = np.rot90(refNorms[camera],rotate_image[camera])
            atomNorms[camera] = np.rot90(atomNorms[camera],rotate_image[camera])

        if len(ROI[camera])>0:
            pprint(ROI[camera])
            refNorms[camera][ROI[camera][0]:ROI[camera][1],ROI[camera][2]:ROI[camera][3]] = 0
            atomNorms[camera][ROI[camera][0]:ROI[camera][1],ROI[camera][2]:ROI[camera][3]] = 0
            atomImages[camera] = atomImages[camera][ROI[camera][0]:ROI[camera][1],ROI[camera][2]:ROI[camera][3]]
            refImages[camera] = refImages[camera][ROI[camera][0]:ROI[camera][1],ROI[camera][2]:ROI[camera][3]]
            if 'NormalizeProbe' in instance_variables.keys() and run_data['NormalizeProbe']:
                print('    Normalizing probe...')
                refImages[camera] = refImages[camera]*np.sum(atomNorms[camera])/np.sum(refNorms[camera])

        atomImages[camera] = np.clip(medfilt2d(atomImages[camera],median_filter_size),1.0,np.inf)
        refImages[camera] = np.clip(medfilt2d(refImages[camera],median_filter_size),1.0,np.inf)

        densityImages[camera] = gaussian_filter(np.log(refImages[camera]/atomImages[camera]),gaussian_filter_size)

        atomNumbers[camera] = np.sum(densityImages[camera])*(pixel_size[camera]**2)/sigma0

        print('    Absorption image processed for ' + camera + ' direction')

elif 'fluorescence' in imaging_types:
    atomImages = {}
    densityImages = {}
    atomNumbers = {}
    for camera in cameras:
        atomImages[camera] = run.get_image(camera,'fluorescence','atoms').astype('float') - run.get_image(camera,'fluorescence','background').astype('float')
        atomImages[camera] = medfilt2d(atomImages[camera],median_filter_size)
        if len(ROI[camera])>0:
            atomImages[camera] = atomImages[camera][ROI[camera][2]:ROI[camera][3],ROI[camera][0]:ROI[camera][1]]
        densityImages[camera] = gaussian_filter(atomImages[camera],gaussian_filter_size)
        atomNumbers[camera] = np.sum(densityImages[camera])*decay_time/(total_efficiency[camera]*run_data['PulseDuration'])
        print('    Fluorescence image processed for ' + camera + ' direction')


plt.rcParams['text.usetex'] = True
plt.rc('font', family='serif')
figs = dict()
x_0 = dict()
dx_0 = dict()
w = dict()
dw = dict()

for camera, imageData in densityImages.items():
    #if transpose_image[camera]:
    #    imageData = np.transpose(imageData)
    #if rotate_image[camera]>0:
    #    imageData = np.rot90(imageData,rotate_image[camera])
    plot_size = np.shape(imageData)

    x_plot = np.arange(plot_size[1])*pixel_size[camera]*10**6
    y_plot = np.arange(plot_size[0])*pixel_size[camera]*10**6
    x_plot -= np.mean(x_plot)
    y_plot -= np.mean(y_plot)

    if run_data['FitData']:
        try:
            print('Fitting data in ' + camera + ' image...')
            xData = x_plot
            yData = np.sum(imageData,0)

            p_x, dp_x = basic_gaussian_fit(x_plot,np.sum(imageData,0))
            p_y, dp_y = basic_gaussian_fit(np.flip(y_plot),np.sum(imageData,1))

            x_0[camera] = (p_x[1],p_y[1])
            dx_0[camera] = (dp_x[1],dp_y[1])
            w[camera] = [p_x[2],p_y[2]]
            dw[camera] = [dp_x[2],dp_y[2]]
        except Exception:
            print('Error fitting data in ' + camera + ' image...')
            x_0[camera] = (0,0)
            dx_0[camera] = (0,0)
            w[camera] = [0,0]
            dw[camera] = [0,0]

    print('Plotting ' + camera + ' image...')
    figs[camera] = plt.figure(figsize=(4, 3), dpi=200)
    axImage = figs[camera].add_subplot(1,1,1)

    c_min = np.min(imageData)
    c_max = np.max(imageData)
    
    image = axImage.imshow(imageData,extent=[np.min(x_plot),np.max(x_plot),np.min(y_plot),np.max(y_plot)],vmin=c_min,vmax=c_max)
    
    #axImage.invert_yaxis()
    cb = figs[camera].colorbar(image, ax=axImage)
    cb.set_label('Optical depth',fontsize=14)

    axImage.set_xlabel("X-position ($\mu$m)",fontsize=14)
    axImage.set_ylabel("Z-position ($\mu$m)",fontsize=14)
    if run_data['FitData']:
        axImage.add_patch(Ellipse(xy=x_0[camera], width=4*w[camera][0], height=4*w[camera][1], edgecolor='r', fc='None', lw=1))
        titleString = ' = {:1.2f} million'.format(atomNumbers[camera]/10**6) + \
            '\n$x_0$ = {:0.0f} $\mu$m, $\sigma_x$ = {:0.0f} $\mu$m'.format(x_0[camera][0],w[camera][0]) + \
            '\n$z_0$ = {:0.0f} $\mu$m, $\sigma_z$ = {:0.0f} $\mu$m'.format(x_0[camera][1],w[camera][1])
    else:
        titleString = (' = {:.2E}').format(atomNumbers[camera])
    axImage.title.set_text('N_' + camera + titleString)
    plt.tight_layout()
    print('    Done plotting ' + camera + ' image.')

print('Saving data...')
for camera, N in atomNumbers.items():
    run.save_result(camera + "/atomNumber", N)
    if run_data['FitData']:
        run.save_result(camera + '/x_position', x_0[camera][0]/(1*10**6))
        run.save_result(camera + '/y_position', x_0[camera][1]/(1*10**6))
        run.save_result(camera + '/x_width', w[camera][0]/(1*10**6))
        run.save_result(camera + '/y_width', w[camera][1]/(1*10**6))
for camera, imageData in densityImages.items():
    if run_data['SaveImage']:
        datapath = path.split('\\')
        #m = path.split('\\')
        m = datapath[-1].split('_')
        rep_number = m[-1][0:-3]
        savepath = '\\'.join(datapath[0:-1]) + '\\' + rep_number + '_density.png'
        plt.savefig(savepath)
        saveAnalysisImage(path,'single_shot_analysis',camera,imageData)

print('    Data saved.')
print('Done') 