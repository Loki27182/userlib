from __future__ import division
from pylab import *

# #############################################
# The following functions are part of the
# "standard load" of functions and should not
# be messed with. They are here for reference only.
# #############################################

__all__ = [
           'QuinticRamp',
           'LineRamp',
           'ExpRamp',
           'TimeInExp',
           'ClampedExpRamp',
           'EvapRamp',
           'EvapRampOffset',
           'Cf2',
           'Cf2Back',
           'Poly4Line',
           'CoilTime',
           'Vmix',
           'Cf4',
           'Cf5',
           'Cf5Back',
           'Cf',
           'ChirpRamp',
           'PolyExp',
           'Poly4',
           'Poly4_shift',
           'Poly4Asymmetric',
           'PolyHalf1',
           'PolyHalf1_shift',
           'PolyHalf2',
           'HalfGaussRamp',
           'Blackman',
           'TrnSin',
           'SinRamp',
           'SmoothAccelerationRamp',
           'EvapRampOffsetLocal',
           ]


def QuinticRamp(
    t,
    duration,
    initial,
    final,
    initial_deriv=0,
    final_deriv=0,
    initial_accel=0,
    final_accel=0,
):
    """A quantic with the given values, derivatives and second derivatives at two
    points."""
    from numpy.polynomial import Polynomial
    import numpy as np

    x0 = 0
    x1 = duration
    y0 = initial
    y1 = final
    dydx0 = initial_deriv
    dydx1 = final_deriv
    d2y_dx20 = initial_accel
    d2y_dx21 = final_accel

    coeffs = np.linalg.solve(
        [
            [1, x0, x0 ** 2, x0 ** 3, x0 ** 4, x0 ** 5],
            [1, x1, x1 ** 2, x1 ** 3, x1 ** 4, x1 ** 5],
            [0, 1, 2 * x0, 3 * x0 ** 2, 4 * x0 ** 3, 5 * x0 ** 4],
            [0, 1, 2 * x1, 3 * x1 ** 2, 4 * x1 ** 3, 5 * x1 ** 4],
            [0, 0, 2, 6 * x0, 12 * x0 ** 2, 20 * x0 ** 3],
            [0, 0, 2, 6 * x1, 12 * x1 ** 2, 20 * x1 ** 3],
        ],
        [y0, y1, dydx0, dydx1, d2y_dx20, d2y_dx21],
    )
    return Polynomial(coeffs)(t)


def LineRamp(t, duration, Initial, Final):
    """Creates a linear ramp from A to B"""
    f = t / duration
    return (1 - f) * Initial + f * Final


def ExpRamp(t, duration, a, b, tau):
    """Creates an exponential ramp from A to B"""
    return (b - a * exp(duration / tau) + (a - b) * exp(t / tau)) / (1 - exp(duration / tau))



def TimeInExp(y, a, b, tau, duration):

    """

    For an exponential that runs from a to b with a time constant tau

    and duration t



    return the time at which it reaches the level y

    """

    if y > a and y > b: # y is too large

        # y too large, so return the time associated with the closer bound

        return 0.0 if a > b else duration

    elif y < a and y < b: # y is too large

        # y too small,  return the time associated with the closer bound

        return 0.0 if a < b else duration

    else: # Otherwise compute

        aa = a - y

        bb = b - y

        t = tau * np.log( (aa*np.exp(duration/tau)-bb) / (aa-bb) )

def ClampedExpRamp(t, duration, a, b, zero, tau, minimum, maximum):
    import numpy as np
    (b - a * exp(duration / tau) + (a - b) * exp(t / tau)) / (1 - exp(duration / tau))
    output = zero + (a - zero)*exp(-t/tau)
    if a >= b:
        np.clip(output, max(b,minimum), min(a,maximum), out = output)
    elif a < b:
        np.clip(output, max(a,minimum), min(b,maximum), out = output)
    return (output)


def SinRamp(t, duration, Offset, A, Freq, Phase):
    """Creates a sinewave"""
    return Offset + A * sin(2 * pi * Freq * t + Phase)


def ChirpRamp(t, duration, Offset, A, f0, f1, Phase):
    """Creates a linear chirp wave"""
    chirp_rate = (f1 - f0)/duration
    Freq = f0 + chirp_rate * t
    return Offset + A * sin(2 * pi * Freq * t + Phase)

def Blackman(t, duration, Offset, A):
    """Creates a blackman pulse"""
    f = t / duration
    return (Offset + A * sqrt(0.5 * cos(pi * (2 * f - 1)) + 0.08 * cos(2 * pi * (2 * f - 1)) + 0.42))


