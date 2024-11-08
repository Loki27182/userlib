from labscript import *

from labscript_utils import import_or_reload
from labscriptlib.common.functions import *

#import_or_reload('labscriptlib.example_experiment.connectiontable')
import_or_reload('labscriptlib.SrMain.connection_table')


SRS_shutter_open_time=0
SRS_shutter_close_time=0

def blow_away(t):
    # Trigger scope at beginning of run
    scope_trigger.go_high(t)
    scope_trigger.go_low(t+.01)

    # AOMs are on
    blue_MOT_RF_TTL.go_low(t)
    probe_RF_TTL.go_high(t)
    MOT_2D_RF_TTL.go_low(t)

    # MOT shutter is closed
    blue_MOT_shutter.go_low(t)

    # Red MOT shutter is open
    red_MOT_shutter.go_high(t)

    # Probe and repump shutters are open to blow away atoms
    probe_shutter.go_high(t)
    repump_707_shutter.go_high(t)
    repump_679_shutter.go_high(t)

    # Set Blue frequency
    blue_BN_DDS.setfreq(t,BlueMOTBeatnote / 5, units = 'MHz')

    # Set REd cooling beatnote frequency
    red_BN_DDS.setfreq(t,RedCoolingBeatnote / 48, units = 'MHz')

    # Turn off MOT field
    current_lock_enable.go_low(t)
    MOT_field.constant(t,0, units='A')
    return(.05)

def initialize(t):
    # Close probe shutter
    probe_shutter.go_low(t)

    # Turn on MOT field
    current_lock_enable.go_high(t)
    MOT_field.ramp(t,0.04,0,BlueMOTField,1000, units='A')
    #blue_MOT_power.constant(t,ProbeDetuningVoltage)
    blue_MOT_power.constant(t,BlueMOTPower)

    # Turn on trim fields
    shim_X.constant(t,BlueMOTShimX, units = 'A')
    shim_Y.constant(t,BlueMOTShimY, units = 'A')
    shim_Z.constant(t,BlueMOTShimZ, units = 'A')
    return(.05)

################################################################################
#   Blue MOT
################################################################################
def load_blue_MOT(t):
    # Open MOT shutter with light off
    blue_MOT_RF_TTL.go_high(t-.02)
    blue_MOT_shutter.go_high(t-.02)

    # Turn light back on
    blue_MOT_RF_TTL.go_low(t)

    # Turn 2D MOT off 
    MOT_2D_RF_TTL.go_high(t+BlueMOTLoadTime-SourceShutoffTime)

    return BlueMOTLoadTime

def compress_blue_MOT(t):
    blue_MOT_power.ramp(t,BlueMOTCompressionTime,BlueMOTPower,BlueMOTTransferPower,1000)
    MOT_field.ramp(t,BlueMOTCompressionTime,BlueMOTField,BlueMOTCompressionField,1000, units='A')

    return BlueMOTCompressionTime

################################################################################
#   Red MOT
################################################################################

def transfer_to_red_MOT(t):
    blue_MOT_RF_TTL.go_high(t)
    MOT_field.constant(t,RedMOTField, units='A')

    if Absorption:
        blue_MOT_shutter.go_low(t)
        blue_MOT_RF_TTL.go_low(t+.02)

    return 0

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
        GrassHp_XZ.expose(t-0.00005,'absorption',name, GHExposureTime+.0001)
    else:
        if exp:
            blue_MOT_RF_TTL.go_low(t)
            blue_MOT_RF_TTL.go_high(t+PulseDuration)

        GrassHp_XZ.expose(t-0.00005,'fluorescence',name, GHExposureTime+.0001)

    return GHExposureTime + 0.02

################################################################################
#   Imaging
################################################################################
def return_to_defaults(t):
    # Turn MOT field back on
    current_lock_enable.go_high(t+0.01)
    MOT_field.ramp(t,0.01,0,BlueMOTField,1000, units='A')

    # Open MOT shutter
    blue_MOT_shutter.go_high(t)

    # Close probe shutter
    probe_shutter.go_low(t)
    # Turn on probe AOM
    probe_RF_TTL.go_high(t)

    # Turn 2D MOT back on
    MOT_2D_RF_TTL.go_low(t)
    blue_MOT_RF_TTL.go_low(t)

    return(.1)

################################################################################
#   Experiment Sequence
################################################################################

start()

t=0

t+=blow_away(t)
t+=initialize(t)
t+=load_blue_MOT(t)
t+=compress_blue_MOT(t)
t+=transfer_to_red_MOT(t)
t+=TimeOfFlight

t+=grasshopper_exposure(t,True,'atoms')
t+=GHDownTime
if Absorption:
    t+=grasshopper_exposure(t,True,'reference')
    t+=GHDownTime
t+=grasshopper_exposure(t,False,'background')

t+=return_to_defaults(t)

stop(t)