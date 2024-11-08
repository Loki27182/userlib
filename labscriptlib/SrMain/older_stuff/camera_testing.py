from labscript import *

from labscript_utils import import_or_reload
from labscriptlib.common.functions import *

#import_or_reload('labscriptlib.example_experiment.connectiontable')
import_or_reload('labscriptlib.SrMain.connection_table')


SRS_shutter_open_time=0
SRS_shutter_close_time=0

def initialize(t):
    
    # Set constant values so they don't get changed in BLACS
    gMOT_coil_current_b.constant(t,ProbeVCOVoltage)
    blue_BN_DDS.setfreq(t,BlueMOTBeatnote / 5, units = 'MHz')
    current_lock_enable.go_high(t)
    MOT_field.constant(t,BlueMOTField, units='A')
    blue_MOT_power.constant(t,BlueMOTPower)
    shim_X.constant(t,BlueMOTShimX, units = 'A')
    shim_Y.constant(t,BlueMOTShimY, units = 'A')
    shim_Z.constant(t,BlueMOTShimZ, units = 'A')
    red_BN_DDS.setfreq(t,RedCoolingBeatnote/48, units = 'MHz')

    # Turn all AOMs on
    blue_MOT_RF_TTL.go_low(t)
    MOT_2D_RF_TTL.go_low(t)
    probe_RF_TTL.go_high(t)

    # Closed all shutters
    blue_MOT_shutter.go_low(t)
    red_MOT_shutter.go_low(t)
    probe_shutter.go_low(t)
    repump_707_shutter.go_low(t)
    repump_679_shutter.go_low(t)

    return(.15)

def get_image(t,imtype='bright'):
    trigger_delay = 1e-4
    shutter_delay = 5e-2
    AOM_delay = 5e-4

    # Turn off probe AOM in preparation for shutter to open
    probe_RF_TTL.go_low(t)
    t += AOM_delay

    # Open shutter
    probe_shutter.go_high(t)
    t += shutter_delay

    # Set up camera exposure
    GrassHp_XZ.expose(t,'images',imtype, GHExposureTime)
    t += trigger_delay

    # Pulse probe beam if this is a bright shot
    if imtype=='bright':
        probe_RF_TTL.go_high(t)

    t += PulseDuration

    if imtype=='bright':
        print(imtype)
        probe_RF_TTL.go_low(t)

    t += GHExposureTime - PulseDuration

    # Close probe shutter
    probe_shutter.go_low(t)
    t += shutter_delay

    # Turn AOM back on
    probe_RF_TTL.go_high(t)

    t += AOM_delay

    t += GHDownTime

    return t

start()

t = 0


# Set everything up
t += initialize(t)

t = get_image(t,'bright')

t = get_image(t,'dark')

t += initialize(t)

stop(t)