def HalfGaussRamp(t, duration, a, b, width):
    """Creates a half-gauss ramp"""
    y = exp(-(duration ** 2) / width ** 2)
    y = (a - b * y) / (1 - y) + ((b - a) / (1 - y)) * exp(-((t - duration) ** 2) / width ** 2)
    return y


def EvapRamp(t, duration, a, b, tau):
    """Creates an "O'Hara" ramp from A to B, for dipole evaporation"""
    y = log(a / b) / log(1 + duration / tau)
    y = a * (1 + t / tau) ** (-y)
    return y

def EvapRampOffset(t, duration, U_I, U_F, U_0, tau):
   """Creates an "O'Hara" evaporation ramp from U_I to U_F assuming a trap bottom at U_0 and
   a time-constant tau"""

   alpha = log( (U_I - U_0)/(U_F - U_0) ) / log(1 + duration/tau)

   return U_0 + (U_I - U_0) * (1 + t/tau)**(-alpha)


def Poly4(t, duration, step, A, B, C, Cf=None):
    """Transfer coil function, standard three segment

    Cf, if not None, should be a list or tuple, the first element
    of which is a Cf function for scaling the time coordinate,
    and the other elements the arguments to be passed to it.
    The normalised time coordinate f will then be calculated as:

    f = Cf_func(t, duration, *Cf_args)

    instead of:

    f = t / duration
    """
    if Cf is None:
        f = t / duration
    else:
        Cf_func = Cf[0]
        Cf_args = Cf[1:]
        f = Cf_func(t, duration, *Cf_args)
    f0 = (f + step) / 3
    return Poly4Asymmetric(f0, None, A, B, C, 1, time_argument_is_f=True)


def Poly4_shift(t, duration, step, A, B, C, shift, Cf=None):
    """Transfer coil function, standard three segment

    Cf, if not None, should be a list or tuple, the first element
    of which is a Cf function for scaling the time coordinate,
    and the other elements the arguments to be passed to it.
    The normalised time coordinate f will then be calculated as:

    f = Cf_func(t, duration, *Cf_args)

    instead of:

    f = t / duration
    """
    if Cf is None:
        f = t / duration
    else:
        Cf_func = Cf[0]
        Cf_args = Cf[1:]
        f = Cf_func(t, duration, *Cf_args)
    f0 = (f + step) / 3
    return Poly4Asymmetric(f0, None, A, B, C, 1, time_argument_is_f=True) + shift



def PolyExp(t, duration, step, A, B, C, D, Cf=None):
    """Transfer coil function, standard three segment with exponent

    Cf, if not None, should be a list or tuple, the first element
    of which is a Cf function for scaling the time coordinate,
    and the other elements the arguments to be passed to it.
    The normalised time coordinate f will then be calculated as:

    f = Cf_func(t, duration, *Cf_args)

    instead of:

    f = t / duration
    """
    if Cf is None:
        f = t / duration
    else:
        Cf_func = Cf[0]
        Cf_args = Cf[1:]
        f = Cf_func(t, duration, *Cf_args)
    f0 = (f + step) / 3
    return Poly4Asymmetric(f0, None, A, B, C, D, time_argument_is_f=True)


def PolyHalf1(t, duration, step, A, B, C, Cf=None):
    """Transfer coil function, standard three segment

    Cf, if not None, should be a list or tuple, the first element
    of which is a Cf function for scaling the time coordinate,
    and the other elements the arguments to be passed to it.
    The normalised time coordinate f will then be calculated as:

    f = Cf_func(t, duration, *Cf_args)

    instead of:

    f = t / duration
    """
    if Cf is None:
        f = t / duration
    else:
        Cf_func = Cf[0]
        Cf_args = Cf[1:]
        f = Cf_func(t, duration, *Cf_args)
    f0 = (f + step + 0) / 4
    return Poly4Asymmetric(f0, None, A, B, C, 1, time_argument_is_f=True)

def PolyHalf1_shift(t, duration, step, A, B, C,shift4, Cf=None):
    """Transfer coil function, standard three segment

    Cf, if not None, should be a list or tuple, the first element
    of which is a Cf function for scaling the time coordinate,
    and the other elements the arguments to be passed to it.
    The normalised time coordinate f will then be calculated as:

    f = Cf_func(t, duration, *Cf_args)

    instead of:

    f = t / duration
    """
    if Cf is None:
        f = t / duration
    else:
        Cf_func = Cf[0]
        Cf_args = Cf[1:]
        f = Cf_func(t, duration, *Cf_args)
    f0 = (f + step + 0) / 4
    return Poly4Asymmetric(f0, None, A, B, C, 1, time_argument_is_f=True) + shift4


