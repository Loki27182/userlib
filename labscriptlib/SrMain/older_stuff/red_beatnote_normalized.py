from labscript import *

from labscript_utils import import_or_reload
from labscriptlib.common.functions import *

#import_or_reload('labscriptlib.example_experiment.connectiontable')
import_or_reload('labscriptlib.SrMain.connection_table')


SRS_shutter_open_time=0
SRS_shutter_close_time=0


################################################################################
#   Get rid of any old atoms
################################################################################
def blow_away(t):
    # Start scope trigger low
    scope_trigger.go_low(t)

    # Set probe frequency (repurposing an old analog line from the grating MOT)
    gMOT_coil_current_b.constant(t,ProbeVCOVoltage)

    # AOMs are on
    blue_MOT_RF_TTL.go_low(t)
    probe_RF_TTL.go_high(t)
    MOT_2D_RF_TTL.go_low(t)

    # MOT shutters are closed
    blue_MOT_shutter.go_low(t)

    # Probe and repump shutters are open to blow away atoms
    probe_shutter.go_high(t)
    repump_707_shutter.go_high(t)
    repump_679_shutter.go_high(t)

    # Set beatnote frequencies
    blue_BN_DDS.setfreq(t,BlueMOTBeatnote / 5, units = 'MHz')
    red_BN_DDS.setfreq(t,RedCoolingBeatnote/48, units = 'MHz')

    # Turn off MOT field
    current_lock_enable.go_low(t)
    MOT_field.constant(t,0, units='A')
    red_AOM_DDS.setfreq(t, 80, units = 'MHz')

    # Turn red MOT light on and lock to anticipated level
    red_MOT_Int_Disable.go_low(t)
    red_AOM_DDS.setfreq(t, 80, units = 'MHz')
    red_MOT_power.constant(t,RedMOTPower)
    red_MOT_shutter.go_high(t)
    red_MOT_RF_TTL.go_high(t)

    return(.1)

################################################################################
#   Get things ready for loading
################################################################################
def initialize(t):
    # Close probe shutter
    probe_shutter.go_low(t)

    # Turn on MOT field
    current_lock_enable.go_high(t)
    MOT_field.ramp(t,0.005,0,BlueMOTField,10000, units='A')
    blue_MOT_power.constant(t,BlueMOTPower)

    # Turn on trim fields
    shim_X.constant(t,BlueMOTShimX, units = 'A')
    shim_Y.constant(t,BlueMOTShimY, units = 'A')
    shim_Z.constant(t,BlueMOTShimZ, units = 'A')

    # Lock integrator and turn red MOT light off with shutter
    red_MOT_Int_Disable.go_high(t)
    red_MOT_shutter.go_low(t)
    red_MOT_RF_TTL.go_low(t+.001)
    red_MOT_RF_TTL.go_high(t+.02)


    return(.01)

################################################################################
#   Blue MOT load
################################################################################
def load_blue_MOT(t):
    # Open MOT shutters with light off (only open red if this is a red MOT shot)
    blue_MOT_RF_TTL.go_high(t-.02)
    blue_MOT_shutter.go_high(t-.02) 

    blue_MOT_RF_TTL.go_low(t)

    # Turn 2D MOT off 
    # MOT_2D_RF_TTL.go_high(t+BlueMOTLoadTime-SourceShutoffTime)

    return BlueMOTLoadTime

################################################################################
#   Red MOT Stage
################################################################################
def red_MOT_On(t):
    red_MOT_RF_TTL.go_low(t-.02)
    red_MOT_shutter.go_high(t-.02)
    red_MOT_RF_TTL.go_high(t)
    red_MOT_Int_Disable.go_low(t+.000000)
    #red_MOT_power.ramp(t+.0001,0.0049,RedMOTMinPower,RedMOTPower,100000)
    return RedMOTDuration

def red_MOT_Off(t):
    red_MOT_RF_TTL.go_low(t)
    red_MOT_shutter.go_low(t)
    red_MOT_RF_TTL.go_high(t+.02)
    return RedMOTDuration

################################################################################
#   Imaging
################################################################################
def grasshopper_exposure(t,name):
    GrassHp_XZ.expose(t,'fluorescence_normalized',name, GHExposureTime)

    return GHExposureTime

################################################################################
#   Get rid of atoms for reference shot
################################################################################
def reference_setup(t):
    # AOMs are on
    blue_MOT_RF_TTL.go_low(t)
    red_MOT_RF_TTL.go_high(t)
    probe_RF_TTL.go_high(t)
    MOT_2D_RF_TTL.go_low(t)

    # Probe and repump shutters are closed to make sure we don't have atoms
    probe_shutter.go_low(t)
    repump_707_shutter.go_low(t)
    repump_679_shutter.go_low(t)

    if RedMOTOn:
        red_MOT_shutter.go_high(t)
    else:
        red_MOT_shutter.go_low(t)

    # Turn off MOT field to make sure we don't have atoms
    current_lock_enable.go_low(t)
    MOT_field.constant(t,0, units='A')

    return(GHDownTime)

################################################################################
#   Imaging
################################################################################
def return_to_defaults(t):
    # Turn MOT field back on
    current_lock_enable.go_high(t+0.01)
    MOT_field.ramp(t,0.09,0,BlueMOTField,1000, units='A')

    # Open MOT shutters
    blue_MOT_shutter.go_high(t)
    repump_679_shutter.go_high(t)
    repump_707_shutter.go_high(t)

    # Close probe shutter
    probe_shutter.go_low(t)
    # Turn on probe AOM
    probe_RF_TTL.go_high(t)

    # Turn 2D MOT back on
    MOT_2D_RF_TTL.go_low(t)
    blue_MOT_RF_TTL.go_low(t)

    gMOT_coil_current_b.constant(t,ProbeVCOVoltage)
    red_AOM_DDS.setfreq(t, 80, units = 'MHz')

    return(.1)

################################################################################
#   Experiment Sequence
################################################################################

start()

t=0
t+=blow_away(t)
t+=initialize(t)
t+=load_blue_MOT(t)
#scope_trigger.go_high(t-GHDownTime-1e-3)
grasshopper_exposure(t-GHDownTime,'reference')
#MOT_2D_RF_TTL.go_high(t-GHDownTime)
grasshopper_exposure(t+DelayBeforeImaging,'atoms')
scope_trigger.go_high(t)
t+=red_MOT_On(t)
scope_trigger.go_low(t)
t+=reference_setup(t)
t+=grasshopper_exposure(t,'background')
#scope_trigger.go_low(t+1e-3)
t+=return_to_defaults(t)

stop(t)