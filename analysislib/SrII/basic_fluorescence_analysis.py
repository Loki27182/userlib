from lyse import *
import matplotlib.pyplot as plt
import numpy as np
import h5py
import scipy.constants as constants
from matplotlib.widgets import Cursor, Slider
from scipy.ndimage import gaussian_filter

from Subroutines.gaussian_fit_sub import gaussian_fit_sub
import SrConstants
import AnalysisSettings
from Subroutines.FitFunctions import gauss

ser = data(path)
run = Run(path)

camera = AnalysisSettings.Camera
sigma0 = SrConstants.sigma0
mass = SrConstants.mass
pixelSize = SrConstants.pixelSizeDict[camera]
#print(pixelSize)

# Get Data

ROI = AnalysisSettings.SGFROI

TimeOfFlight = ser['TimeOfFlight']
BlueMOTBeatnote = ser['BlueMOTBeatnote']
BlueMOTBeatnoteScan = ser['BlueMOTBeatnoteScan']

#if ser['FluorImaging']:
if ser['GrasshopperImagingOn']:
    #fluor = run.get_image('grating','fluorescence','atoms').astype('float') - run.get_image('grating','fluorescence','background').astype('float')
    fluor = run.get_image(camera,'fluorescence','atoms').astype('float') - run.get_image(camera,'fluorescence','background').astype('float')
# PrepareImage

ROI = AnalysisSettings.SGFROI
#fluor_alt = gaussian_filter(fluor, 1.5)
fluor_alt = fluor
# Fit OD
x, imageX, pOptX, pCovX, z, imageZ, pOptZ, pCovZ = integrated_gaussian_fit_sub(fluor_alt, True)
pStdDevX = np.sqrt(np.diag(pCovX))
pStdDevZ = np.sqrt(np.diag(pCovX))
atomNumber = np.sum(fluor_alt)

# Calculate Things of Interest
#print(pOptX)
widthX = pOptX[2] * pixelSize
widthZ = pOptZ[2] * pixelSize
widthXDev = pStdDevX[2] * pixelSize
widthZDev = pStdDevZ[2] * pixelSize

centerX = pOptX[1] * pixelSize
centerZ = pOptZ[1] * pixelSize
centerXPix = pOptX[1]
centerZPix = pOptZ[1]
centerXDev = pStdDevX[1] * pixelSize
centerZDev = pStdDevZ[1] * pixelSize

# Make Figure

fig = plt.figure()
#fig.suptitle("avgTemp= "+ str(avgTemp), fontsize=24)
#fig.suptitle((pOptX[0] + pOptZ[0])/2, fontsize=70)
ax_image = fig.add_subplot(221)
ax_x = fig.add_subplot(223)
ax_z = fig.add_subplot(222)
# c_min = min(pOptX[3], pOptX[0])
# c_max = max(pOptX[3] + pOptX[0], 0.01)
avg = np.average(fluor_alt)
std = np.std(fluor_alt)
c_min = avg - 1*std
c_max = avg + 1.5*std
imagePlot = ax_image.imshow(fluor_alt, vmin=c_min, vmax=c_max)

ax_cmin = plt.axes([0.55, 0.27, 0.4, 0.03])
ax_cmax = plt.axes([0.55, 0.23, 0.4, 0.03])
s_cmin = Slider(ax_cmin,"min",-1000,3000,valinit = c_min)
s_cmax = Slider(ax_cmax,"max",-1000,3000,valinit = c_max)

def update(val, s=None):
    _cmin = s_cmin.val
    _cmax = s_cmax.val
    imagePlot.set_clim([_cmin,_cmax])

s_cmin.on_changed(update)
s_cmax.on_changed(update)

ax_x.plot(x, imageX)
ax_x.grid(True)
ax_x.plot(x, gauss(x, *pOptX))
ax_x.set_xlim(0,2000)
ax_x.title.set_text("gaussian in x")
ax_z.plot(z, imageZ)
ax_z.plot(z, gauss(z, *pOptZ))
ax_z.grid(True)
ax_z.set_xlim(0,1500)
ax_z.title.set_text("gaussian in z")

run.save_result("fitParamX0", pOptX[0])
run.save_result("fitParamX1", pOptX[1])
run.save_result("fitParamX2", pOptX[2])
run.save_result("fitParamX3", pOptX[3])
run.save_result("fitParamZ0", pOptZ[0])
run.save_result("fitParamZ1", pOptZ[1])
run.save_result("fitParamZ2", pOptZ[2])
run.save_result("fitParamZ3", pOptZ[3])

run.save_result("widthX", widthX)
run.save_result("x", x)
run.save_result("imageX", imageX)
run.save_result("z", z)
run.save_result("imageZ", imageZ)
run.save_result("centerX", centerX)
run.save_result("centerXPix", centerXPix)
run.save_result("peakODZ", pOptZ[0])
run.save_result("widthZ", widthZ)
run.save_result("centerZ", centerZ)
run.save_result("centerZPix", centerZPix)

run.save_result("peakODXDev", pStdDevX[0])
run.save_result("widthXDev", widthXDev)
run.save_result("centerXDev", centerXDev)
run.save_result("peakODZDev", pStdDevZ[0])
run.save_result("widthZDev", widthZDev)
run.save_result("centerZDev", centerZDev)
run.save_result("TimeofFlight", TimeOfFlight)
run.save_result("BlueMOTBeatnote", BlueMOTBeatnote)
run.save_result("BlueMOTBeatnoteScan", BlueMOTBeatnoteScan)
run.save_result("atomNumber", atomNumber)

run.save_result_array("fluorImage", fluor_alt)