def PolyHalf2(t, duration, step, A, B, C, Cf=None):
    """Transfer coil function, standard three segment

    Cf, if not None, should be a list or tuple, the first element
    of which is a Cf function for scaling the time coordinate,
    and the other elements the arguments to be passed to it.
    The normalised time coordinate f will then be calculated as:

    f = Cf_func(t, duration, *Cf_args)

    instead of:

    f = t / duration
    """
    if Cf is None:
        f = t / duration
    else:
        Cf_func = Cf[0]
        Cf_args = Cf[1:]
        f = Cf_func(t, duration, *Cf_args)
    f0 = (f + step + 2) / 4
    return Poly4Asymmetric(f0, None, A, B, C, 1, time_argument_is_f=True)


def Poly4Line(t, duration, step, A, B, C, Initial, Final, Cf=None):
    """Transfer coil function, standard two segment

    Cf, if not None, should be a list or tuple, the first element
    of which is a Cf function for scaling the time coordinate,
    and the other elements the arguments to be passed to it.
    The normalised time coordinate f will then be calculated as:

    f = Cf_func(t, duration, *Cf_args)

    instead of:

    f = t / duration
    """
    if Cf is None:
        f = t / duration
    else:
        Cf_func = Cf[0]
        Cf_args = Cf[1:]
        f = Cf_func(t, duration, *Cf_args)
    f0 = (f + step) / 2
    return Poly4Asymmetric(f0, None, A, B, C, 1, time_argument_is_f=True) + (1 - f0) * Initial + f0 * Final


def Poly4Asymmetric(t, duration, A, B, C, D, Cf=None, time_argument_is_f=False):
    """Transfer coil function, standard one segment

    Cf, if not None, should be a list or tuple, the first element
    of which is a Cf function for scaling the time coordinate,
    and the other elements the arguments to be passed to it.
    The normalised time coordinate f will then be calculated as:

    f = Cf_func(t, duration, *Cf_args)

    instead of:

    f = t / duration.

    if time_argument_is_f == True, then duration and Cf must be None.
    In this case the first argument, t, will be interpreted as an already
    scaled time coordinate:

    f = t
    """
    if not time_argument_is_f:
        if Cf is None:
            f = t / duration
        else:
            Cf_func = Cf[0]
            Cf_args = Cf[1:]
            f = Cf_func(t, duration, *Cf_args)
    else:
        if duration is not None or Cf is not None:
            raise TypeError('If time_argument_is_f == True, then t is interpreted as the already scaled '
                            'time coordinate, f. In this case duration and Cf are not used and must be None.')
        f = t
    return 4 * A * f * (1 - f) * exp(-(((f - 1 / 2) - C) ** 2 / B ** 2) ** abs(D))

# Functions that are designed for specifying velocities #
# given known current to position conversions #
# These still have to be divided into fractions 1,2,3 to denote center of coils
# In this version I will assume a uniform acceleration


def CoilTime(d, v1, v2):
    """Function to compute duration of line #
    Need to know distance between Nth and Nth+1 coil"""
    return 2 * d / (v1 + v2)

# In the current to position curves, position is expressed as a fraction f
# from 0 to 1 so take the actual fraction in the line and convert that to
# a positional fraction.


def Cf(t, duration, d, v1, v2):
    f = t / duration
    f0 = f * ((v2 - v1) * f + 2 * v1) / (v1 + v2)
    return f0


def Cf2(t, duration, d, v1, v2, f_max=1.0):
    """
    Function that retuns a smoothly accelerating or declarating curve with zero jerk at the
    start and stop in a fractional time interval from zero to f_max.  This implies that the velocities
    have only relative meaning.

    t: a time that runs from 0 to duration
    duration: duration of ramp
    d: unused
    v1: initial velocity (note that this is used in a dimesnionless way below)
    v2: final velicity
    f_max: max fraction to return.  Naturally 1 is default
        when this is used it is suggested that you reduce the stage time by the same
        fraction to match physical velocities.
    """
    f = t / duration
    f0 = (2 * v1 * f + (v2 - v1) * (2 * f ** 3 - f ** 4)) / (v1 + v2)
    return f0*f_max


