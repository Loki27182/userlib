from lyse import *
import numpy as np
import h5py
import matplotlib.pyplot as plt
from pprint import pp as pprint
import scipy.constants as constants
from matplotlib.widgets import Cursor, Slider, CheckButtons, TextBox, Button
from scipy.ndimage import gaussian_filter
from scipy.signal import medfilt2d
from time import perf_counter as pc
import matplotlib.patches as patches
from helper_functions import basic_gaussian_fit, saveAnalysisImage

all_run_data = data()

default_variables = {'labscript','sequence','sequence_index','run number','run repeat','run time','n_runs','filepath','agnostic_path'}
camera_variables = {'camera'}
variables = dict()
for tags in all_run_data.columns:
    pprint(tags)
    if (len(tags)<2 or tags[1]=='') and tags[0] not in default_variables and tags[0] not in camera_variables:
        variables[tags[0]] = all_run_data[tags[0]].values

results = dict()
for tags in all_run_data.columns:
    if (tags[0] not in variables.keys()) and (tags[0] not in default_variables):
        results[tags[1].split('/')[-1]] = all_run_data[tags].values 

run_paths = [(path.split('\\')) for path in all_run_data['filepath'].values]
run_years = [a[-5] for a in run_paths]
run_months = [a[-4] for a in run_paths]
run_days = [a[-3] for a in run_paths]
run_sequence_numbers = [a[-2] for a in run_paths]
run_names = all_run_data['labscript'].values

filepaths = []
for ii, path in enumerate(run_paths):
    y = run_years[ii]
    m = run_months[ii]
    d = run_days[ii]
    s = run_sequence_numbers[ii]
    n = run_names[ii][0:-3]

    basepath = '\\'.join(path[0:-1])
    filename = '{:s}-{:s}-{:s}_{:s}_{:s}_multishot'.format(y,m,d,s,n)
    fullname = basepath + '\\' + filename
    if fullname not in filepaths:
        filepaths.append(fullname)
