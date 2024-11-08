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

    # Intensity Stabilization set points
    blue_MOT_power.constant(t, BlueMOTPower)
    red_MOT_power.constant(t, RedMOTPower)

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
    MOT_field.ramp(t,0.04,0,BlueMOTField,1000, units='A')

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
def turn_off_load(t):
    # Switch 2D MOT light off
    MOT_2D_RF_TTL.go_high(t)

    return TimeOfFlight-ThrowawayTime-GHExposureTime

################################################################################
#   Imaging
################################################################################
def grasshopper_exposure(t,name):
    GrassHp_XZ.expose(t,'fluorescence',name, GHExposureTime)

    return GHExposureTime

def drop_MOT(t):
    current_lock_enable.go_low(t)
    MOT_field.constant(t,0, units='A')

    return GHDownTime

################################################################################
#   Imaging
################################################################################
def return_to_defaults(t):
    # Turn MOT field back on
    current_lock_enable.go_high(t+0.01)
    MOT_field.ramp(t,0.09,0,BlueMOTField,1000, units='A')

    # Open MOT shutter
    blue_MOT_shutter.go_high(t)

    probe_shutter.go_low(t)

    # Turn 2D MOT back on
    MOT_2D_RF_TTL.go_low(t)

    # Intensity stabilization setpoints
    blue_MOT_power.constant(t, BlueMOTPower)
    red_MOT_power.constant(t, RedMOTPower)

    return(.1)

################################################################################
#   Experiment Sequence
################################################################################

start()

t=0

t+=blow_away(t)
t+=initialize(t)
t+=load_blue_MOT(t)

t+=turn_off_load(t)
t+=grasshopper_exposure(t,'throwaway')
t+=ThrowawayTime
t+=grasshopper_exposure(t,'atoms')
t+=drop_MOT(t)
t+=grasshopper_exposure(t,'background')

t+=return_to_defaults(t)

stop(t)