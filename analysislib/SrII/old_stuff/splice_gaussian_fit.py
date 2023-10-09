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

optical_depth = run.get_result_array('VerySimpleImaging', 'optical_depth')
TimeOfFlight = ser['TimeOfFlight']

# PrepareImage

ROI = AnalysisSettings.SGFROI
optical_depth_alt = gaussian_filter(optical_depth[ROI[2]:ROI[3],ROI[0]:ROI[1]], AnalysisSettings.SGFFilterWidth)
#optical_depth_alt = gaussian_filter(optical_depth, AnalysisSettings.SGFFilterWidth)
#optical_depth_alt = run.get_image(camera, 'absorption', 'atoms').astype('float')
run.get_image(camera, 'absorption', 'atoms').astype('float')

avg = np.average(optical_depth_alt)
std = np.std(optical_depth_alt)
# Fit OD

x, imageX, pOptX, pCovX, z, imageZ, pOptZ, pCovZ = splice_gaussian_fit_sub(optical_depth_alt, False)
pStdDevX = np.sqrt(np.diag(pCovX))
pStdDevZ = np.sqrt(np.diag(pCovX))

# Make Figure

fig = plt.figure()
fig.suptitle(pOptX[0], fontsize=70)
ax_image = fig.add_subplot(221)
ax_x = fig.add_subplot(223)
ax_z = fig.add_subplot(222)
# c_min = min(pOptX[3], pOptX[0])
# c_max = max(pOptX[3] + pOptX[0], 0.01)
c_min = avg - (1/2)*std
c_max = avg + (2.5)*std
imagePlot = ax_image.imshow(optical_depth_alt, vmin=c_min, vmax=c_max)
showOverlap = True;
if showOverlap:
    # ax_image.plot([100-ROI[0],1200-ROI[0]],[985-ROI[2],960-ROI[2]],color = "white")
    # ax_image.plot([590-ROI[0],540-ROI[0]],[1000-ROI[2],200-ROI[2]],color = "white")
    # ax_image.plot([730-ROI[0],730-ROI[0]],[1000-ROI[2],200-ROI[2]],color = "white")
    ax_image.plot([659-ROI[0]-11*0.001/pixelSize+68.2*4,(659-11*0.001/pixelSize)+68.2*12-ROI[0]],[972.5-ROI[2]-73.14*4,972.5-ROI[2]-73.14*12],color = "red")
    ax_image.plot([659-ROI[0]-1.5*0.001/pixelSize,(659-1.5*0.001/pixelSize)-ROI[0]+68.2*9],[972.5-ROI[2],972.5-73.14*9-ROI[2]],color = "red")
    ax_image.plot([659-ROI[0]+11*0.001/pixelSize-68.2*4,(659+11*0.001/pixelSize)-ROI[0]-68.2*12],[972.5-73.14*4-ROI[2],972.5-73.14*12-ROI[2]],color = "red")
    ax_image.plot([659-ROI[0]+1.5*0.001/pixelSize,(659+1.5*0.001/pixelSize)-ROI[0]-68.2*9],[972.5-ROI[2],972.5-73.14*9-ROI[2]],color = "red")
    #ax_image.plot([(588+730)/2,(588+730)/2],[(974+971)/2,0],color = 'red')
ax_cmin = plt.axes([0.55, 0.27, 0.4, 0.03])
ax_cmax = plt.axes([0.55, 0.23, 0.4, 0.03])
s_cmin = Slider(ax_cmin,"min",-0.2,0.5,valinit = c_min)
s_cmax = Slider(ax_cmax,"max",-0.2,0.5,valinit = c_max)

def update(val, s=None):
    _cmin = s_cmin.val
    _cmax = s_cmax.val
    imagePlot.set_clim([_cmin,_cmax])

s_cmin.on_changed(update)
s_cmax.on_changed(update)

ax_x.plot(x, imageX)
ax_x.plot(x, gauss(x, *pOptX))
ax_z.plot(z, imageZ)
ax_z.plot(z, gauss(z, *pOptZ))
#ax_image.plot(pOptX[1],pOptZ[1],'bo')

# Calculate Things of Interest

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
        with h5py.File('C:\\Users\\Lab\\labscript-suite\\userlib\\analysislib\SrII\\current_roi.h5', 'w') as f:
            if 'center' not in f:
                f.attrs.create('center', center)
            else:
                f.attrs['center'] = center


if not getattr(routine_storage, 'keypress_connected', False):
    plt.connect('key_press_event', set_center)
    routine_storage.keypress_connected = True
