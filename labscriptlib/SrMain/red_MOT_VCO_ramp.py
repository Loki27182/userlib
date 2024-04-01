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

    # Set probe frequency
    probe_VCO.constant(t,ProbeVCOVoltage)

    # AOMs are on
    blue_MOT_RF_TTL.go_low(t)
    red_MOT_RF_TTL.go_high(t)
    probe_RF_TTL.go_high(t)
    MOT_2D_RF_TTL.go_low(t)

    # Set red MOT RF source to internal VCO, and set voltage
    red_MOT_RF_select.go_low(t)
    red_MOT_VCO.constant(t, RedMOTRamp0L, units = 'MHz')

    # Set blue MOT VCO frequency
    blue_MOT_VCO.constant(t,BlueFreqOffset, units = 'MHz')

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
    #blue_BN_DDS.setfreq(t,BlueMOTBeatnote / 5, units = 'MHz')
    red_BN_DDS.setfreq(t,RedBeatnote/48, units = 'MHz')
    red_AOM_DDS.setfreq(t,RedMOTNarrowFrequency, units = 'MHz')

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
    red_MOT_power.constant(t,RedMOTRampPower0)

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
    blue_MOT_power.ramp(t,BlueMOTRampDuration,BlueMOTPower,BlueMOTTransferPower,100000)
    MOT_field.ramp(t,BlueMOTRampDuration,BlueMOTField,BlueMOTCompressionField,100000,units='A')
    blue_MOT_RF_TTL.go_high(t+BlueMOTRampDuration)

    return BlueMOTRampDuration

def set_field(t):
    blue_MOT_power.constant(t+.0001,BlueMOTPower)
    MOT_field.constant(t+.0001,RedMOTField,units='A')

    return .0002

def swap_ramp(t,dur,V_low_i,V_high_i,V_low_f,V_high_f,f_ramp):
    tau = t/dur
    dV_i = V_high_i - V_low_i
    dV_f = V_high_f - V_low_f

    dvdt = f_ramp*dV_i

    scale_factor = (dV_i - tau*(dV_i - dV_f))/dV_i
    offset = V_low_i + tau*(V_low_f - V_low_i)
    return scale_factor*np.mod(dvdt*t,dV_i) + offset

def ramp_down_red(t):
    red_MOT_power.ramp(t,RedMOTRampTime,RedMOTRampPower0,RedMOTRampPowerF,500000)
    #red_MOT_VCO.ramp(t,RedMOTRampTime,RedMOTRamp0L,RedMOTRampFH,500000,units='MHz')
    red_MOT_VCO.customramp(t,RedMOTRampTime,swap_ramp,RedMOTRamp0L,RedMOTRamp0H,RedMOTRampFL,RedMOTRampFH,RedMOTRampFreq,samplerate=500000,units='MHz')
    MOT_field.ramp(t,RedMOTRampTime,RedMOTField,RedMOTFieldFinal,500000,units='A')

    return(RedMOTRampTime)

def red_MOT_narrow(t):
    red_MOT_power.constant(t,RedMOTNarrowPower)
    red_MOT_RF_select.go_high(t)

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

    # Turn off MOT field to make sure we don't have atoms
    current_lock_enable.go_low(t)
    MOT_field.constant(t,0, units='A')
    

    return(GHDownTime)

################################################################################
#   Imaging
################################################################################
def return_to_defaults(t):
    t+=.01
    # Start scope trigger low
    scope_trigger.go_low(t)

    # Set probe frequency
    probe_VCO.constant(t,ProbeVCOVoltage)

    # AOMs are on
    blue_MOT_RF_TTL.go_low(t)
    red_MOT_RF_TTL.go_high(t)
    probe_RF_TTL.go_high(t)
    MOT_2D_RF_TTL.go_low(t)

    # Set red MOT RF source to internal VCO, and set voltage
    red_MOT_RF_select.go_low(t)
    red_MOT_VCO.constant(t, RedMOTNarrowFrequency, units = 'MHz')

    # Set blue MOT VCO frequency
    blue_MOT_VCO.constant(t,BlueFreqOffset, units = 'MHz')

    # Enable red MOT power intensity lock
    red_MOT_Int_Disable.go_low(t)

    # MOT shutters are open
    blue_MOT_shutter.go_high(t)
    red_MOT_shutter.go_high(t)

    # Repump shutters are open
    repump_707_shutter.go_high(t)
    repump_679_shutter.go_high(t)

    # Probe shutter is closed
    probe_shutter.go_low(t)

    # Set beatnote frequencies
    #blue_BN_DDS.setfreq(t,BlueMOTBeatnote / 5, units = 'MHz')
    red_BN_DDS.setfreq(t,RedBeatnote/48, units = 'MHz')
    red_AOM_DDS.setfreq(t,RedMOTNarrowFrequency, units = 'MHz')

    # Turn MOT field on
    current_lock_enable.go_low(t)
    MOT_field.constant(t,0, units='A')

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
t+=ramp_down_red(t)
t+=red_MOT_narrow(t)
t+=DelayBeforeImaging
t+=grasshopper_exposure(t,'atoms')
t+=reference_setup(t)
t+=grasshopper_exposure(t,'background')
t+=return_to_defaults(t)

stop(t)