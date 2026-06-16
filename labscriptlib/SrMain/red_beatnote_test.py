from labscript import start, stop, add_time_marker
from labscript_utils import import_or_reload
from labscriptlib.common.functions import *
import numpy as np
# Load connection table
import_or_reload('labscriptlib.SrMain.connection_table')

# Load all experimental sequence functions 
# (also defines constants, globals, and controls for proper highlighting )
from labscriptlib.SrMain.Subroutines.define_functions import initialize, field_off, load_blue_MOT, red_swap_MOT, red_narrow_MOT, red_light_off, dipole_trap, exposure
from labscriptlib.SrMain.Subroutines.define_functions import magnetometry_pulse, magnetometry_shim_ramp, AOMDelay, ShutterDelay, dumb_wait, sideband_blowaway, sideband_pulse, shelving_pulse

# Uncomment the line below to make highlighting work better, but recomment to actually run
#from labscriptlib.SrMain.Subroutines.define_constants import *

################################################################################
#   Experiment Sequence
################################################################################
# Let's do this!
start()

# Starting at time=DelayBeforeStart
# This might need to me slightly positive to avoid errors...we'll see when we try it! Hopefully can be zero
t = np.round(np.random.rand(1)/60,6)
add_time_marker(0, 'start_delay')
t = DelayBeforeStart

scope_trigger.go_low(t)

# Initialize things and blow away old atoms
add_time_marker(t, 'blow_away')
t += initialize(t)

red_sideband_shutter.go_high(t)
red_MOT_shutter.go_high(t)

sideband_dds.setfreq(t,85, units = 'MHz')
dc_offset = 80
phase = 0
angfreq = 2*np.pi*RedMOTDitherFrequency*1000
amplitude = RedMOTDitherFrequency*RedMOTDitherDepth/1000
duration = 2
red_MOT_VCO.sine(t, duration, amplitude, angfreq, phase, dc_offset, 500000,units='MHz')
#red_MOT_VCO.constant(t, 80, units = 'MHz')
t+=duration


# Initialize things to default, but don't blow away atoms (default on state)
t += initialize(t, blowaway = False)
t+= ShutterDelay

# All done!
stop(t)