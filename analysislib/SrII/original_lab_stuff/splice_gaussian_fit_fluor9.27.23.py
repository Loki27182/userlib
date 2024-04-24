from lyse import *
import matplotlib.pyplot as plt
import numpy as np
import h5py
import scipy.constants as constants
from matplotlib.widgets import Cursor, Slider
from scipy.ndimage import gaussian_filter

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
print(pixelSize)


# Get Data

ROI = AnalysisSettings.SGFROI
"""
with h5py.File(path) as f:
    # Load in the MOT video:
#     im_loading_raw = []
#     for ii in range(int(ser['BlueMOTLoadTime']/ser['TimeBetweenExp'])-2):
#         im_loading_raw.append(run.get_image('grating', 'fluorescence', 'atoms'+str(ii)))
#     im_loading_raw = np.array(im_loading_raw)
# fluor = im_loading_raw[-1]
    maxcounts = 0
    for ii in range(int(ser['BlueMOTLoadTime']/ser['TimeBetweenExp'])-2):
        currentCounts = np.sum(run.get_image(camera,'fluorescence', 'atoms'+str(ii))[ROI[2]:ROI[3],ROI[0]:ROI[1]])
        if currentCounts > maxcounts:
            print(currentCounts)
            maxcounts = currentCounts
            fluor = run.get_image(camera,'fluorescence', 'atoms'+str(ii))
"""
TimeOfFlight = ser['TimeOfFlight']

#if ser['FluorImaging']:
if ser['GrasshopperImagingOn']:
    #fluor = run.get_image('grating','fluorescence','atoms').astype('float') - run.get_image('grating','fluorescence','background').astype('float')
    fluor = run.get_image(camera,'fluorescence','atoms').astype('float') - run.get_image(camera,'fluorescence','background').astype('float')
# PrepareImage

ROI = AnalysisSettings.SGFROI
#fluor_alt = gaussian_filter(fluor, 1.5)
fluor_alt = fluor
# Fit OD

x, imageX, pOptX, pCovX, z, imageZ, pOptZ, pCovZ = splice_gaussian_fit_sub(fluor_alt, True)
pStdDevX = np.sqrt(np.diag(pCovX))
pStdDevZ = np.sqrt(np.diag(pCovX))

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




#ax_image.plot(pOptX[1],pOptZ[1],'bo')

# Save Values

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

run.save_result_array("fluorImage", fluor_alt)
"""
tempX = mass * (widthX / TimeOfFlight) ** 2 / (2 * constants.value("Boltzmann constant"))
tempZ = mass * (widthZ / TimeOfFlight) ** 2 / (2 * constants.value("Boltzmann constant"))
tempXDev = mass * 2 * (widthX / (TimeOfFlight** 2)) * widthXDev / (2 * constants.value("Boltzmann constant"))
tempZDev = mass * 2 * (widthZ / (TimeOfFlight** 2)) * widthZDev / (2 * constants.value("Boltzmann constant"))

atomNumber = (pOptX[0] + pOptZ[0]) * np.pi * widthX * widthZ / sigma0
atomNumberDev =   np.sqrt((pStdDevX[0]* np.pi * widthX * widthZ / sigma0)**2
                + (pStdDevZ[0] * np.pi * widthX * widthZ / sigma0)**2
                + ((pOptX[0] + pOptZ[0]) * np.pi * widthXDev * widthZ / sigma0)**2
                + ((pOptX[0] + pOptZ[0]) * np.pi * widthX * widthZDev / sigma0)**2)

avgWidth = (widthX + widthZ)/2
avgWidthDev = np.sqrt((widthXDev/2)**2 + (widthZDev/2)**2)
avgPeakOD = (pOptX[0] + pOptZ[0])/2
avgPeakODDev = np.sqrt((pStdDevX[0]/2)**2 + (pStdDevZ[0]/2)**2)
avgTemp = (tempX + tempZ)/2
avgTempDev = np.sqrt((tempXDev/2)**2 + (tempZDev/2)**2)


# Save Values

run.save_result("peakODX", pOptX[0])
run.save_result("widthX", widthX)
run.save_result("tempX", tempX)
run.save_result("centerX", centerX)
run.save_result("centerXPix", centerXPix)
run.save_result("peakODZ", pOptZ[0])
run.save_result("widthZ", widthZ)
run.save_result("tempZ", tempZ)
run.save_result("centerZ", centerZ)
run.save_result("centerZPix", centerZPix)
run.save_result("atomNumber", atomNumber)
run.save_result("avgWidth", avgWidth)
run.save_result("avgPeakOD", avgPeakOD)
run.save_result("avgTemp", avgTemp)

run.save_result("peakODXDev", pStdDevX[0])
run.save_result("widthXDev", widthXDev)
run.save_result("tempXDev", tempXDev)
run.save_result("centerXDev", centerXDev)
run.save_result("peakODZDev", pStdDevZ[0])
run.save_result("widthZDev", widthZDev)
run.save_result("tempZDev", tempZDev)
run.save_result("centerZDev", centerZDev)
run.save_result("atomNumberDev", atomNumberDev)
run.save_result("avgWidthDev", avgWidthDev)
run.save_result("avgPeakODDev", avgPeakODDev)
run.save_result("avgTempDev", avgTempDev)

run.save_result_array("fluorImage", fluor_alt)

print("avgTemp"+ str(avgTemp))
print("atomNumber" + str(atomNumber))
print("widthz " + str(widthZ))
print("CenterX" + str(centerX))
print("CenterZ" + str(centerZ))
# Set Center event

cursor = Cursor(ax_image, useblit=True, color='white', linewidth=1)
cursor.set_active(False)


def set_center(event):
    if event.key in ['C', 'c'] and not cursor.active:
        cursor.set_active(True)
    elif event.key in ['C', 'c'] and cursor.active:
        cursor.set_active(False)
        center = (int(event.xdata), int(event.ydata))
        print(center)
        with h5py.File('C:\\Users\\jqisr\\labscript-suite\\userlib\\analysislib\SrII\\current_roi.h5', 'w') as f:
            if 'center' not in f:
                f.attrs.create('center', center)
            else:
                f.attrs['center'] = center


if not getattr(routine_storage, 'keypress_connected', False):
    plt.connect('key_press_event', set_center)
    routine_storage.keypress_connected = True
"""
