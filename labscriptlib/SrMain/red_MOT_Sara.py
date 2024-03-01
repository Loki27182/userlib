from labscript import *

from labscript_utils import import_or_reload
from labscriptlib.common.functions import *

#import_or_reload('labscriptlib.example_experiment.connectiontable')
import_or_reload('labscriptlib.SrMain.connection_table')

def blow_away(t):
    # AOMs are on
    blue_MOT_RF_TTL.go_low(t)
    red_MOT_RF_TTL.go_high(t)
    probe_RF_TTL.go_high(t)
    MOT_2D_RF_TTL.go_low(t)

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

    # Turn off MOT field
    current_lock_enable.go_low(t)
    MOT_field.constant(t,0, units='A')

    return(.05)

def return_to_defaults(t):
    # Turn MOT field back on
    current_lock_enable.go_high(t+0.01)
    MOT_field.ramp(t,0.09,0,BlueMOTField,1000, units='A')

    # Open blue MOT shutter
    blue_MOT_shutter.go_high(t)
    probe_shutter.go_low(t)
    # Turn 2D MOT back on
    MOT_2D_RF_TTL.go_low(t)
    blue_MOT_RF_TTL.go_low(t)
    # Intensity stabilization setpoints
    blue_MOT_power.constant(t, BlueMOTPower)
    red_MOT_power.constant(t, RedMOTPower)
    return(.5)

def initialize(t):
     # Close probe shutter
    probe_shutter.go_low(t)

    #setting beatnotes
    #red_BN_DDS.setfreq(t,RedCoolingBeatnote/48, units = 'MHz')
    #blue_BN_DDS.setfreq(t,BlueMOTBeatnote / 5, units = 'MHz')
    red_AOM_DDS.setfreq(t,RedMotFreqI, units = 'MHz')

    # Turn on MOT field
    current_lock_enable.go_high(t)
    MOT_field.ramp(t,0.04,0,BlueMOTField,1000, units='A')

    # AOMs are on
    blue_MOT_RF_TTL.go_low(t)
    probe_RF_TTL.go_high(t)
    MOT_2D_RF_TTL.go_low(t)
    red_MOT_RF_TTL.go_high(t)

    # Set powers
    blue_MOT_power.constant(t,BlueMOTPower)
    red_MOT_power.constant(t,RedMOTPower)

    # Turn on trim fields
    shim_X.constant(t,BlueMOTShimX, units = 'A')
    shim_Y.constant(t,BlueMOTShimY, units = 'A')
    shim_Z.constant(t,BlueMOTShimZ, units = 'A')
    return(.5)
################################################################################
#   Blue
################################################################################
def load_blue_MOT(t):
    # Open MOT shutter with light off
    blue_MOT_RF_TTL.go_high(t-.02)
    blue_MOT_shutter.go_high(t-.02)

    # Turn light back on
    blue_MOT_RF_TTL.go_low(t)

    return(BlueMOTLoadTime)    

################################################################################
#   Transfering from the blue to red
################################################################################
def ramp_down_blue(t):
    blue_MOT_power.ramp(t,TransferTime,BlueMOTPower,BlueMOTTransferPower,100000)
    #MOT_field.constant(t,3, units='A')
    MOT_field.ramp(t,TransferTime,BlueMOTField,BlueMOTCompressionField,100000,units='A')
    return TransferTime
def turn_off_blue(t):
    blue_MOT_RF_TTL.go_high(t)
    #blue_MOT_RF_TTL.go_low(t+0.02)
    #blue_MOT_shutter.go_low(t)
    MOT_2D_RF_TTL.go_high(t-.05)
    MOT_field.constant(t,RedMOTField, units='A')

    return(UnloadTime)

#loading red mot now. the light have been on so we only need to get the field to its final value
def red_MOT_narrow(t):
    MOT_field.ramp(t,RedMOTNarrowTime,RedMOTField,RedMOTFieldFinal,100000,units='A')
    #red_MOT_power.customramp(t, duration=RedMOTBroadTime, function=HalfGaussRamp, a=RedMOTBroadPowerI,
    #                         b=RedMOTBroadPowerF, width=250*10**(-3), samplerate=1000)
        #Narrow Frequency red MOT
    #scope_trigger.go_high(t)
    red_AOM_DDS.setrampon(t, RedMotFreqI, RedMotFreqF, RedMOTNarrowTime*1000, units='MHz')
    red_AOM_DDS.setfreq(t+RedMOTNarrowTime+.01,RedMotFreqF, units = 'MHz')
    #scope_trigger.go_low(t+RedMOTNarrowTime)
    return(RedMOTNarrowTime)



################################################################################
#   Imaging
################################################################################
def reference_setup(t):
    red_MOT_RF_TTL.go_low(t)
    red_MOT_RF_TTL.go_high(t+GHDownTime)

    # Turn off MOT field to make sure we don't have atoms
    current_lock_enable.go_low(t)
    MOT_field.constant(t,0, units='A')

    return(GHDownTime)

def grasshopper_exposure(t,name):
    GrassHp_XZ.expose(t-.0001,'fluorescence',name, GHExposureTime)
    #blue_MOT_RF_TTL.go_high(t-0.015)
    #probe_shutter.go_high(t-0.01)
    blue_MOT_RF_TTL.go_low(t)
    blue_MOT_RF_TTL.go_high(t+PulseDuration)
    #probe_shutter.go_high(t+PulseDuration+GHExposureTime)

    return(GHExposureTime)
################################################################################
#   Imaging
################################################################################

start()

t=0
t+=blow_away(t)
t+=initialize(t)
t+=load_blue_MOT(t)
t+=ramp_down_blue(t)
t+=turn_off_blue(t)
t+=red_MOT_narrow(t)
t+=grasshopper_exposure(t,'atoms')
t+=DelayBeforeImaging
t+=grasshopper_exposure(t,'background')
t+=return_to_defaults(t)

stop(t)