from lyse import *
import matplotlib.pyplot as plt
import numpy as np
import h5py
import scipy.constants as constants
from matplotlib.widgets import Cursor, Slider
from scipy.ndimage import gaussian_filter
from scipy.signal import medfilt2d
from pprint import pprint

#from Subroutines.gaussian_fit_sub import gaussian_fit_sub
#import SrConstants
import AnalysisSettings
#from Subroutines.FitFunctions import gauss, gauss_zero_ref

data_series = data()
run_data = data(path)
run = Run(path)

variables = {name: data_series[name].values for name, value in run.get_globals().items()}
iterated_variables = {name: value for name, value in variables.items() if len(value)>1 and len(value)==len(np.unique(value))}
static_variables = {name: value[0] for name, value in variables.items() if not (len(value)>1 and len(value)==len(np.unique(value)))}

pixel_size = AnalysisSettings.camera['GH']['pixel_size']
mass = AnalysisSettings.Sr['mass']
sigma0 = AnalysisSettings.Sr['sigma0']

if 'ROI' in variables.keys():
    if run_data['ROI'] in AnalysisSettings.ROI.keys():
        ROI = AnalysisSettings.ROI[run_data['ROI']]
    else:
        ROI = []
else:
    ROI = []

gaussian_filter_size = AnalysisSettings.filters['gaussian']['small']
median_filter_size = AnalysisSettings.filters['median']['small']

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

figs = dict()
for imageType, imageData in densityImages.items():
    print('Plotting ' + imageType + ' image...')
    figs[imageType] = plt.figure()
    axImage = figs[imageType].add_subplot(111)

    c_min = np.min(imageData)
    c_max = np.max(imageData)

    image = axImage.imshow(imageData,vmin=c_min,vmax=c_max)

    figs[imageType].colorbar(image, ax=axImage)

    axImage.title.set_text('N = ' + '{:.2e}'.format(atomNumbers[imageType]))
    
    print('    Done plotting ' + imageType + ' image.')

print('Saving data...')
for imageType, N in atomNumbers.items():
    run.save_result("atomNumber/"+imageType, N)
print('    Data saved.')
print('Done')