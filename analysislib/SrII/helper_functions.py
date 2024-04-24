from lyse import *
from pprint import pp as pprint
from scipy.optimize import curve_fit
import numpy as np
import h5py

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
