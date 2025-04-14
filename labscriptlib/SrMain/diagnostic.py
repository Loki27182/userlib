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
def init(t=0,expose=False,T=0.0004,dt=0.0002,is_on=IsOn,name='init'):
    # Reset trigger line
    scope_trigger.go_high(t)

    # Slight delay so things aren't happenint at t=0
    dt = np.max(np.array((dt,0.0002)))
    t0 = t + dt
    T = np.max(np.array((T,2*dt)))

    # Set frequencies
    probe_VCO.constant(t0,ProbeVCOVoltage)
    red_MOT_VCO.constant(t0, RedLoadPumpFreq, units = 'MHz')
    blue_sat_abs_AOM_offset.constant(t0,SatAbsOffset)
    blue_BN_DDS.setfreq(t0,BlueMOTBeatnote / 5, units = 'MHz')
    red_BN_DDS.setfreq(t0,RedBeatnote/48, units = 'MHz')
    red_MOT_RF_select.go_low(t0)

    # Turn AOMs on
    blue_MOT_RF_TTL.go_low(t0)
    red_MOT_RF_TTL.go_high(t0)
    probe_RF_TTL.go_high(t0)
    MOT_2D_RF_TTL.go_low(t0)

    # Set beam powers
    blue_MOT_power.constant(t0,BlueMOTPower)
    red_MOT_power.constant(t0,RedMOTRampPower0)

    # Enable red MOT power intensity lock
    red_MOT_Int_Disable.go_low(t0)

    # Close probe, dipole, and kill beam shutters
    probe_shutter.go_low(t0)
    DP_main_shutter.go_low(t0)
    Red_kill_beam_shutter.go_low(t0)

    # Set MOT coil current
    MOT_field.constant(t0,BlueMOTField, units='A')
    if is_on:
        current_lock_enable.go_high(t0)
        # Open MOT and repump shutters
        blue_MOT_shutter.go_high(t0)
        repump_707_shutter.go_high(t0)
        repump_679_shutter.go_high(t0)
        red_MOT_shutter.go_high(t0)
    else:
        current_lock_enable.go_low(t0)
        # ...or don't!
        blue_MOT_shutter.go_low(t0)
        repump_707_shutter.go_low(t0)
        repump_679_shutter.go_low(t0)
        red_MOT_shutter.go_low(t0)

    # Set trim fields
    shim_X.constant(t0,BlueMOTShimX, units = 'A')
    shim_Y.constant(t0,BlueMOTShimY, units = 'A')
    shim_Z.constant(t0,BlueMOTShimZ, units = 'A')

    # Expose each camera if we want to
    if expose:
        cam_gh_0.expose(t0,'diagnostic',name, T-dt)
        cam_bf_0.expose(t0,'diagnostic',name, T-dt)
        #cam_fl_0.expose(t0,'diagnostic',name, T-dt)

    # Add a scope trigger during the exposure, whether or not there actually was an exposure
    #scope_trigger.go_low(t0)
    #scope_trigger.go_high(t0+(T-dt))

    return(T)


start()

t = init(T=.01)

t += 0.1
scope_trigger.go_low(t)
blue_MOT_shutter.go_low(t)
t_edge = t
t += 0.01
scope_trigger.go_high(t)
blue_MOT_shutter.go_high(t)
t += 0.1

cam_gh_0.expose(t_edge+ShutterDelay,'diagnostic','im_0', GHExposureTime)
cam_bf_0.expose(t_edge+ShutterDelay,'diagnostic','im_0', GHExposureTime)
#cam_fl_0.expose(t_edge+ShutterDelay,'diagnostic','im_0', GHExposureTime)

stop(t)