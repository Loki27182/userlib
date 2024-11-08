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
    red_AOM_DDS.setfreq(t,RedMotFreqI, units = 'MHz')

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

    if RedMOTOn:
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
#   Transfer
################################################################################
def ramp_down_blue(t):
    blue_MOT_power.ramp(t,TransferTime,BlueMOTPower,BlueMOTTransferPower,100000)
    MOT_field.ramp(t,TransferTime,BlueMOTField,BlueMOTCompressionField,100000,units='A')
    blue_MOT_RF_TTL.go_high(t+TransferTime)

    return TransferTime

def set_field(t):
    blue_MOT_power.constant(t+.0002,BlueMOTPower)
    MOT_field.constant(t+.0002,RedMOTField,units='A')

    return np.max([FieldExtinctionTime,.0002])

def red_MOT_narrow(t):
    red_MOT_power.ramp(t,RedMOTNarrowTime,RedMOTPower,RedMOTPowerFinal,100000)
    MOT_field.ramp(t,RedMOTNarrowTime,RedMOTField,RedMOTFieldFinal,100000,units='A')
    # Red MOT AOM 
    # red_AOM_DDS.setrampon(t, RedMotFreqI, RedMotFreqF, RedMOTNarrowTime*1000, units='MHz')
    # This seems necessary to make the DDS work properly. Need to look into this more
    # red_AOM_DDS.setfreq(t+RedMOTNarrowTime+.01,RedMotFreqF, units = 'MHz')
    return(RedMOTNarrowTime)

################################################################################
#   Imaging
################################################################################
def grasshopper_exposure(t,name):
    GrassHp_XZ.expose(t-.0001,'fluorescence',name, GHExposureTime)
    blue_MOT_RF_TTL.go_low(t)
    blue_MOT_RF_TTL.go_high(t+PulseDuration)

    return GHExposureTime


################################################################################
#   Get rid of atoms for reference shot
################################################################################
def reference_setup(t):
    red_MOT_RF_TTL.go_low(t)
    red_MOT_RF_TTL.go_high(t+GHDownTime)

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
t+=red_MOT_narrow(t)
t+=DelayBeforeImaging
current_lock_enable.go_low(t-FieldExtinctionTime)
t+=grasshopper_exposure(t,'atoms')
t+=reference_setup(t)
t+=grasshopper_exposure(t,'background')
t+=return_to_defaults(t)

stop(t)