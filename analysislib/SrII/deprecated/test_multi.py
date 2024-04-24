from lyse import *
import matplotlib.pyplot as plt
import numpy as np
import h5py
import scipy.constants as constants
from matplotlib.widgets import Cursor, Slider
from scipy.ndimage import gaussian_filter
from scipy.signal import medfilt2d
from pprint import pprint

from Subroutines.gaussian_fit_sub import gaussian_fit_sub
import SrConstants
import AnalysisSettings
from Subroutines.FitFunctions import gauss, gauss_zero_ref

# path is the filepath to the h5 file for the run
# ser is a panda series
ser = data(path)
run = Run(path)

#for name, val in ser.items():
#    if type(name)==type(()):
#        for a in name:
#            pass
#    else:
#        print(name + ':' + str(type(val)))
#
#print(type(ser['RedMOTOn']))

run_globals = run.get_globals()
print(type(run_globals))
for name, val in run_globals.items():
    if name=='Absorption':
        print(str(val))

print('Done')