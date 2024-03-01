from labscript import *

from labscript_utils import import_or_reload
from labscriptlib.common.functions import *

#import_or_reload('labscriptlib.example_experiment.connectiontable')
import_or_reload('labscriptlib.SrMain.connection_table')

################################################################################
#   Initialize
################################################################################
def initialize(t):
    # Start scope trigger low
    scope_trigger.go_low(t)

    # Set probe frequency (repurposing an old analog line from the grating MOT)
    gMOT_coil_current_b.constant(t,ProbeVCOVoltage)

    # AOMs are on
    blue_MOT_RF_TTL.go_low(t)
    red_MOT_RF_TTL.go_high(t)
    probe_RF_TTL.go_high(t)
    MOT_2D_RF_TTL.go_low(t)

    # Shutters are open
    blue_MOT_shutter.go_high(t)
    red_MOT_shutter.go_low(t)
    probe_shutter.go_low(t)
    repump_707_shutter.go_high(t)
    repump_679_shutter.go_high(t)

    # Set DDS frequencies
    blue_BN_DDS.setfreq(t,BlueMOTBeatnote / 5, units = 'MHz')
    red_BN_DDS.setfreq(t,RedCoolingBeatnote/48, units = 'MHz')
    red_AOM_DDS.setfreq(t,79.5, units = 'MHz')

    # MOT field on
    current_lock_enable.go_high(t)
    MOT_field.constant(t,BlueMOTField, units='A')

    # Set powers
    blue_MOT_power.constant(t,BlueMOTPower)
    red_MOT_power.constant(t,RedMOTPower)

    # Turn on trim fields
    shim_X.constant(t,BlueMOTShimX, units = 'A')
    shim_Y.constant(t,BlueMOTShimY, units = 'A')
    shim_Z.constant(t,BlueMOTShimZ, units = 'A')
    return(.05)

def sweep_red_freq(t):
    scope_trigger.go_high(t)

    red_AOM_DDS.setrampon( t, 79.5, 80, RedMOTSweepTime*1000, units='MHz')
    
    scope_trigger.go_low(t+RedMOTSweepTime)

    return(RedMOTSweepTime)

def cleanup(t):
    MOT_field.constant(t,BlueMOTField, units='A')
    gMOT_coil_current_b.constant(t,ProbeVCOVoltage)
    red_AOM_DDS.setfreq(t,80, units = 'MHz')

    return(0.05)

################################################################################
#   Experiment Sequence
################################################################################

start()

t = 0
t += initialize(t)
t += sweep_red_freq(t)
t += cleanup(t)

stop(t)