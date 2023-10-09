import numpy as np
import h5py
from scipy.optimize import curve_fit
from Subroutines.FitFunctions import gauss, gauss_zero_ref


def gaussian_fit_sub(image, zero_ref = False):

    # Find Size of Image
    x_length = np.shape(image)[1]
    z_length = np.shape(image)[0]

    z = np.arange(z_length)
    x = np.arange(x_length)

    image_x = np.sum(image,0)
    image_z = np.sum(image,1)

    # Make Initial Guess
    a_x=np.max(image_x)-np.min(image_x)
    a_z=np.max(image_z)-np.min(image_z)
    offset_x=np.min(image_x)
    offset_z=np.min(image_z)
    center_x=int(np.average(np.argmax(image_x)))
    center_z=int(np.average(np.argmax(image_z)))
    initial_guess_x = (a_x, center_x, 150, offset_x)
    initial_guess_z = (a_z, center_z, 150, offset_z)


    try:
        if not zero_ref:
            p_opt_z, p_cov_z = curve_fit(gauss, z, image_z, p0=initial_guess_z, bounds=([0, -np.inf, 0, -np.inf], [np.inf, np.inf, np.inf, np.inf]))
            p_opt_x, p_cov_x = curve_fit(gauss, x, image_x, p0=initial_guess_x, bounds=([0, -np.inf, 0, -np.inf], [np.inf, np.inf, np.inf, np.inf]))
        else:
            p_opt_z, p_cov_z = curve_fit(gauss_zero_ref, z, image_z, p0=initial_guess_z[0:3], bounds=([0, -np.inf, 0], [np.inf, np.inf, np.inf]))
            p_opt_x, p_cov_x = curve_fit(gauss_zero_ref, x, image_x, p0=initial_guess_x[0:3], bounds=([0, -np.inf, 0], [np.inf, np.inf, np.inf]))
    except RuntimeError:
        p_opt_x = (-.001, 0, 1, 0)
        p_cov_x = np.zeros((4,4))
        p_opt_z = (-.001, 0, 1, 0)
        p_cov_z = np.zeros((4,4))
        pass
    
    return[x, image_x, p_opt_x, p_cov_x, z, image_z, p_opt_z, p_cov_z]
