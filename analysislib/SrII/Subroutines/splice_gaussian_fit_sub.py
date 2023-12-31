import numpy as np
import h5py
from scipy.optimize import curve_fit
from Subroutines.FitFunctions import gauss


def splice_gaussian_fit_sub(image, fix_center):

    # Find Size of Image
    x_length = np.shape(image)[1]
    z_length = np.shape(image)[0]

    z = np.arange(z_length)
    x = np.arange(x_length)

    # Get Center
    with h5py.File('current_roi.h5', 'a') as f:
        if 'center' not in f.attrs:
            f.attrs.create('center', (x_length / 2, z_length / 2))
        center = f.attrs['center']

    # Slice At Center
    z_slice_point = 0 if center[1] < 0 else z_length-1 if center[1] >= z_length else center[1]
    x_slice_point = 0 if center[0] < 0 else x_length - 1 if center[0] >= x_length else center[0]

    # Search For Atoms If There Are None At The Center
    #if image[int(z_slice_point)][int(x_slice_point)] < 0.3 and not fix_center:
    #    for i in range(1000):
    #        guess = (np.random.randint(x_length - 1), np.random.randint(z_length - 1))
    #        if image[guess[1]][guess[0]] > 0.3:
    #            z_slice_point = guess[1]
    #            x_slice_point = guess[0]
    #            break

    # Slice Image
    #image_x = image[int(z_slice_point)]
    #image_z = image[:, int(x_slice_point)]
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

    # Iterate Fits
    try:
        #for i in range(2):
        p_opt_z, p_cov_z = curve_fit(gauss, z, image_z, p0=initial_guess_z, bounds=([0, -np.inf, 0, -np.inf], [np.inf, np.inf, np.inf, np.inf]))
        #z_slice_point = 0 if p_opt_z[1] < 0 else z_length-1 if p_opt_z[1] >= z_length else p_opt_z[1]
        #image_x = image[int(z_slice_point)]
        #initial_guess_z = p_opt_z

        p_opt_x, p_cov_x = curve_fit(gauss, x, image_x, p0=initial_guess_x, bounds=([0, -np.inf, 0, -np.inf], [np.inf, np.inf, np.inf, np.inf]))
        #x_slice_point = 0 if p_opt_x[1] < 0 else x_length - 1 if p_opt_x[1] >= x_length else p_opt_x[1]
        #image_z = image[:, int(x_slice_point)]
        #initial_guess_x = p_opt_x
    except RuntimeError:
        p_opt_x = (-.001, 0, 1, 0)
        p_cov_x = np.zeros((4,4))
        p_opt_z = (-.001, 0, 1, 0)
        p_cov_z = np.zeros((4,4))
        pass

    # Save New Center
    with h5py.File('current_roi.h5', 'a') as f:
        if p_opt_x[0] > 0.2 and not fix_center:
            f.attrs['center'] = (p_opt_x[1], p_opt_z[1])

    # Fit Found Something Artificial
    #if p_opt_x[2] < 5 or p_opt_z[2] < 5:
    #    p_opt_x = (-.001, 0, 1, 0)
    #    p_opt_z = (-.001, 0, 1, 0)

    # Return Everything
    return[x, image_x, p_opt_x, p_cov_x, z, image_z, p_opt_z, p_cov_z]
