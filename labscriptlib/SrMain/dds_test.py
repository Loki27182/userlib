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
t = 0
t += initialize(t,False)
t += DelayBeforeStart

N = 100
T = 5

for ii in range(N):
    #add_time_marker(t, 'ii: {:0.0f}'.format(ii))
    clock_aux_dds.setfreq(t,79+2*ii/N, units = 'MHz')
    clock_atoms_dds.setfreq(t,79+2*ii/N, units = 'MHz')
    clock_cavity_dds.setfreq(t,79+2*ii/N, units = 'MHz')
    t += T/N/2
    #add_time_marker(t, 'ii2: {:0.0f}'.format(ii))
    clock_aux_dds.setfreq(t,(79 + 2/(2*N))+2*ii/N, units = 'MHz')
    clock_atoms_dds.setfreq(t,(79 + 2/(2*N))+2*ii/N, units = 'MHz')
    clock_cavity_dds.setfreq(t,(79 + 2/(2*N))+2*ii/N, units = 'MHz')
    t += T/N/2

#clock_aux_dds.setfreq(t,80, units = 'MHz')
#clock_atoms_dds.setfreq(t,80, units = 'MHz')
#clock_cavity_dds.setfreq(t,80, units = 'MHz')

t += .05
t += initialize(t,False)
t += 0.05
stop(t)