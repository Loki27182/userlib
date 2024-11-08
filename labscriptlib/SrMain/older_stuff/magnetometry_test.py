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
def blow_away(t):
    # Start scope trigger low
    scope_trigger.go_low(t)

    # Set probe frequency (repurposing an old analog line from the grating MOT)
    gMOT_coil_current_b.constant(t,ProbeVCOVoltage)

    # AOMs are on
    blue_MOT_RF_TTL.go_low(t)
    red_MOT_RF_TTL.go_high(t)
    probe_RF_TTL.go_high(t)
    MOT_2D_RF_TTL.go_low(t)

    # Disable red MOT power intensity lock
    red_MOT_Int_Disable.go_high(t)

    # MOT shutters are closed
    blue_MOT_shutter.go_low(t)
    red_MOT_shutter.go_low(t)

    # Probe and repump shutters are open to blow away atoms
    probe_shutter.go_high(t)
    repump_707_shutter.go_high(t)
    repump_679_shutter.go_high(t)

    # Set beatnote frequencies
    blue_BN_DDS.setfreq(t,BlueMOTBeatnote / 5, units = 'MHz')
    red_BN_DDS.setfreq(t,RedCoolingBeatnote/48, units = 'MHz')
    red_AOM_DDS.setfreq(t,RedMotFreqF, units = 'MHz')

    # Turn off MOT field
    current_lock_enable.go_low(t)
    MOT_field.constant(t,0, units='A')

    return(.05)

################################################################################
#   Get things ready for loading
################################################################################
def initialize(t):
    # Close probe shutter
    probe_shutter.go_low(t)

    # Turn on MOT field
    current_lock_enable.go_high(t)
    MOT_field.ramp(t,0.04,0,BlueMOTField,1000, units='A')
    blue_MOT_power.constant(t,BlueMOTPower)
    red_MOT_power.constant(t,RedMOTPower)

    # Turn on trim fields
    shim_X.constant(t,BlueMOTShimX, units = 'A')
    shim_Y.constant(t,BlueMOTShimY, units = 'A')
    shim_Z.constant(t,BlueMOTShimZ, units = 'A')

    #if RedMOTOn:
    red_MOT_RF_TTL.go_low(t)
    red_MOT_shutter.go_high(t)
    red_MOT_RF_TTL.go_high(t+.02)
    red_MOT_Int_Disable.go_low(t+.02)
    
    return(.05)

################################################################################
#   Blue MOT load
################################################################################
def load_blue_MOT(t):
    # Open MOT shutters with light off
    blue_MOT_RF_TTL.go_high(t-.02)
    blue_MOT_shutter.go_high(t-.02) 
    blue_MOT_RF_TTL.go_low(t)

    # Turn 2D MOT off 
    MOT_2D_RF_TTL.go_high(t+BlueMOTLoadTime)

    return BlueMOTLoadTime+SourceShutoffTime

################################################################################
#   Blue ramp, shut off red light, and set field
################################################################################
def ramp_down_blue(t):
    blue_MOT_power.ramp(t,TransferTime,BlueMOTPower,BlueMOTTransferPower,100000)
    MOT_field.ramp(t,TransferTime,BlueMOTField,BlueMOTCompressionField,100000,units='A')
    blue_MOT_RF_TTL.go_high(t+TransferTime)
    blue_MOT_shutter.go_high(t+TransferTime) 
    blue_MOT_RF_TTL.go_low(t+TransferTime+.02)
    blue_MOT_power.constant(t+TransferTime+.021,BlueMOTPower)

    return TransferTime

def set_field(t):
    current_lock_enable.go_low(t)

    return np.max([FieldExtinctionTime,.0002])

def turn_red_off(t):
    red_MOT_Int_Disable.go_high(t)
    red_MOT_RF_TTL.go_high(t)

    return 0

def red_pulse(t):
    red_MOT_RF_TTL.go_low(t)
    red_MOT_Int_Disable.go_low(t)
    red_MOT_RF_TTL.go_high(t + RedPulseDuration)
    red_MOT_Int_Disable.go_high(t + RedPulseDuration)

    return RedPulseDuration

################################################################################
#   Imaging
################################################################################
def grasshopper_exposure(t,exp,name):
    if Absorption:
        # Turn probe AOM off and open shutter
        probe_shutter.go_high(t-.02)
        probe_RF_TTL.go_low(t-.02)

        if exp:
            # Probe pulse if this isn't a background shot
            probe_RF_TTL.go_high(t)
            probe_RF_TTL.go_low(t+PulseDuration)

        # Close shutter and turn AOM back on
        probe_shutter.go_low(t+PulseDuration)
        probe_RF_TTL.go_high(t+PulseDuration+.02)

        # Set up camera exposure
        GrassHp_XZ.expose(t-0.0001,'absorption',name, GHExposureTime+.0002)
    else:
        if exp:
            blue_MOT_RF_TTL.go_low(t)
            blue_MOT_RF_TTL.go_high(t+PulseDuration)

        GrassHp_XZ.expose(t-0.0001,'fluorescence',name, GHExposureTime+.0002)

    return GHExposureTime + 0.02


################################################################################
#   Get rid of atoms for reference shot
################################################################################
def reference_setup(t):
    red_MOT_RF_TTL.go_low(t)
    red_MOT_RF_TTL.go_high(t+GHDownTime)

    # Turn off MOT field to make sure we don't have atoms
    
    MOT_field.constant(t,0, units='A')
    

    return(GHDownTime)

################################################################################
#   Imaging
################################################################################
def return_to_defaults(t):
    # Turn MOT field back on
    current_lock_enable.go_high(t+0.01)
    MOT_field.ramp(t,0.09,0,BlueMOTField,10000, units='A')

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

    return(.1)

################################################################################
#   Experiment Sequence
################################################################################

start()

t=0
t+=blow_away(t)
t+=initialize(t)
t+=load_blue_MOT(t)
t+=ramp_down_blue(t)
t+=set_field(t)
turn_red_off(t-.001)
if RedMOTOn:
    t+=red_pulse(t)
t+=grasshopper_exposure(t,True,'atoms')
t+=reference_setup(t)
t+=grasshopper_exposure(t,True,'reference')
t+=GHDownTime
t+=grasshopper_exposure(t,False,'background')
t+=return_to_defaults(t)

stop(t)