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

default_variables = {'labscript','sequence','sequence_index','run number','run repeat','run time','n_runs','filepath','agnostic_path','horizontal'}

variables = dict()
for tags in all_run_data.columns:
    if tags[1]=='' and tags[0] not in default_variables:
        variables[tags[0]] = all_run_data[tags[0]].values

#pprint(variables)
results = dict()
for tags in all_run_data.columns:
    if (tags[0] not in variables.keys()) and (tags[0] not in default_variables):
        results[tags[1].split('/')[-1]] = all_run_data[tags].values

#results = {tags[1].split('/')[-1]: all_run_data[tags].values for tags in all_run_data.columns if (tags[0] not in variables.keys()) and (tags[0] not in default_variables)}
#pprint(results)

run_paths = [(path.split('\\')) for path in all_run_data['filepath'].values]
run_years = [a[5] for a in run_paths]
run_months = [a[6] for a in run_paths]
run_days = [a[7] for a in run_paths]
run_sequence_numbers = [a[8] for a in run_paths]
run_names = all_run_data['labscript'].values

filepaths = []
for ii, path in enumerate(run_paths):
    y = run_years[ii]
    m = run_months[ii]
    d = run_days[ii]
    s = run_sequence_numbers[ii]
    n = run_names[ii][0:-3]

    basepath = '\\'.join(path[0:-1]) + '\\'
    filename = '{:s}-{:s}-{:s}_{:s}_{:s}_multishot'.format(y,m,d,s,n)

    if filename not in filepaths:
        filepaths.append(basepath + filename)

#filepaths =np.unique(['\\'.join(path[0:-1]) + '\\{:s}-{:s}-{:s}_{:s}_{:s}_multishot'.format(run_years[ii],run_months[ii],run_days[ii],run_sequence_numbers[ii],run_names[ii][0:-3]) for ii, path in enumerate(run_paths)])
