from labscript import *

from labscript_utils import import_or_reload
from labscriptlib.common.functions import *

import_or_reload('labscriptlib.SrMain.connection_table')
def set_defaults(t):
    scope_trigger.go_high(t)
    probe_VCO.constant(t,ProbeVCOVoltage)

    # AOMs are on
    blue_MOT_RF_TTL.go_low(t)
    red_MOT_RF_TTL.go_high(t)
    probe_RF_TTL.go_high(t)
    MOT_2D_RF_TTL.go_low(t)

    # Set red MOT RF source to internal VCO, and set voltage
    red_MOT_RF_select.go_high(t)
    red_MOT_VCO.constant(t, RedMOTNarrowFrequency, units = 'MHz')

    # Set blue MOT VCO frequency
    blue_MOT_VCO.constant(t,BlueFreqOffset, units = 'MHz')

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

    shim_X.constant(t,BlueMOTShimX, units = 'A')
    shim_Y.constant(t,BlueMOTShimY, units = 'A')
    shim_Z.constant(t,BlueMOTShimZ, units = 'A')

    gMOT_coil_TTL.go_low(t)

    scope_trigger.go_low(t+0.05)
    return t+0.1

start()
t = set_defaults(0)
gMOT_coil_TTL.go_high(t)
t += test_pulse_duration
gMOT_coil_TTL.go_low(t)
t += set_defaults(t)
stop(t)