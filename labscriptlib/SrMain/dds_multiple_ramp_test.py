from labscript import *

from labscript_utils import import_or_reload
from labscriptlib.common.functions import *
import numpy as np

#import_or_reload('labscriptlib.example_experiment.connectiontable')
import_or_reload('labscriptlib.SrMain.connection_table')


SRS_shutter_open_time=0
SRS_shutter_close_time=0



################################################################################
#   Get rid of any old atoms
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

    # Enable red MOT power intensity lock
    red_MOT_Int_Disable.go_high(t)

    # Set MOT powers
    blue_MOT_power.constant(t,BlueMOTPower)
    red_MOT_power.constant(t,RedMOTPower)

    # MOT shutters are open
    blue_MOT_shutter.go_high(t)
    red_MOT_shutter.go_high(t)

    # Probe shutter closed
    probe_shutter.go_low(t)

    # Repump shutters are open to blow away atoms
    repump_707_shutter.go_high(t)
    repump_679_shutter.go_high(t)

    # Set beatnote frequencies
    blue_BN_DDS.setfreq(t,BlueMOTBeatnote / 5, units = 'MHz')
    red_BN_DDS.setfreq(t,RedCoolingBeatnote/48, units = 'MHz')

    # Turn on MOT field
    current_lock_enable.go_high(t)
    MOT_field.constant(t,BlueMOTField, units='A')
    
    # Turn on trim fields
    shim_X.constant(t,BlueMOTShimX, units = 'A')
    shim_Y.constant(t,BlueMOTShimY, units = 'A')
    shim_Z.constant(t,BlueMOTShimZ, units = 'A')

    red_AOM_DDS.setfreq(t,80, units = 'MHz')

    red_inj_VCO.constant(t,0)
    
    return(.01)

def swap_ramp(t,dur,t_const_i,t_const_f,V_low_i,V_high_i,V_low_f,V_high_f,f_ramp):
    tau = t/dur
    dV_i = V_high_i - V_low_i
    dV_f = V_high_f - V_low_f

    dvdt = f_ramp*dV_i

    scale_factor = (dV_i - tau*(dV_i - dV_f))/dV_i
    offset = V_low_i + tau*(V_low_f - V_low_i)
    return scale_factor*np.mod(dvdt*t,dV_i) + offset

def run_ramps(t):
    t_const_i = .05
    t_const_f = .05
    dur = .2
    V_low_i = -1
    V_high_i = 2
    V_low_f = -.1
    V_high_f = .1
    f_swap = 20000
    red_inj_VCO.customramp(t,dur,swap_ramp,t_const_i,t_const_f,V_low_i,V_high_i,V_low_f,V_high_f,f_swap,samplerate=500000)
    
    return(dur)

start()
t=0
t+=initialize(t)
t+=run_ramps(t)
t+=initialize(t)
stop(t)