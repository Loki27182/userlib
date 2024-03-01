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
try:
    BlueMOTPower = ser['BlueMOTPower']
except:
    print("BlueMOTPower does not exist for this run")
try:
    BlueMOTShimX = ser['BlueMOTShimX']
except:
    print("BlueMOTShimX does not exist for this run")
try:
    BlueMOTShimY = ser['BlueMOTShimY']
except:
    print("BlueMOTShimY does not exist for this run")
try:
    BlueMOTShimZ = ser['BlueMOTShimZ']
except:
    print("BlueMOTShimZ does not exist for this run")
try:
    SaveImage = ser['SaveImage']
except:
    print("SaveImage does not exist for this run")
try:
    RedCoolingBeatnote = ser['RedCoolingBeatnote']
except:
    print("RedCoolingBeatnote does not exist for this run")
try:
    DelayBeforeImaging = ser['DelayBeforeImaging']
except:
    print("DelayBeforeImaging does not exist for this run")


print('Variables loaded')

print('Loading images...')
if ser['GrasshopperImagingOn'] and ('horizontal', 'absorption', 'atoms','CLASS') in ser.index:
    imaging_type = 'absorption'
elif ser['GrasshopperImagingOn'] and ('horizontal', 'fluorescence', 'atoms','CLASS') in ser.index:
    imaging_type = 'fluorescence'
elif ser['GrasshopperImagingOn'] and ('horizontal', 'fluorescence_normalized', 'atoms','CLASS') in ser.index:
    imaging_type = 'fluorescence_normalized'
print(imaging_type)
    
#print(imaging_type)

if imaging_type=='absorption':
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
elif imaging_type=='fluorescence':
    densityImage = run.get_image(camera,'fluorescence','atoms').astype('float') - run.get_image(camera,'fluorescence','background').astype('float')
elif imaging_type=='fluorescence_normalized':
    atomImage = run.get_image(camera,'fluorescence_normalized','atoms').astype('float') - run.get_image(camera,'fluorescence_normalized','background').astype('float')
    refImage = run.get_image(camera,'fluorescence_normalized','reference').astype('float') - run.get_image(camera,'fluorescence_normalized','background').astype('float')
    atomNumber = np.sum(atomImage)/np.sum(refImage)
    print(atomImage.dtype)
    print(atomImage.dtype)
    #print(type(refImage[0]))

if imaging_type=='absorption':
    densityImage = gaussian_filter(densityImage, gaussFiltN)
elif imaging_type=='fluorescence':
    densityImage = gaussian_filter(densityImage, gaussFiltN)*PulseDuration/.116 # Hand-picked factor to approximate actual atom number

if imaging_type!='fluorescence_normalized':
    atomNumber = np.sum(densityImage)*(pixelSize**2)/sigma0

    print('Images loaded and density calculated')

    print('Fitting gaussian...')
    if imaging_type=='absorption':
        x, imageX, pOptX, pCovX, z, imageZ, pOptZ, pCovZ = gaussian_fit_sub(densityImage, zero_ref=True)
    elif imaging_type=='fluorescence':
        x, imageX, pOptX, pCovX, z, imageZ, pOptZ, pCovZ = gaussian_fit_sub(densityImage, zero_ref=False)

    print('Fit complete')

    widthX =pOptX[2]*pixelSize
    widthZ =pOptZ[2]*pixelSize
    BeamRadius=((widthX/2)**2 + (widthZ/2)**2)**0.5 * 1000000

    print('Plotting...')

    fig = plt.figure()

    ax_image = fig.add_subplot(221)
    ax_x = fig.add_subplot(223)
    ax_z = fig.add_subplot(224)

    c_min = 0
    c_max = np.max(densityImage)
    imagePlot = ax_image.imshow(densityImage, vmin=c_min, vmax=c_max)
    fig.colorbar(imagePlot, ax=ax_image)
    ax_image.title.set_text('N = ' + '{:.2e}'.format(atomNumber))

    ax_x.plot(x, imageX)
    ax_x.grid(True)
    if imaging_type=='absorption':
        ax_x.plot(x, gauss_zero_ref(x, *pOptX))
    elif imaging_type=='fluorescence':
        ax_x.plot(x, gauss(x, *pOptX))
    ax_x.set_xlim(0,np.max(x))

    ax_z.plot(z, imageZ)
    if imaging_type=='absorption':
        ax_z.plot(z, gauss_zero_ref(z, *pOptZ))
    elif imaging_type=='fluorescence':
        ax_z.plot(z, gauss(z, *pOptZ))
    ax_z.grid(True)
    ax_z.set_xlim(0,np.max(z))

    print('Done Plotting')
else:
    print('Plotting...')

    fig = plt.figure()

    ax_atoms = fig.add_subplot(122)
    ax_ref = fig.add_subplot(121)

    c_min = 0
    c_max = np.max([np.max(atomImage),np.max(refImage)])

    atomsPlot = ax_atoms.imshow(atomImage, vmin=c_min, vmax=c_max)
    fig.colorbar(atomsPlot, ax=ax_atoms)
    ax_atoms.title.set_text('N_atoms = ' + '{:.2e}'.format(np.sum(atomImage)))
    
    refPlot = ax_ref.imshow(refImage, vmin=c_min, vmax=c_max)
    fig.colorbar(refPlot, ax=ax_ref)
    ax_ref.title.set_text('N_ref = ' + '{:.2e}'.format(np.sum(refImage)))

    fig.suptitle('N_atoms/N_ref = ' + '{:1.2g}'.format(atomNumber))

    print('Done Plotting')


if SaveImage:
    print('Plotting figure to save...')

    fig_save = plt.figure()
    ax_image_save = fig_save.add_subplot(111)
    c_min = 0
    c_max = np.max(densityImage)
    imagePlot_save = ax_image_save.imshow(densityImage, vmin=c_min, vmax=c_max)
    fig_save.colorbar(imagePlot_save, ax=ax_image_save)
    if "RedCoolingBeatnote" in locals():
        ax_image_save.title.set_text("Red Beatnote Frequency = " + '{:.3f}'.format(RedCoolingBeatnote))

    print('Done plotting figure to save')


    print('Saving plot...')

    datapath = path.split('\\')
    #for part in datapath:
    #    print(part)
    savepath = '\\'.join(datapath[0:-1]) + '\\' + rep_number + '_density.png'
    plt.savefig(savepath)

    print('Plot saved')


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
if "BlueMOTPower" in locals():
    run.save_result("BlueMOTPower", BlueMOTPower)
if "BlueMOTShimX" in locals():
    run.save_result("BlueMOTShimX", BlueMOTShimX)
if "BlueMOTShimY" in locals():
    run.save_result("BlueMOTShimY", BlueMOTShimY)
if "BlueMOTShimZ" in locals():
    run.save_result("BlueMOTShimZ", BlueMOTShimZ)
if "RedCoolingBeatnote" in locals():
    run.save_result("RedCoolingBeatnote", RedCoolingBeatnote)
if "DelayBeforeImaging" in locals():
    run.save_result("DelayBeforeImaging", DelayBeforeImaging)
    
print('Data saved')

print('Complete')