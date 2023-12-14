from lyse import *
import matplotlib.pyplot as plt
import numpy as np
import h5py
import scipy.constants as constants
from matplotlib.widgets import Cursor, Slider
from scipy.optimize import curve_fit
from scipy.ndimage import gaussian_filter

from Subroutines.gaussian_fit_sub import gaussian_fit_sub
import SrConstants
import AnalysisSettings
from Subroutines.FitFunctions import gauss, gauss_zero_ref

ser = data(path)
run = Run(path)

camera = AnalysisSettings.Camera

x0 = 960
y0 = 724

w = 900
h = 700

ROI = [x0-w,x0+w+1,y0-h,y0+h+1]


print('Loading variables...')
try:
    PulseDuration = ser['PulseDuration']
except:
    print("PulseDuration does not exist for this run")
print('Variables loaded')

print('Loading images...')
im_bright = run.get_image(camera,'images','bright').astype('float')
im_dark = run.get_image(camera,'images','dark').astype('float')
print('Images loaded')

print('Analyzing...')

im_bright = im_bright[ROI[2]:ROI[3],ROI[0]:ROI[1]]
im_dark = im_dark[ROI[2]:ROI[3],ROI[0]:ROI[1]]
im_act = im_bright - im_dark

im_bright_avg = np.mean(im_bright)
im_bright_min = np.min(im_bright)
im_bright_max = np.max(im_bright)

im_dark_avg = np.mean(im_dark)
im_dark_min = np.min(im_dark)
im_dark_max = np.max(im_dark)

im_act_avg = np.mean(im_act)
im_act_min = np.min(im_act)
im_act_max = np.max(im_act)


edges = np.arange(-302,2**16,4)

counts_bright, bins_bright = np.histogram(np.ndarray.flatten(im_bright),edges)
counts_dark, bins_dark = np.histogram(np.ndarray.flatten(im_dark),edges)
counts_act, bins_act = np.histogram(np.ndarray.flatten(im_act),edges)
plt_max = np.max(counts_bright[0:-1])
p_round = np.floor(np.log10(plt_max))-1
plt_max = np.ceil(plt_max*1.1/10**p_round)*10**p_round

x = bins_act[0:-1]+(bins_act[1]-bins_act[0])/2
y = counts_act

n0 = 10
n_ignore = 200
kernel_size = 50
counts_act_extended = np.concatenate((np.ones(kernel_size)*counts_act[0],counts_act[0:-n_ignore],np.ones(kernel_size)*np.mean(counts_act[-n_ignore-kernel_size:-n_ignore])))
kernel = np.ones(kernel_size) / kernel_size
counts_act_smooth = np.convolve(counts_act_extended, kernel, mode='full')
counts_act_smooth1 = counts_act_smooth[np.int64(3*kernel_size/2-1):-np.int64(3*kernel_size/2)]

kernel_size = np.int64(np.argmax(counts_act_smooth1)/n0/2)*2
kernel = np.ones(kernel_size) / kernel_size
counts_act_extended = np.concatenate((np.ones(kernel_size)*counts_act[0],counts_act[0:-n_ignore],np.ones(kernel_size)*np.mean(counts_act[-n_ignore-kernel_size:-n_ignore])))
counts_act_smooth = np.convolve(counts_act_extended, kernel, mode='full')
counts_act_smooth = counts_act_smooth[np.int64(3*kernel_size/2-1):-np.int64(3*kernel_size/2)]
#counts_act_smooth = counts_act_smooth[kernel_size:-kernel_size]
n_max = x[np.argmax(counts_act_smooth)]

print('Analysis done.')

print('Plotting..')

plt.rcParams['text.usetex'] = True
fig = plt.figure()

fig.suptitle('Pulse Duration = ' + '{:1.0f}'.format(PulseDuration*1e6) + ' $\mu$s')

bright_hist_ax = fig.add_subplot(2,2,1)
dark_hist_ax = fig.add_subplot(2,2,2)
act_hist_ax = fig.add_subplot(2,2,3)
act_plt_ax = fig.add_subplot(2,2,4)

bright_hist = bright_hist_ax.plot(bins_bright[0:-1]+(bins_bright[1]-bins_bright[0])/2, counts_bright)
bright_hist_ax.title.set_text('Bright Image\nAverage = ' + '{:1.0f}'.format(im_bright_avg) +', Min =' + '{:1.0f}'.format(im_bright_min) + ', Max = ' + '{:1.0f}'.format(im_bright_min))
bright_hist_ax.grid(True)
bright_hist_ax.set_ylim(0,plt_max)
bright_hist_ax.set_xlim(-300,2**16-2)

dark_hist = dark_hist_ax.plot(bins_dark[0:-1]+(bins_dark[1]-bins_dark[0])/2, counts_dark)
dark_hist_ax.title.set_text('Dark Image\nAverage = ' + '{:1.0f}'.format(im_dark_avg) +', Min =' + '{:1.0f}'.format(im_dark_min) + ', Max = ' + '{:1.0f}'.format(im_dark_min))
dark_hist_ax.grid(True)

act_hist = act_hist_ax.plot(x, y,'.')
act_hist = act_hist_ax.plot(x[0:-n_ignore], counts_act_smooth,'--')
#act_hist = act_hist_ax.plot(bins_act[0:-1]+(bins_act[1]-bins_act[0])/2, act_hist_fit/1e3,'--')
#act_hist = act_hist_ax.plot(bins_act[0:-1]+(bins_act[1]-bins_act[0])/2, act_hist_guess/1e3,'--')
#act_hist = act_hist_ax.plot(bins_act[0:-2-n_ignore-n_ignore]+(bins_act[1]-bins_act[0])/2, counts_act_smooth,'--')
act_hist_ax.title.set_text('Subtracted Image\nAverage = ' + '{:1.0f}'.format(im_act_avg) +', Min =' + '{:1.0f}'.format(im_act_min) + ', Max = ' + '{:1.0f}'.format(im_act_min))
act_hist_ax.grid(True)
act_hist_ax.set_ylim(0,plt_max)
act_hist_ax.set_xlim(-300,2**16-2)

#a=act_plt_ax.plot(counts_act_extended)

imagePlot = act_plt_ax.imshow(im_act, vmin=0, vmax=im_act_max)
fig.colorbar(imagePlot, ax=act_plt_ax)
act_plt_ax.axis('off')

print('Plotting done')


print('Saving plot...')
datapath = path.split('\\')
savepath = '\\'.join(datapath[0:-1]) + '\\' + '{:1.0f}'.format(PulseDuration*1e6) + '_histogram.png'
plt.savefig(savepath)
print('Plot saved')


print('Saving data...')
run.save_result('im_mean', im_act_avg)
run.save_result('n_max', n_max)
run.save_result('PulseDuration', PulseDuration)

print('Data saved')
print('Complete')


