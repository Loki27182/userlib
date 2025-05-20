from lyse import *
import numpy as np
from helper_functions import get_scale
import AnalysisSettings
import pandas as pd

def load_data(cameras={'horizontal','xz','yz'},var_names={}):
    all_run_data = data()
    default_variables = {'labscript','sequence','sequence_index','run number','run repeat','run time','n_runs','filepath','agnostic_path'}

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

    idxs_all = [[idx for idx, val in enumerate(run_sequence_numbers) if val == val0] for val0 in np.unique(run_sequence_numbers)]
    idx0 = [idxs[0] for idxs in idxs_all]
    first_paths = ['\\'.join(path) for idx_pth, path in enumerate(run_paths) if idx_pth in idx0]

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

    all_var_ranges = [{ name: [np.min(np.array(eval(val.replace('linspace','np.linspace').replace('logspace','np.logspace')))), 
                               np.max(np.array(eval(val.replace('linspace','np.linspace').replace('logspace','np.logspace'))))]
                                if not isinstance(eval(val.replace('linspace','np.linspace').replace('logspace','np.logspace')),type('')) 
                                else [0,0]
                            for name, val in Run(filepath).get_globals_raw().items() 
                        if np.size(np.array(eval(val.replace('linspace','np.linspace').replace('logspace','np.logspace')))) > 1 
                    } 
                    for filepath in first_paths
                ]

    all_var_names = [{name for name in var_range} for var_range in all_var_ranges]

    for idx, var_names in enumerate(all_var_names):
        if idx==0:
            unique_var_names = var_names
        else:
            unique_var_names = unique_var_names | var_names

    var_ranges = {}
    for var_ranges_ii in all_var_ranges:
        for var_name, var_range in var_ranges_ii.items():
            if var_name not in var_ranges:
                var_ranges[var_name] = var_range
            else:
                var_ranges[var_name] = [np.min([var_range,var_ranges[var_name]]),np.max([var_range,var_ranges[var_name]])]

    display_variable_info = dict()
    for name, val in var_ranges.items():
        try:
            plot_title = AnalysisSettings.variable_info[name]['plot_title']
            axis_label = AnalysisSettings.variable_info[name]['axis_label']
            axis_scale = AnalysisSettings.variable_info[name]['scale']
        except:
            plot_title = 'Varying ' + name
            axis_label = name
            axis_scale = 1
        display_variable_info[name] = dict()
        display_variable_info[name]['plot_title'] = plot_title
        display_variable_info[name]['axis_label'] = axis_label
        display_variable_info[name]['axis_scale'] = axis_scale
        display_variable_info[name]['values'] = variables[name]
        display_variable_info[name]['unique_values'] = np.unique(display_variable_info[name]['values'])
        display_variable_info[name]['range'] = val
        display_variable_info[name]['loglin'] = get_scale(display_variable_info[name]['values'])


    return variables, iterated_variables, results, filepaths, first_paths

