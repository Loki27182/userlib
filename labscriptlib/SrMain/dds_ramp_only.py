from labscript import start, stop, add_time_marker
from labscript_utils import import_or_reload
from labscriptlib.common.functions import *
import numpy as np
# Load connection table
import_or_reload('labscriptlib.SrMain.connection_table')

from labscriptlib.SrMain.Subroutines.define_functions import initialize, field_off, load_blue_MOT, red_swap_MOT, red_narrow_MOT, red_light_off, dipole_trap, exposure, magnetometry_pulse, magnetometry_shim_ramp, AOMDelay, ShutterDelay

start()
t = 0
t += initialize(t)
t += DDSRampDelay

dt = DDSRampDuration/DDSRampN
df = (DDSRampff-DDSRampf0)/DDSRampN
if DDSRampN > 512:
    raise RuntimeError('Too many DDS ramp points')
if dt < 2e-3:
    raise RuntimeError('DDS ramp time increment too small')
if DDSRampf0 < 1 or DDSRampf0 > 400:
    raise RuntimeError('DDS ramp start frequency out of range')
if DDSRampff < 1 or DDSRampff > 400:
    raise RuntimeError('DDS ramp stop frequency out of range')

for ii in range(0,DDSRampN+1):
    fi = np.clip(DDSRampf0+df*ii,1,400)
    dds_1.setfreq(t,fi, units = 'MHz')
    dds_2.setfreq(t,fi, units = 'MHz')
    #add_time_marker(t, '{fi:0.0f}'.format(fi=fi))
    t += dt

t += initialize(t, blowaway = False)
t+= ShutterDelay

stop(t)