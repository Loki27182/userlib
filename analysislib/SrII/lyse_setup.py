from lyse import *
import numpy as np
from numpy import *
import runmanager.remote as rm

def load_data(cameras={'horizontal'}):
    all_run_data = data()
    default_variables = {'labscript','sequence','sequence_index','run number','run repeat','run time','n_runs','filepath','agnostic_path'}
    run = Run(all_run_data.filepath.iloc[-1])
    run_globals = run.get_globals_raw()
    
    all_iterated_variables = {name: val for name, val in run_globals.items() if np.size(np.array(eval(val)))>1}


    for cam in cameras:
        default_variables.add(cam)

    variables = dict()
    for tags in all_run_data.columns:
        if tags[1]=='' and tags[0] not in default_variables:
            variables[tags[0]] = all_run_data[tags[0]].values
    
    iterated_variables = {name: val for name, val in variables.items() if len(np.unique(val))>1}

    results = dict()
    for tags in all_run_data.columns:
        if (tags[0] not in variables.keys()) and (tags[0] not in default_variables):
            results[tags[1].split('/')[-1]] = all_run_data[tags].values
    
    

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

        basepath = '\\'.join(path[0:-2]) + '\\'
        filename = '{:s}-{:s}-{:s}_{:s}_{:s}_multishot'.format(y,m,d,s,n)

        if basepath + filename not in filepaths:
            filepaths.append(basepath + filename)

    return variables, iterated_variables, results, filepaths, all_iterated_variables