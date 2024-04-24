from lyse import *
import matplotlib.pyplot as plt
import numpy as np
import h5py
import scipy.constants as constants
from matplotlib.widgets import Cursor, Slider
from scipy.ndimage import gaussian_filter
from scipy.signal import medfilt2d

from Subroutines.splice_gaussian_fit_sub import splice_gaussian_fit_sub
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
    atomImage = run.get_image(camera,'absorption','atoms').astype('float') - run.get_image(camera,'absorption','background').astype('float')
    refImage = run.get_image(camera,'absorption','reference').astype('float') - run.get_image(camera,'absorption','background').astype('float')
    atomImage = np.clip(atomImage,1e-10,np.Inf)
    refImage = np.clip(refImage,1e-10,np.Inf)
    ODImage = medfilt2d(np.log(refImage/atomImage),5)
    #ODImage = np.log(refImage/atomImage)
# PrepareImage

#ROI = AnalysisSettings.SGFROI
##fluor_alt = gaussian_filter(fluor, 1.5)
#fluor_alt = fluor
## Fit OD
#x, imageX, pOptX, pCovX, z, imageZ, pOptZ, pCovZ = splice_gaussian_fit_sub(fluor_alt, True)
#pStdDevX = np.sqrt(np.diag(pCovX))
#pStdDevZ = np.sqrt(np.diag(pCovX))
#atomNumber = np.sum(fluor_alt)
#
## Calculate Things of Interest
##print(pOptX)
#widthX = pOptX[2] * pixelSize
#widthZ = pOptZ[2] * pixelSize
#widthXDev = pStdDevX[2] * pixelSize
#widthZDev = pStdDevZ[2] * pixelSize
#
#centerX = pOptX[1] * pixelSize
#centerZ = pOptZ[1] * pixelSize
#centerXPix = pOptX[1]
#centerZPix = pOptZ[1]
#centerXDev = pStdDevX[1] * pixelSize
#centerZDev = pStdDevZ[1] * pixelSize
#
## Make Figure
#
fig = plt.figure()

ax_image = fig.add_subplot(111)
c_min = 0
c_max = 1
imagePlot = ax_image.imshow(ODImage, vmin=c_min, vmax=c_max)
fig.colorbar(imagePlot, ax=ax_image)


run.save_result_array("atomImage", atomImage)
run.save_result_array("refImage", atomImage)
run.save_result_array("ODImage", ODImage)

#run.save_result("fitParamX0", pOptX[0])
#run.save_result("fitParamX1", pOptX[1])
#run.save_result("fitParamX2", pOptX[2])
#run.save_result("fitParamX3", pOptX[3])
#run.save_result("fitParamZ0", pOptZ[0])
#run.save_result("fitParamZ1", pOptZ[1])
#run.save_result("fitParamZ2", pOptZ[2])
#run.save_result("fitParamZ3", pOptZ[3])

#run.save_result("widthX", widthX)
#run.save_result("x", x)
#run.save_result("imageX", imageX)
#run.save_result("z", z)
#run.save_result("imageZ", imageZ)
#run.save_result("centerX", centerX)
#run.save_result("centerXPix", centerXPix)
#run.save_result("peakODZ", pOptZ[0])
#run.save_result("widthZ", widthZ)
#run.save_result("centerZ", centerZ)
#run.save_result("centerZPix", centerZPix)
#
#run.save_result("peakODXDev", pStdDevX[0])
#run.save_result("widthXDev", widthXDev)
#run.save_result("centerXDev", centerXDev)
#run.save_result("peakODZDev", pStdDevZ[0])
#run.save_result("widthZDev", widthZDev)
#run.save_result("centerZDev", centerZDev)
#run.save_result("TimeofFlight", TimeOfFlight)
#run.save_result("BlueMOTBeatnote", BlueMOTBeatnote)
#run.save_result("BlueMOTBeatnoteScan", BlueMOTBeatnoteScan)
#run.save_result("atomNumber", atomNumber)
#
#run.save_result_array("fluorImage", fluor_alt)
