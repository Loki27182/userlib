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
def initialize(t):
    # Start scope trigger low
    scope_trigger.go_low(t)

    # Set probe frequency
    probe_VCO.constant(t,ProbeVCOVoltage)

    # AOMs are on
    blue_MOT_RF_TTL.go_low(t)
    red_MOT_RF_TTL.go_high(t)
    probe_RF_TTL.go_high(t)
    MOT_2D_RF_TTL.go_low(t)

    # Set red MOT RF source to internal VCO, and set voltage for red on resonance
    red_MOT_RF_select.go_low(t)
    red_MOT_VCO.constant(t, RedMOTNarrowFrequency, units = 'MHz')

    # Set blue MOT VCO frequency
    blue_MOT_VCO.constant(t,BlueFreqOffset, units = 'MHz')

    # Disable red MOT power intensity lock
    red_MOT_Int_Disable.go_low(t)

    # MOT shutters are closed
    blue_MOT_shutter.go_high(t)
    red_MOT_shutter.go_low(t)

    # Probe and repump shutters are open to blow away atoms
    probe_shutter.go_low(t)
    repump_707_shutter.go_high(t)
    repump_679_shutter.go_high(t)

    # Set beatnote frequencies
    #blue_BN_DDS.setfreq(t,BlueMOTBeatnote / 5, units = 'MHz')
    red_BN_DDS.setfreq(t,RedBeatnote/48, units = 'MHz')
    red_AOM_DDS.setfreq(t,RedMOTNarrowFrequency, units = 'MHz')

    # Turn off MOT field
    current_lock_enable.go_high(t)
    MOT_field.constant(t,BlueMOTField, units='A')

    blue_MOT_power.constant(t,BlueMOTPower)
    red_MOT_power.constant(t,RedMOTRampPower0)
    
    # Turn on trim fields
    shim_X.constant(t,BlueMOTShimX, units = 'A')
    shim_Y.constant(t,BlueMOTShimY, units = 'A')
    shim_Z.constant(t,BlueMOTShimZ, units = 'A')

    return(.05)

################################################################################
#   Imaging
################################################################################
def grasshopper_exposure(t,name):
    GrassHp_XZ.expose(t-.0001,'fluorescence',name, GHExposureTime)

    return GHExposureTime

################################################################################
#   Experiment Sequence
################################################################################

start()

t=0
t+=initialize(t)

xvalues = np.linspace(0,5,11)
yvalues = np.linspace(0,5,11)
for val_i in xvalues:
    shim_X.constant(t,val_i, units = 'A')
    for val_j in yvalues:
        shim_Y.constant(t,val_j, units = 'A')
        t+=GHDownTime
        t+=grasshopper_exposure(t,'atoms_shimX_{:1.3f}_shimY_{:1.3f}'.format(val_i,val_j))

t+=initialize(t)

stop(t)