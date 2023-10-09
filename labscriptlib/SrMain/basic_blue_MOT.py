from labscript import *

from labscript_utils import import_or_reload
from labscriptlib.common.functions import *

#import_or_reload('labscriptlib.example_experiment.connectiontable')
import_or_reload('labscriptlib.SrMain.connection_table')


SRS_shutter_open_time=0
SRS_shutter_close_time=0

def blow_away(t):
    # AOMs are on
    blue_MOT_RF_TTL.go_low(t)
    probe_RF_TTL.go_low(t)
    MOT_2D_RF_TTL.go_low(t)

    # MOT shutter is closed
    blue_MOT_shutter.go_low(t)

    # Probe and repump shutters are open to blow away atoms
    probe_shutter.go_high(t)
    repump_707_shutter.go_high(t)
    repump_679_shutter.go_high(t)

    # Set Blue frequency
    blue_BN_DDS.setfreq(t,BlueMOTBeatnote / 5, units = 'MHz')

    # Turn off MOT field
    current_lock_enable.go_low(t)
    MOT_field.constant(t,0, units='A')
    return(.05)

def initialize(t):
    # Close probe shutter
    probe_shutter.go_low(t)

    # Turn on MOT field
    current_lock_enable.go_high(t)
    MOT_field.ramp(t,0.04,0,BlueMOTField,100, units='A')

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

    return BlueMOTLoadTime

################################################################################
#   TOF
################################################################################
def time_of_flight(t):
    # Switch MOT light off
    blue_MOT_RF_TTL.go_high(t)
    # Then close shutter and turn AOM back on if this is an absorption image
    if Absorption:
        blue_MOT_shutter.go_low(t)
        blue_MOT_RF_TTL.go_low(t+.02)

    # Turn 2D MOT off
    MOT_2D_RF_TTL.go_high(t-SourceShutoffTime)

    # Switch off MOT field
    current_lock_enable.go_low(t)
    
    return TimeOfFlight

################################################################################
#   Imaging
################################################################################
def grasshopper_exposure(t,exp,name):
    if Absorption:
        # Turn probe AOM off and open shutter
        probe_shutter.go_high(t-.02)
        probe_RF_TTL.go_high(t-.02)

        if exp:
            # Probe pulse if this isn't a background shot
            probe_RF_TTL.go_low(t)
            probe_RF_TTL.go_high(t+PulseDuration)

        # Close shutter and turn AOM back on
        probe_shutter.go_low(t+PulseDuration)
        probe_RF_TTL.go_low(t+PulseDuration+.02)

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
    MOT_field.ramp(t,0.09,0,BlueMOTField,100, units='A')

    # Open MOT shutter
    blue_MOT_shutter.go_high(t)

    probe_shutter.go_low(t)

    # Turn 2D MOT back on
    MOT_2D_RF_TTL.go_low(t)

    return(.1)

################################################################################
#   Experiment Sequence
################################################################################

start()

t=0

t+=blow_away(t)
t+=initialize(t)
t+=load_blue_MOT(t)

t+=time_of_flight(t)

t+=grasshopper_exposure(t,True,'atoms')
t+=GHDownTime
if Absorption:
    t+=grasshopper_exposure(t,True,'reference')
    t+=GHDownTime
t+=grasshopper_exposure(t,False,'background')

t+=return_to_defaults(t)

stop(t)