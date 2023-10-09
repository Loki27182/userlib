from lyse import *
import matplotlib.pyplot as plt
import numpy as np
import AnalysisSettings
from matplotlib.widgets import Cursor, Slider


df = data()
shot_paths = df['filepath']

fig = plt.figure()

run = Run(shot_paths[0])
image = run.get_result_array('splice_gaussian_fit_fluor','fluorImage')


average_density = np.zeros(np.shape(image))

for i in range(len(shot_paths)):
    run = Run(shot_paths[i])
    image = run.get_result_array('splice_gaussian_fit_fluor','fluorImage')
    average_density += image

ROI = AnalysisSettings.SGFROI
average_density_alt = average_density
avg = np.average(average_density_alt/len(shot_paths))
std = np.std(average_density_alt/len(shot_paths))

c_min = avg - (1)*std
c_max = avg + (1)*std

imagePlot = plt.imshow(average_density/len(shot_paths),vmin=c_min, vmax=c_max)

# ax_cmin = plt.axes([0.55, 0.27, 0.4, 0.03])
# ax_cmax = plt.axes([0.55, 0.23, 0.4, 0.03])
# s_cmin = Slider(ax_cmin,"min",-0.2,0.5,valinit = c_min)
# s_cmax = Slider(ax_cmax,"max",-0.2,0.5,valinit = c_max)

# def update(val, s=None):
#     _cmin = s_cmin.val
#     _cmax = s_cmax.val
#     imagePlot.set_clim([_cmin,_cmax])

# s_cmin.on_changed(update)
# s_cmax.on_changed(update)