def load_iterated_data():
    column_names = data(n_sequences=0).columns
    n_mi = len(column_names[0])

    default_variables = ['labscript','sequence','sequence_index','run number','run repeat','run time','n_runs','filepath']
    def_var_idx = [name_to_idx(var_name,n_mi) for var_name in default_variables]

    run_info = data(filter_kwargs={'items':def_var_idx})
    script_names = np.array([[a[0:-3]] for a in run_info['labscript'].values])
    run_dates = np.array([str(a)[0:10].split('-') for a in run_info['sequence'].values])
    seq_idxs = np.array([[str(a)] for a in run_info['sequence_index'].values])
    run_uid = ['_'.join(nameparts) for nameparts in np.concatenate((script_names,run_dates,seq_idxs),axis=1)]
    idxs_all = [[idx for idx, val in enumerate(run_uid) if val == val0] for val0 in np.unique(run_uid)]
    idx0 = [idxs[0] for idxs in idxs_all]
    run_sample_filepaths = run_info['filepath'].values[idx0]
    all_var_ranges = [{ name: [np.min(np.array(eval(val.replace('linspace','np.linspace').replace('logspace','np.logspace')))), 
                               np.max(np.array(eval(val.replace('linspace','np.linspace').replace('logspace','np.logspace'))))]
                                if not isinstance(eval(val.replace('linspace','np.linspace').replace('logspace','np.logspace')),type('')) 
                                else [0,0]
                            for name, val in Run(filepath).get_globals_raw().items() 
                        if np.size(np.array(eval(val.replace('linspace','np.linspace').replace('logspace','np.logspace')))) > 1 
                    } 
                    for filepath in run_sample_filepaths
                ]

    var_ranges = {}
    for var_ranges_ii in all_var_ranges:
        for var_name, var_range in var_ranges_ii.items():
            if var_name not in var_ranges:
                var_ranges[var_name] = var_range
            else:
                var_ranges[var_name] = [np.min([var_range,var_ranges[var_name]]),np.max([var_range,var_ranges[var_name]])]

    var_idx = [name_to_idx(name,n_mi) for name, val in var_ranges.items()]

    variable_info = []
    if len(var_ranges)>0:
        for idx, (varname, varrange) in enumerate(var_ranges.items()):
            try:
                axis_label = AnalysisSettings.variable_info[varname]['axis_label']
            except:
                axis_label = varname
            try:
                axis_scale = AnalysisSettings.variable_info[varname]['scale']
            except:
                axis_scale = 1
            try:
                prefer_x = AnalysisSettings.variable_info[varname]['prefer_x']
            except:
                prefer_x = 0
            temp_dict = dict()
            temp_dict['name'] = varname
            temp_dict['axis_label'] = axis_label
            temp_dict['prefer_x'] = prefer_x
            temp_dict['axis_scale'] = np.array(axis_scale)
            temp_dict['values'] = data(filter_kwargs={'items':[var_idx[idx]]}).values
            temp_dict['range'] = varrange
            temp_dict['loglin'] = get_scale(temp_dict['values'])
            variable_info.append(temp_dict)
    else:
        temp_dict['name'] = 'Time'
        temp_dict['axis_label'] = 'Time'
        temp_dict['prefer_x'] = 0
        temp_dict['axis_scale'] = np.array(1.0)
        temp_dict['values'] = pd.to_datetime(data(filter_kwargs={'items':['run time']}).values)
        temp_dict['range'] = [np.min(temp_dict['values']),np.max(temp_dict['values'])]
        temp_dict['loglin'] = 'linear'
        variable_info.append(temp_dict)

    result_info = dict()
    for name in column_names:
        if name[0]=='single':
            result_info[name[1]] = dict()
            result_info[name[1]]['imaging_axis'] = name[1].split('/')[0]
            result_info[name[1]]['result_type'] = name[1].split('/')[-1]
            try:
                axis_label = AnalysisSettings.result_info[result_info[name[1]]['result_type']]['axis_label']
            except:
                axis_label = name[1]
            try:
                axis_scale = AnalysisSettings.result_info[result_info[name[1]]['result_type']]['scale']
            except:
                axis_scale = 1
            try:
                plot_flag = AnalysisSettings.result_info[result_info[name[1]]['result_type']]['plot_flag']
            except:
                plot_flag = False
            result_info[name[1]]['axis_label'] = np.array(axis_label)
            result_info[name[1]]['plot_flag'] = plot_flag
            result_info[name[1]]['axis_scale'] = axis_scale
            result_info[name[1]]['values'] = data(filter_kwargs={'items':[name]}).values

    save_paths = []
    for filepath in run_sample_filepaths:
        directory = '\\'.join(filepath.split('\\')[0:-2]) + '\\'
        basename = filepath.split('\\')[-2] + '\\'
        save_paths.append(directory + basename)

    return variable_info, result_info, save_paths

def name_to_idx(name,n):
    name_idx = (name,)
    for idx in range(n-1):
        name_idx = name_idx + ('',)
    return name_idx