def Cf2Back(t, duration, d, v1, v2, f_max=1.0):
    """
    Function that retuns a smoothly accelerating or declarating curve with zero jerk at the
    start and stop in a fractional time interval from zero to f_max.  This implies that the velocities
    have only relative meaning.

    t: a time that runs fromS 0 to duration
    duration: duration of ramp
    d: unused
    v1: initial velocity (note that this is used in a dimesnionless way below)
    v2: final velicity
    f_max: max fraction to return.  Naturally 1 is default
        when this is used it is suggested that you reduce the stage time by the same
        fraction to match physical velocities.
    """
    f = 1-(t/duration)
    f0 = (2 * v1 * f + (v2 - v1) * (2 * f ** 3 - f ** 4)) / (v1 + v2)
    return f0*f_max


def Cf4(t, duration, fm, v1, v2):
    f = t / duration
    f0 = where(f < fm,
              # If f < fm:
              (3 * fm * v1 * f + (-v1 + v2) * f ** 3) / (fm * (v1 + fm * v1 + 2 * v2 - fm * v2)),
              # Otherwise:
              ((fm ** 2 * (v1 - v2) + 3 * fm * v2 * f + f * (v2 * (-3 + f) * f - v1 * (3 - 3 * f + f ** 2))) /
              ((-1 + fm) * (v1 + fm * v1 + 2 * v2 - fm * v2))))
    return f0


def Cf5(t, duration, fm, v1, v2):
    f = t / duration
    fint = f / fm
    f0 = where(fint <= 1,
               # If fint <= 1:
               (2 * v1 * (fint) + (v2 - v1) * (2 * fint ** 3 - fint ** 4)) / 2,
               # Otherwise:
               (v1 + v2) / 2 + v2 * (fint - 1))
    return 2 * f0 * fm / (fm * v1 + (2 - fm) * v2)


def Cf5Back(t, duration, fm, v1, v2):
    f = 1-(t/duration)
    fint = f / fm
    f0 = where(fint <= 1,
               # If fint <= 1:
               (2 * v1 * (fint) + (v2 - v1) * (2 * fint ** 3 - fint ** 4)) / 2,
               # Otherwise:
               (v1 + v2) / 2 + v2 * (fint - 1))
    return 2 * f0 * fm / (fm * v1 + (2 - fm) * v2)

def Vmix(t, duration, Vhalf, rate, max, base):
    f = t / duration
    f0 = Vhalf - rate * log((max / (f - base)) - 1)
    # Clip negative or NaN to zero
    f0[(f0 < 0) | isnan(f0)] = 0
    return f0


def TrnSin(t, duration, T0, tconst, n):
    f = t / duration
    t0 = f * T0
    f0 = where((t0 <= n * tconst) | (t0 >= (n + 2) * tconst),
               # where the above is True:
               0,
               # Otherwise:
               (sin(pi * t0 / tconst / 2 + n * pi / 2)) ** 2)
    return f0

def SmoothAccelerationRamp(t, duration, initial, final):

    t = t / duration

    f0 = initial - t **3 * (10 - 15 * t + 6 * t **2) * (initial - final)

    return f0


def EvapRampOffsetLocal(t, duration, U_I, U_F, U_0, tau):
   """Creates an "O'Hara" evaporation ramp from U_I to U_F assuming a trap bottom at U_0 and
    a time-constant tau"""

   alpha = log( (U_I - U_0)/(U_F - U_0) ) / log(1 - duration/tau)

   return U_0 + (U_I - U_0) * (1 - t/tau)**(-alpha)


if __name__ == '__main__':
    # Run all functions with random inputs as a test:
    import types
    import inspect
    t = linspace(0, 1, 1000)
    import numpy as np
    ifts, widths = np.meshgrid(np.linspace(0, 70, 1000), np.linspace(0, 85, 1000))
    pcolormesh(ifts, widths, PolyHalf1(t, 1, step=1, A=ifts, B=widths, C=0, Cf=None), cmap='seismic')
    show()
    # for name in __all__:
        # function = globals()[name]
        # print 'testing', name
        # argspec = inspect.getargspec(function)
        # try:
            # n_args = len(argspec.args) - (len(argspec.defaults) if argspec.defaults is not None else 0)
        # except Exception:
            # import IPython
            # IPython.embed()
        # print n_args
        # y = function(t, *rand(n_args-1))
        # plot(t, y, label=function.__name__)
        # legend()
        # grid(True)
        # xlabel('t')
        # ylabel('y')
        # title('testing all the functions')
        # show()
        # clf()
