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

    # Set probe frequency
    probe_VCO.constant(t,ProbeVCOVoltage)

    # AOMs are on
    blue_MOT_RF_TTL.go_low(t)
    red_MOT_RF_TTL.go_high(t)
    probe_RF_TTL.go_high(t)
    MOT_2D_RF_TTL.go_low(t)

    # Set red MOT RF source to external VCO, and set voltage for red on resonance
    red_MOT_RF_select.go_high(t)
    red_MOT_VCO.constant(t, RedMOTNarrowFrequency, units = 'MHz')

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
    red_MOT_power.constant(t,RedMOTNarrowPower)

    # Turn on trim fields
    shim_X.constant(t,BlueMOTShimX, units = 'A')
    shim_Y.constant(t,BlueMOTShimY, units = 'A')
    shim_Z.constant(t,BlueMOTShimZ, units = 'A')

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

def ramp_blue_down(t):
    blue_MOT_power.ramp(t,BlueMOTRampDuration,BlueMOTPower,BlueMOTTransferPower,samplerate=100000)
    MOT_field.ramp(t,BlueMOTRampDuration,BlueMOTField,BlueMOTCompressionField, samplerate=100000,units='A')

    blue_MOT_RF_TTL.go_high(t+BlueMOTRampDuration)
    blue_MOT_shutter.go_low(t+BlueMOTRampDuration) 
    blue_MOT_power.constant(t+BlueMOTRampDuration,BlueMOTPower)
    blue_MOT_RF_TTL.go_low(t+BlueMOTRampDuration+.02)
    
    current_lock_enable.go_low(t+BlueMOTRampDuration)

    red_MOT_RF_TTL.go_low(t+BlueMOTRampDuration-.02)
    red_MOT_Int_Disable.go_high(t+BlueMOTRampDuration-.02)

    return BlueMOTRampDuration

def flash_red(t):
    if RedMOTOn:
        red_MOT_RF_TTL.go_high(t)
        red_MOT_Int_Disable.go_low(t)

        red_MOT_RF_TTL.go_low(t+RedMOTNarrowTime)
        red_MOT_Int_Disable.go_high(t+RedMOTNarrowTime)

    return RedMOTNarrowTime
    
################################################################################
#   Imaging
################################################################################
def grasshopper_exposure(t,name,exposure):
    GrassHp_XZ.expose(t-.0001,'absorption',name, GHExposureTime)
    if exposure:
        probe_RF_TTL.go_low(t-.02)
        probe_shutter.go_high(t-.02)
        probe_RF_TTL.go_high(t)
        probe_RF_TTL.go_low(t+PulseDuration)
        probe_shutter.go_low(t+PulseDuration)
        probe_RF_TTL.go_high(t+PulseDuration+.02)

    return GHExposureTime

################################################################################
#   Imaging
################################################################################
def return_to_defaults(t):
    t+=.01
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
    current_lock_enable.go_high(t)
    MOT_field.constant(t,BlueMOTField, units='A')

    blue_MOT_power.constant(t,BlueMOTPower)
    red_MOT_power.constant(t,RedMOTNarrowPower)

    return(.1)

################################################################################
#   Experiment Sequence
################################################################################

start()

t=0
t+=blow_away(t)
t+=initialize(t)
t+=load_blue_MOT(t)
t+=ramp_blue_down(t)
t+=DelayBeforeImaging
t+=flash_red(t)+.0001
t+=grasshopper_exposure(t,'atoms',True)
t+=GHDownTime
t+=grasshopper_exposure(t,'reference',True)
t+=GHDownTime
t+=grasshopper_exposure(t,'background',False)
t+=return_to_defaults(t)

stop(t)