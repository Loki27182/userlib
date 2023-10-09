from lyse import *
import matplotlib.pyplot as plt
import numpy as np
import h5py
import scipy.constants as constants
import AnalysisSettings
from matplotlib.widgets import Cursor, Slider


df = data()
shot_paths = df['filepath']
run = Run(shot_paths[-1])

# Get Data
ROI = AnalysisSettings.SGFROI
optical_depth_current = run.get_result_array('VerySimpleImaging', 'optical_depth')[ROI[2]:ROI[3],ROI[0]:ROI[1]]
run = Run(shot_paths[-2])
optical_depth_previous = run.get_result_array('VerySimpleImaging', 'optical_depth')[ROI[2]:ROI[3],ROI[0]:ROI[1]]

# Process Images
current_average = np.average(optical_depth_current)
previous_average = np.average(optical_depth_previous)
current_std = np.std(optical_depth_current)
previous_std = np.std(optical_depth_previous)
print(current_average)
print(previous_average)
multiplier = 1#current_average/previous_average
print(multiplier)

subtracted_image = optical_depth_current - multiplier * optical_depth_previous
sub_average = current_average - multiplier * previous_average
sub_std = np.std(subtracted_image)
# Make Figure

fig = plt.figure()
ax_image_current = fig.add_subplot(221)
ax_image_current.imshow(optical_depth_current,vmin=current_average - current_std, vmax=current_average + current_std)
ax_image_previous = fig.add_subplot(222)
ax_image_previous.imshow(optical_depth_previous,vmin=previous_average-previous_std, vmax=previous_average + previous_std)
ax_image = fig.add_subplot(223)
imagePlot = ax_image.imshow(subtracted_image, vmin=sub_average-sub_std, vmax=sub_average+sub_std)

ax_mult = plt.axes([0.55, 0.27, 0.4, 0.03])
#ax_cmax = plt.axes([0.55, 0.23, 0.4, 0.03])
s_mult = Slider(ax_mult,"mult",0.1,2,valinit = multiplier)
#s_cmax = Slider(ax_cmax,"max",-0.2,0.5,valinit = c_max)

def update(val, s=None):
    multiplier = s_mult.val
    subtracted_image = optical_depth_current - multiplier * optical_depth_previous
    sub_average = current_average - multiplier * previous_average
    imagePlot = ax_image.imshow(subtracted_image, vmin=sub_average-sub_std, vmax=sub_average+sub_std)

s_mult.on_changed(update)
