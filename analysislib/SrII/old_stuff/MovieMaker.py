from lyse import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from scipy.optimize import curve_fit
import scipy.constants as constants
import AnalysisSettings
################################################################################

df = data()
shot_paths = df['filepath']
images = []

fig = plt.figure()

ROI = AnalysisSettings.SGFROI

for i in range(len(shot_paths)):
    run = Run(shot_paths[i])
    OD = run.get_result_array('VerySimpleImaging','optical_depth')
    optical_depth_alt = OD[ROI[2]:ROI[3],ROI[0]:ROI[1]]
    avg = np.average(optical_depth_alt)
    std = np.std(optical_depth_alt)
    c_min = avg - (1/2)*std
    c_max = avg + (2.5)*std
    im = plt.imshow(optical_depth_alt, animated=True,vmin = c_min, vmax = c_max)
    images.append([im])

ani = animation.ArtistAnimation(fig, images, interval=50, blit=True,
                                repeat_delay=1000)

ani.save('MovieMaker.gif', writer = 'imagemagick', fps = 5)
