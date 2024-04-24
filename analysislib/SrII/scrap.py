from lyse import *
import matplotlib.pyplot as plt
from pprint import pp as pprint
import numpy as np
import h5py
import scipy.constants as constants
from matplotlib.widgets import Cursor, Slider, CheckButtons, TextBox, Button
from scipy.ndimage import gaussian_filter
from scipy.signal import medfilt2d
from time import perf_counter as pc
import matplotlib.patches as patches
from helper_functions import saveAnalysisImage

def getExponent(n):
    return np.floor(np.log10(n))


print(getExponent(10))
