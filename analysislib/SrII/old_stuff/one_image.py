from lyse import *
import matplotlib.pyplot as plt
import numpy as np

ser = data(path)
run = Run(path)


im_one = run.get_image('grating','fluorescence','atoms').astype('float')
im_background = run.get_image('grating', 'fluorescence', 'background')
avg = np.average(im_one-im_background)
std = np.std(im_one-im_background)
c_min = avg - (.5)*std
c_max = avg + (2.5)*std
plt.imshow(im_one-im_background, vmin = c_min, vmax = c_max)
#print(np.average(im_one))
#run.save_result('clear_average',np.average(im_one))
