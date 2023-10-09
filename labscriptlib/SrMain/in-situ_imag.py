from labscript import *

from labscript_utils import import_or_reload
from labscriptlib.common.functions import *

#import_or_reload('labscriptlib.example_experiment.connectiontable')
import_or_reload('labscriptlib.SrMain.connection_table')


SRS_shutter_open_time=0
SRS_shutter_close_time=0

def initialize(t):

    #Blue
    #blue_MOT_shutter.go_high(t)
    blue_MOT_RF_TTL.go_high(t)
    MOT_2D_RF_TTL.go_high(t)

    blue_BN_DDS.setfreq(t,BlueMOTBeatnote / 5, units = 'MHz')
    blue_MOT_power.constant(t,BlueMOTPower)

    #Fields
    current_lock_enable.go_high(t)

    MOT_field.ramp(t,0.09,0,BlueMOTField,1000, units='A')
    shim_X.constant(t,BlueMOTShimX, units = 'A')
    shim_Y.constant(t,BlueMOTShimY, units = 'A')
    shim_Z.constant(t,BlueMOTShimZ, units = 'A')
    return(.1)
'''
    #Repumps
    repump_707_shutter.go_high(t)
    repump_679_shutter.go_high(t)
    repump_707_DDS.MultiFreq(t,[RepumpFreq1,RepumpAmp1,RepumpFreq2,
        RepumpAmp2,RepumpFreq3,RepumpAmp3,RepumpFreq4,RepumpAmp4,RepumpFreq5,
        RepumpAmp5,10,0,10,0,10,0],RepumpUsedFreqs,RepumpDelayTime)
'''


################################################################################
#   Blue MOT
################################################################################

def load_blue_MOT(t):
    #Load Blue MOT

    #Things that are on
    MOT_2D_RF_TTL.go_low(t)
    blue_MOT_RF_TTL.go_low(t)
    #blue_MOT_shutter.go_high(t-SRS_shutter_open_time)


    #shim_X.constant(t,BlueMOTShimX, units = 'A')
    #shim_Y.constant(t,BlueMOTShimY, units = 'A')
    #shim_Z.constant(t,BlueMOTShimZ, units = 'A')

    return BlueMOTLoadTime


################################################################################
#   Imaging
################################################################################
def time_of_flight(t):

    blue_MOT_RF_TTL.go_high(t)
    #blue_MOT_shutter.go_low(t-SRS_shutter_close_time)
    MOT_2D_RF_TTL.go_high(t)
    current_lock_enable.go_low(t)
    

    return TimeOfFlight


def grasshopper_fluorescence(t):

    #current_lock_enable.go_low(t)
    blue_MOT_RF_TTL.go_high(t)
    #blue_MOT_shutter.go_low(t)
    #repump_679_shutter.go_high(t-SRS_shutter_open_time)
    #repump_707_shutter.go_high(t-SRS_shutter_open_time)


    GrassHp_XZ.expose(t-0.00005,'fluorescence','atoms', GHExposureTime)
    return GHExposureTime + 0.02


def grasshopper_background(t):
    #flea_background
    GrassHp_XZ.expose(t-0.00005,'fluorescence','background', GHExposureTime)

    return GHExposureTime + 0.02


def return_to_defaults(t):
    #pulseblaster_0
    current_lock_enable.go_high(t+0.01)
    # IGBT_enable.go_high(t)
    #ni_0
    MOT_field.ramp(t,0.09,0,BlueMOTField,1000, units='A')
    shim_X.constant(t,BlueMOTShimX, units = 'A')
    shim_Y.constant(t,BlueMOTShimY, units = 'A')
    shim_Z.constant(t,BlueMOTShimZ, units = 'A')
    blue_MOT_power.constant(t,BlueMOTPower)
    #blue_MOT_shutter.go_high(t)
    blue_MOT_RF_TTL.go_low(t)
    MOT_2D_RF_TTL.go_low(t)
    #repump_707_shutter.go_high(t)
    #repump_679_shutter.go_high(t)
    #Blue BN Arduino
    blue_BN_DDS.setfreq(t,BlueMOTBeatnote / 5, units ='MHz')
    return(.1)

################################################################################
#   Experiment Sequence
################################################################################

start()

t=0

t+=initialize(t)

if _1BlueMOTOn:
    t+=load_blue_MOT(t)

if TimeOfFlightOn:
    t+=time_of_flight(t)


if GrasshopperImagingOn:
    t+=grasshopper_fluorescence(t)
    t+=GHDownTime
    t+=grasshopper_background(t)

t+=return_to_defaults(t)

stop(t)