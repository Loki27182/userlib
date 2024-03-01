from lyse import *
import matplotlib.pyplot as plt
import numpy as np
import h5py
import scipy.constants as constants
from matplotlib.widgets import Cursor, Slider
from scipy.ndimage import gaussian_filter
from scipy.signal import medfilt2d

from Subroutines.gaussian_fit_sub import gaussian_fit_sub
import SrConstants
import AnalysisSettings
from Subroutines.FitFunctions import gauss, gauss_zero_ref

ser = data(path)
run = Run(path)

m = path.split('\\')
m = m[-1].split('_')
rep_number = m[-1][0:-3]

camera = AnalysisSettings.Camera
sigma0 = SrConstants.sigma0
mass = SrConstants.mass
pixelSize = SrConstants.pixelSizeDict["horizontal"]

ROI = AnalysisSettings.SGROI
medFiltN = AnalysisSettings.SGMedFilterWidth
gaussFiltN = AnalysisSettings.SGGaussFilterWidth


densityImage = run.get_image(camera,'fluorescence','atoms').astype('float') - run.get_image(camera,'fluorescence','background').astype('float')
atomNumber = np.sum(densityImage)
densityImage = gaussian_filter(densityImage, gaussFiltN)

print('Plotting...')

fig = plt.figure()

ax_image = fig.add_subplot(111)

c_min = 0
c_max = np.max(densityImage)
imagePlot = ax_image.imshow(densityImage, vmin=c_min, vmax=c_max)
fig.colorbar(imagePlot, ax=ax_image)
ax_image.title.set_text('N = ' + '{:.2e}'.format(atomNumber))

run.save_result("atomNumber", atomNumber)

print('Data saved')

print('Complete')