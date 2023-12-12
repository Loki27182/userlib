import numpy as np

def black_level (gain, mode=7, p_0=1):
    # Calculates the correct black level for the Grasshopper camera for a given
    # mode (0 or 7, with 7 being the lower noise but slower mode), gain setting
    # (from -3 to 24, in dB), and p_0 (expected number of pixels that will read
    # as zero based on readout noise)

    # Hard coding this in since this function is currently specific to this camera
    ccd_size = [1448,1920]
    print(type(ccd_size))
    # Check that gain and p_0 inputs are valid
    if gain<-3 or gain>24:
        raise ValueError("gain must be in the range of -3 to 24")
    if p_0<0 or p_0>np.prod(ccd_size):
        raise ValueError("p_0 must be strictly greater than 0 and less than %n" % np.prod(ccd_size))
    
    # Check that mode is valid, and set constants according to calibration
    match mode:
        case 0:
            s_0 = 4.4
            s_1 = -3.8
        case 7:
            s_0 = 3.32
            s_1 = 1.41
        case _:
            raise ValueError("mode must be either 0 or 7")
    
    # Set/Calculate some constants
    s = s_0*10**(gain/20)
    p = p_0/np.prod(ccd_size)
    black_level_max = 6.25*1018/1024

    # Calculate required black level to have on average p_0 zero counts on a dark
    # image for the given settings
    black_level = (np.sqrt(-np.log(p*s*np.sqrt(2*np.pi))*2*s**2)+s_1*s/s_0)*100/2**12

    # Clip to allowed range (this only really happens for either mode if you make p_0 
    # very small, and/or have very high gain)
    if black_level<0:
        black_level = 0
    elif black_level>black_level_max:
        black_level = black_level_max

    # Round value to closest value the camera is expecting - this isn't really necessary, but oh well
    black_level = np.round(black_level*1018/black_level_max)*black_level_max/1018

    # Return calculated value
    return black_level