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

camera = AnalysisSettings.Camera
sigma0 = SrConstants.sigma0
mass = SrConstants.mass
pixelSize = SrConstants.pixelSizeDict["horizontal"]

ROI = AnalysisSettings.SGROI
medFiltN = AnalysisSettings.SGMedFilterWidth
gaussFiltN = AnalysisSettings.SGGaussFilterWidth

print('Loading variables...')
try:
    TimeOfFlight = ser['TimeOfFlight']
except:
    print("TimeOfFlight does not exist for this run")
try:
    BlueMOTHoldTime = ser['BlueMOTHoldTime']
except:
    print("BlueMOTHoldTime does not exist for this run")
try:
    PulseDuration = ser['PulseDuration']
except:
    print("PulseDuration does not exist for this run")
try:
    BlueMOTField = ser['BlueMOTField']
except:
    print("BlueMOTField does not exist for this run")
try:
    BlueMOTLoadTime = ser['BlueMOTLoadTime']
except:
    print("BlueMOTLoadTime does not exist for this run")
try:
    ProbeDetuningVoltage = ser['ProbeDetuningVoltage']
except:
    print("ProbeDetuningVoltage does not exist for this run")
try:
    BlueMOTBeatnote = ser['BlueMOTBeatnote']
except:
    print("BlueMOTBeatnote does not exist for this run")
try:
    ProbeVCOVoltage = ser['ProbeVCOVoltage']
except:
    print("ProbeVCOVoltage does not exist for this run")

print('Variables loaded')

print('Loading images...')
if ser['GrasshopperImagingOn'] and ('horizontal', 'absorption', 'atoms','CLASS') in ser.index:
    type = 'absorption'
elif ser['GrasshopperImagingOn'] and ('horizontal', 'fluorescence', 'atoms','CLASS') in ser.index:
    type = 'fluorescence'
    
#print(type)

if type=='absorption':
    #print('absorption')
    atomImage = run.get_image(camera,'absorption','atoms').astype('float') - run.get_image(camera,'absorption','background').astype('float')
    refImage = run.get_image(camera,'absorption','reference').astype('float') - run.get_image(camera,'absorption','background').astype('float')
    refNorm = refImage.copy()
    atomNorm = atomImage.copy()
    refNorm[ROI[2]:ROI[3],ROI[0]:ROI[1]] = 0
    atomNorm[ROI[2]:ROI[3],ROI[0]:ROI[1]] = 0
    atomImage = atomImage[ROI[2]:ROI[3],ROI[0]:ROI[1]]
    refImage = refImage[ROI[2]:ROI[3],ROI[0]:ROI[1]]*np.sum(atomNorm)/np.sum(refNorm)
    atomImage = np.clip(atomImage,1e-10,np.Inf)
    refImage = np.clip(refImage,1e-10,np.Inf)
    densityImage = medfilt2d(np.log(refImage/atomImage),medFiltN)
elif type=='fluorescence':
    densityImage = run.get_image(camera,'fluorescence','atoms').astype('float') - run.get_image(camera,'fluorescence','background').astype('float')
    #densityImage = densityImage[ROI[2]:ROI[3],ROI[0]:ROI[1]]

if type=='absorption':
    densityImage = gaussian_filter(densityImage, gaussFiltN)
elif type=='fluorescence':
    densityImage = gaussian_filter(densityImage, gaussFiltN)*PulseDuration/.116 # Hand-picked factor to approximate actual atom number

atomNumber = np.sum(densityImage)*(pixelSize**2)/sigma0
print('Images loaded and density calculated')

print('Plotting...')
fig = plt.figure()

ax_image = fig.add_subplot(111)
#ax_empty = fig.add_subplot(222)
#ax_x = fig.add_subplot(223)
#ax_z = fig.add_subplot(224)

c_min = 0
c_max = np.max(densityImage)
x = np.array(range(densityImage.shape[1]))*pixelSize*1e3
x -= np.median(x)
y = np.array(range(densityImage.shape[1]))*pixelSize*1e3
y -= np.median(y)
imagePlot = ax_image.imshow(densityImage, vmin=c_min, vmax=c_max,extent=[np.min(x),np.max(x),np.min(y),np.max(y)])
fig.colorbar(imagePlot, ax=ax_image)
#if type=='absorption':
ax_image.title.set_text("N = " + '{:.2e}'.format(atomNumber))
ax_image.set_xlabel('X (mm)')
ax_image.set_ylabel('Z (mm)')

#ax_x.plot(x, imageX)
#ax_x.grid(True)
#if type=='absorption':
#    #print(len(pOptX))
#    ax_x.plot(x, gauss_zero_ref(x, *pOptX))
#elif type=='fluorescence':
#    ax_x.plot(x, gauss(x, *pOptX))
#ax_x.set_xlim(0,np.max(x))
##ax_x.title.set_text("gaussian in x")
#
#ax_z.plot(z, imageZ)
#if type=='absorption':
#    ax_z.plot(z, gauss_zero_ref(z, *pOptZ))
#elif type=='fluorescence':
#    ax_z.plot(z, gauss(z, *pOptZ))
#ax_z.grid(True)
#ax_z.set_xlim(0,np.max(z))

datapath = path.split('\\')

print('Saving plot...')
savepath = '\\'.join(datapath[0:-1]) + '\\MOT_image.png'
plt.savefig(savepath)

print('Plot saved')
#ax_z.title.set_text("gaussian in z")

#fig.tight_layout()

#run.save_result_array("densityImage", densityImage)
#if type=='absorption':
#    run.save_result_array("atomImage", atomImage)
#    run.save_result_array("refImage", refImage)

#run.save_result("x", x)
#run.save_result("imageX", imageX)
#run.save_result("z", z)
#run.save_result("imageZ", imageZ)

print('Saving data...')
run.save_result("atomNumber", atomNumber)
if "pOptX" in locals():
    run.save_result("sigma_x", pOptX[2]*pixelSize)
if "pOptZ" in locals():
    run.save_result("sigma_z", pOptZ[2]*pixelSize)
if "BlueMOTLoadTime" in locals():
    run.save_result("BlueMOTLoadTime", BlueMOTLoadTime)
if "ProbeDetuningVoltage" in locals():
    run.save_result("ProbeDetuningVoltage", ProbeDetuningVoltage)
if "TimeOfFlight" in locals():
    run.save_result("TimeOfFlight", TimeOfFlight)
if "BlueMOTBeatnote" in locals():
    run.save_result("BlueMOTBeatnote", BlueMOTBeatnote)
if "ProbeVCOVoltage" in locals():
    run.save_result("ProbeVCOVoltage", ProbeVCOVoltage)
if "BlueMOTField" in locals():
    run.save_result("BlueMOTField", BlueMOTField)
if "BlueMOTHoldTime" in locals():
    run.save_result("BlueMOTHoldTime", BlueMOTHoldTime)
    
print('Data saved')
print('Complete')