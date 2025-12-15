from labscript import start, stop, add_time_marker
from labscript_utils import import_or_reload
from labscriptlib.common.functions import *
import numpy as np
# Load connection table
import_or_reload('labscriptlib.SrMain.connection_table')

# Load all experimental sequence functions 
# (also defines constants, globals, and controls for proper highlighting )
from labscriptlib.SrMain.Subroutines.define_functions import initialize, field_off, load_blue_MOT, red_swap_MOT, red_narrow_MOT, red_light_off, dipole_trap, exposure, magnetometry_pulse, magnetometry_shim_ramp, AOMDelay, ShutterDelay

# Uncomment the line below to make highlighting work better, but recomment to actually run
#from labscriptlib.SrMain.Subroutines.define_constants import *

################################################################################
#   Experiment Sequence
################################################################################
# Let's do this!
start()

t = DelayBeforeStart
dipole_shutter.go_high(t)
t += initialize(t,True)

scope_trigger.go_low(t)
dds_0.setfreq(t,20, units = 'MHz')
dds_1.setfreq(t,20, units = 'MHz')
t += 0.25

scope_trigger.go_high(t)
dds_0.setfreq(t,40, units = 'MHz')
dds_1.setfreq(t,40, units = 'MHz')
t += 0.25

scope_trigger.go_low(t)
dds_0.setfreq(t,20, units = 'MHz')
dds_1.setfreq(t,20, units = 'MHz')
t += 0.25

scope_trigger.go_high(t)
dds_0.setfreq(t,40, units = 'MHz')
dds_1.setfreq(t,40, units = 'MHz')
t += 0.25

scope_trigger.go_low(t)
t += 0.25

t += initialize(t,False)
t += 0.25
stop(t)