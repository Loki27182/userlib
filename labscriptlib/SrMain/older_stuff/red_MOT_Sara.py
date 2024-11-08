from labscript import *

from labscript_utils import import_or_reload
from labscriptlib.common.functions import *

#import_or_reload('labscriptlib.example_experiment.connectiontable')
import_or_reload('labscriptlib.SrMain.connection_table')

def initialize(t):
    scope_trigger.go_low(t)
    # Set Trim currents
    shim_X.constant(t,BlueMOTShimX, units = 'A')
    shim_Y.constant(t,BlueMOTShimY, units = 'A')
    shim_Z.constant(t,BlueMOTShimZ, units = 'A')

    # Set up blue MOT light
    blue_MOT_RF_TTL.go_low(t)
    blue_MOT_shutter.go_low(t)
    blue_MOT_power.constant(t,BlueMOTPower)

    # Set up probe light
    probe_RF_TTL.go_high(t)
    probe_shutter.go_high(t)

    # Setup 2D MOT light
    MOT_2D_RF_TTL.go_low(t)

    # Turn red cooling light on and lock intensity
    red_MOT_shutter.go_high(t)
    red_MOT_Int_Disable.go_low(t)
    red_MOT_RF_TTL.go_high(t)
    red_MOT_power.constant(t,RedMOTPower)

    # Probe and repump shutters are open to blow away atoms
    repump_707_shutter.go_high(t)
    repump_679_shutter.go_high(t)

    # Set beatnote frequencies
    blue_BN_DDS.setfreq(t,BlueMOTBeatnote / 5, units = 'MHz')
    red_BN_DDS.setfreq(t,RedCoolingBeatnote/48, units = 'MHz')
    red_AOM_DDS.setfreq(t,RedMotFreqI, units = 'MHz')

    # Turn off MOT field
    current_lock_enable.go_low(t)
    MOT_field.constant(t,0, units='A')

    # Turn field on and close probe shutter after blow-away
    current_lock_enable.go_high(t+.025)
    MOT_field.ramp(t+.025,0.02,0,BlueMOTField,10000, units='A')
    probe_shutter.go_low(t+.025)

    return(.05)

################################################################################
#   Blue
################################################################################
def load_blue_MOT(t):
    scope_trigger.go_high(t)
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
    # Ramp the blue MOT power down while compressing
    blue_MOT_power.ramp(t,TransferTime,BlueMOTPower,BlueMOTTransferPower,100000)
    MOT_field.ramp(t,TransferTime,BlueMOTField,BlueMOTCompressionField,100000,units='A')

    # Shut off the 2D MOT light and the red cooling light a bit before end of ramp (disabling intensity lock integrator)
    MOT_2D_RF_TTL.go_high(t)
    red_MOT_Int_Disable.go_high(t)
    red_MOT_RF_TTL.go_low(t)

    return TransferTime

def turn_off_blue(t):
    # Snap off blue cooling light and snap field to initial red MOT value with all cooling light off
    #blue_MOT_RF_TTL.go_high(t)
    MOT_field.constant(t,RedMOTField, units='A')

    blue_MOT_power.constant(t,BlueMOTPower)

    return(0)

#loading red mot now. the light have been on so we only need to get the field to its final value
def red_MOT_narrow(t):

    # Snap red light on at initial value if red MOT is used
    if RedMOTOn:
        red_MOT_Int_Disable.go_low(t)
        red_MOT_RF_TTL.go_high(t)

    # Ramp field up and red cooling power down to final values
    MOT_field.ramp(t,RedMOTNarrowTime,RedMOTField,RedMOTFieldFinal,100000,units='A')
    red_AOM_DDS.setrampon(t, RedMotFreqI, RedMotFreqF, RedMOTNarrowTime*1000, units='MHz')
    red_MOT_power.ramp(t,RedMOTNarrowTime,RedMOTPower,RedMOTPowerFinal,100000)

    # This seems necessary to make the DDS work properly. Need to look into this more
    red_AOM_DDS.setfreq(t+RedMOTNarrowTime+.01,RedMotFreqF, units = 'MHz')

    # red_MOT_power.customramp(t, duration=RedMOTBroadTime, function=HalfGaussRamp, a=RedMOTBroadPowerI,
    #                          b=RedMOTBroadPowerF, width=250*10**(-3), samplerate=1000)

    return(RedMOTNarrowTime)

def red_MOT_off(t):
    # Turn field off
    MOT_field.constant(t,0,units='A')
    current_lock_enable.go_low(t)

    # Turn red light off, disable intensity lock integrator (if it was on)
    if RedMOTOn:
        red_MOT_Int_Disable.go_high(t)
        red_MOT_RF_TTL.go_low(t)

    scope_trigger.go_low(t)

    return(0)

################################################################################
#   Imaging
################################################################################
def grasshopper_exposure(t,name):
    GrassHp_XZ.expose(t-.0001,'fluorescence',name, GHExposureTime)
    #blue_MOT_RF_TTL.go_high(t-0.015)
    #probe_shutter.go_high(t-0.01)
    blue_MOT_RF_TTL.go_low(t)
    blue_MOT_RF_TTL.go_high(t+PulseDuration)
    #probe_shutter.go_high(t+PulseDuration+GHExposureTime)

    return(GHExposureTime)

################################################################################
#   End
################################################################################
def return_to_defaults(t):
    # Turn MOT field back on
    current_lock_enable.go_high(t+0.01)
    MOT_field.ramp(t,0.04,0,BlueMOTField,1000, units='A')

    # Open blue MOT shutter
    blue_MOT_shutter.go_high(t)
    probe_shutter.go_low(t)
    # Turn 2D MOT back on
    MOT_2D_RF_TTL.go_low(t)
    blue_MOT_RF_TTL.go_low(t)
    # Intensity stabilization setpoints
    blue_MOT_power.constant(t, BlueMOTPower)
    red_MOT_power.constant(t, RedMOTPower)

    red_MOT_Int_Disable.go_low(t)
    red_MOT_RF_TTL.go_high(t)
    
    scope_trigger.go_low(t)

    return(.05)


################################################################################
#   Actual sequence
################################################################################
start()

t=0
t+=initialize(t)
t+=load_blue_MOT(t)
t+=ramp_down_blue(t)
t+=turn_off_blue(t)
t+=UnloadTime
t+=red_MOT_narrow(t)
t+=UnloadTime
t+=red_MOT_off(t)
t+=DelayBeforeImaging
t+=grasshopper_exposure(t,'atoms')
t+=GHDownTime
t+=grasshopper_exposure(t,'background')
t+=return_to_defaults(t)

stop(t)