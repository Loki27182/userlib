from lyse import *
from pprint import pp as pprint
from scipy.optimize import curve_fit
import numpy as np
import h5py
import AnalysisSettings
import pandas as pd
#import matplotlib.pylab as plt

def saveAnalysisImage(h5_filepath,groupname,imagename,imagedata,imagetype='frame'):
    try:
        ii = 0
        with h5py.File(h5_filepath, 'r+') as f:
            groupname = 'results/' + '/'.join([str for str in groupname.split('/') if str != ''])
            image_group = f.require_group(groupname)
            group = image_group.require_group('images')


            while imagename + '_{:d}'.format(ii) in group:
                ii += 1
            
            fullImageName = imagename + '_{:d}'.format(ii)
            
            dset = group.create_dataset(
                    fullImageName, data=imagedata, dtype=str(imagedata.dtype), #compression='gzip'
                )
            dset.attrs['CLASS'] = np.string_('IMAGE')
            dset.attrs['IMAGE_VERSION'] = np.string_('1.2')
            dset.attrs['IMAGE_SUBCLASS'] = np.string_('IMAGE_GRAYSCALE')
            dset.attrs['IMAGE_WHITE_IS_ZERO'] = np.uint8(0)
    except:
        ii = -1
    return ii

def gauss(x, *p):
    a, center, width, offset = p
    return a*np.exp(-(x-center)**2/(2.*width**2)) + offset

def basic_gaussian_fit(xData,yData):
    # Find index of maximum
    idx_max = np.argmax(yData)
    # Get x and y componenents of maximum
    y_max = yData[idx_max]
    x_max = xData[idx_max]
    # Get y component of mimimum
    y_min = np.min(yData)
    # List of all x values who's corresponding y values are more than halfway up from the min to max
    x_span = xData[yData>(y_max + y_min)/2]
    # Find width of this span as an initial guess for our fit
    dx = np.max(x_span) - np.min(x_span)
    # Set up initial conditions and bounds for fit
    initial_guess = (y_max-y_min,x_max,dx,y_min)
    bounds = {'lower': [0,np.min(xData),np.mean(np.diff(xData)),y_min], 
              'upper': [10*(y_max-y_min),max(xData),10*(np.max(xData)-np.min(xData)),y_max]}
    
    # Do the fit!!!
    p, p_cov = curve_fit(gauss, xData, yData, p0=initial_guess, bounds=(bounds['lower'], bounds['upper']))
    dp = np.sqrt(np.diag(p_cov))
    return [p, dp]

def expansion_TOF(t, *p):
    w0, temp = p
    kB = 1.38*10**-23
    m = 87.9/(6.022*10**26)
    return np.sqrt(w0**2+(kB*temp/m)*t**2)

def temp_fit(t,w,t_test):
    kB = 1.38*10**-23
    m = 87.9/(6.022*10**26)
    temp_0 = m/kB*(w[-1]/t[-1])**2
    w0 = np.min(w)
    initial_guess = (w0, temp_0)
    bounds = {'lower': [0,0], 
              'upper': [np.Inf,np.Inf]}
    p, p_cov = curve_fit(expansion_TOF, t, w, p0=initial_guess, bounds=(bounds['lower'], bounds['upper']),sigma=5/(t*1000), absolute_sigma=True)
    dp = np.sqrt(np.diag(p_cov))
    w_test = expansion_TOF(t_test,*p)
    return [p, dp, w_test]

def triple_peak(x,*p):
    a, b, c, d, e, f, g = p
    return a-b*np.exp(-(x-c)^2/d^2)-e*np.exp(-(x-c-f)^2/d^2)-g*np.exp(-(x-c+f)^2/d^2)

def drop_position(t, *p):
    z0, g = p
    return z0 - g/2*t**2

def freefall_fit(t,z,t_test):
    initial_guess = (z[0], 9.8)
    bounds = {'lower': [-np.Inf,0], 
              'upper': [np.Inf,20]}
    p, p_cov = curve_fit(drop_position, t, z, p0=initial_guess, bounds=(bounds['lower'], bounds['upper']))
    dp = np.sqrt(np.diag(p_cov))
    z_test = drop_position(t_test,*p)
    return [p,dp,z_test]

def plot_the_thing(ax,x,y,xlab,ylab,titleStr,plottype='linear'):
    ax.plot(x,y,'--x')
    ax.set_xlabel(xlab,fontsize=20)
    ax.set_ylabel(ylab,fontsize=20)
    if titleStr not in {''}:
        ax.title.set_text(titleStr)
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    ax.set_ylim([np.min([0,np.min(y)*1.1]),np.max([0,np.max(y)*1.1])])
    ax.grid(True)
    ax.set_xscale(plottype)

def plot_the_thing_2D(ax,fig,x,y,z,xlab,ylab,titleStr,type1='linear',type2='linear'):
    image = ax.imshow(np.flipud(z),extent=[np.min(x),np.max(x),np.min(y),np.max(y)],vmin=np.min(z),vmax=np.max(z))
    cb = fig.colorbar(image, ax=ax)
    cb.set_label(titleStr,fontsize=14)
    if type1 is 'linear':
        ax.set_xlabel(xlab,fontsize=14)
    else:
        ax.set_xlabel(xlab + ' (' + type1 + ')',fontsize=14)
    if type2 is 'linear':
        ax.set_ylabel(ylab,fontsize=14)
    else:
        ax.set_ylabel(ylab + ' (' + type2 + ')',fontsize=14)
    #ax.set_ylabel(ylab,fontsize=14)
    ax.set_aspect('auto')
    #ax.title.set_text(titleStr)
    #ax.title.set_size(14)
    #ax.invert_yaxis()

def get_scale(x):
    if np.any(x <= 0):
        scale_type = 'linear'
    else:
        dx = np.diff(x)
        dx_err = np.mean(((dx - np.mean(dx))/np.mean(dx))**2)**.5
        dx_log = np.diff(np.log10(x))
        dx_log_err = np.mean(((dx_log - np.mean(dx_log))/np.mean(dx_log))**2)**.5
        if dx_log_err < dx_err/10:
            scale_type = 'log'
        else:
            scale_type = 'linear'
    return scale_type

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
