from labscript import *

from labscript_utils import import_or_reload
from labscriptlib.common.functions import *
import numpy as np

#import_or_reload('labscriptlib.example_experiment.connectiontable')
import_or_reload('labscriptlib.SrMain.connection_table')


SRS_shutter_open_time=0
SRS_shutter_close_time=0

if CompensateProbeDetuning>0:
    ProbeVCOVoltage = ProbeVCOVoltage - CompensateProbeDetuning*(.016-TimeOfFlight)/.016

################################################################################
#   Get rid of any old atoms
################################################################################
def blow_away(t):
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
    red_MOT_VCO.constant(t, RedLoadPumpFreq, units = 'MHz')
    #red_AOM_DDS.setfreq(t,RedMOTNarrowFrequency, units = 'MHz') 

    # Set blue MOT VCO frequency
    blue_sat_abs_AOM_offset.constant(t,SatAbsOffset)

    # Disable red MOT power intensity lock
    red_MOT_Int_Disable.go_high(t)

    # blue MOT shutter is open for the DelayBeforeStart time, then closed for the last 50ms for the actual blow away.
    blue_MOT_shutter.go_high(t)
    blue_MOT_shutter.go_low(t + DelayBeforeStart)
    red_MOT_shutter.go_low(t)

    # Probe and repump shutters are open to blow away atoms
    probe_shutter.go_high(t)
    repump_707_shutter.go_high(t)
    repump_679_RF_TTL.go_low(t)

    # Set beatnote frequencies
    blue_BN_DDS.setfreq(t,BlueMOTBeatnote / 5, units = 'MHz')
    red_BN_DDS.setfreq(t,RedBeatnote/48, units = 'MHz')
    #blue_broken_DDS.setfreq(t,25 , units = 'MHz')

    # Turn off MOT field
    current_lock_enable.go_low(t)
    MOT_field.constant(t,0, units='A')

    return(0.05 + DelayBeforeStart)

################################################################################
#   Get things ready for loading
################################################################################
def initialize(t):
    # Close probe shutter
    probe_shutter.go_low(t)

    # Turn on MOT field
    current_lock_enable.go_high(t)
    MOT_field.ramp(t,0.04,0,BlueMOTField,1000, units='A')
    blue_MOT_power.constant(t,BlueMOTPower)
    red_MOT_power.constant(t,RedMOTRampPower0)

    shim_X.constant(t,BlueMOTShimX, units = 'A')
    shim_Y.constant(t,BlueMOTShimY, units = 'A')
    shim_Z.constant(t,BlueMOTShimZ, units = 'A')

    # Open red MOT shutter if we're actually going to make a red MOT
    if RedMOTOn:
        red_MOT_shutter.go_high(t)
        red_MOT_Int_Disable.go_low(t)

    Red_kill_beam_shutter.go_low(t)
    if DipoleOn:
        DP_main_shutter.go_high(t)
    else:
        DP_main_shutter.go_low(t)
    
    return(0.05)

################################################################################
#   Blue MOT load
################################################################################
def load_blue_MOT(t):
    # Open MOT shutters with light off
    blue_MOT_RF_TTL.go_high(t-.02)
    blue_MOT_shutter.go_high(t-.02) 
    blue_MOT_RF_TTL.go_low(t)

    duration = BlueMOTLoadTime
    
    if RampDownBlue:
        if BlueMOTRampDuration <= BlueMOTLoadTime:
            duration -= BlueMOTRampDuration
        else:
            raise Exception('Error: BlueMOTRampDuration must be less than or equal to BlueMOTLoadTime')
    
    # Turn 2D MOT off 
    MOT_2D_RF_TTL.go_high(t + duration - SourceShutoffTime)

    return duration

################################################################################
#   Transfer
################################################################################
def ramp_down_blue(t):
    blue_MOT_power.ramp(t,BlueMOTRampDuration,BlueMOTPower,BlueMOTTransferPower,100000)
    MOT_field.ramp(t,BlueMOTRampDuration,BlueMOTField,BlueMOTCompressionField,100000,units='A')
    
    return BlueMOTRampDuration

def hold_blue(t):
    # Set red frequency to low end of beginning of SWAP ramp
    #if RedMOTOn:
    #    red_MOT_VCO.constant(t,RedMOTRamp0L,units='MHz')

    # Turn blue off
    blue_MOT_RF_TTL.go_high(t+BlueMOTHoldTime)
    blue_MOT_power.constant(t+BlueMOTHoldTime+.0001,BlueMOTPower)
    
    if Absorption:
        blue_MOT_shutter.go_low(t+BlueMOTHoldTime) 
        blue_MOT_RF_TTL.go_low(t+BlueMOTHoldTime+.02)

    return BlueMOTHoldTime

def blue_MOT_off(t):
    MOT_field.constant(t,0,units='A')
    current_lock_enable.go_low(t)
    

    return TimeOfFlight

def swap_ramp(t,dur,V_low_i,V_high_i,V_low_f,V_high_f,f_ramp):
    tau = t/dur
    dV_i = V_high_i - V_low_i
    dV_f = V_high_f - V_low_f

    dvdt = f_ramp*dV_i

    scale_factor = (dV_i - tau*(dV_i - dV_f))/dV_i
    offset = V_low_i + tau*(V_low_f - V_low_i)
    return scale_factor*np.mod(dvdt*t,dV_i) + offset

def ramp_down_red(t):
    red_MOT_Int_Disable.go_high(t-.0004)
    red_MOT_RF_TTL.go_low(t-.0003)
    red_MOT_VCO.constant(t-.0001,RedMOTRamp0L,units='MHz')
    red_MOT_RF_TTL.go_high(t)
    red_MOT_Int_Disable.go_low(t+.0001)

    red_MOT_power.ramp(t,RedMOTRampTime,RedMOTRampPower0,RedMOTRampPowerF,500000)
    red_MOT_VCO.customramp(t,RedMOTRampTime,swap_ramp,RedMOTRamp0L,RedMOTRamp0H,RedMOTRampFL,RedMOTRampFH,RedMOTRampFreq,samplerate=500000,units='MHz')
    MOT_field.ramp(t,RedMOTRampTime,RedMOTField,RedMOTFieldFinal,500000,units='A')

    return(RedMOTRampTime)

def red_MOT_narrow(t):
    red_MOT_VCO.constant(t,RedMOTNarrowFrequency,units='MHz')
    red_MOT_power.constant(t,RedMOTNarrowPower)

    return(RedMOTNarrowTime)

def red_MOT_off(t):
    red_MOT_RF_TTL.go_low(t)

    MOT_field.constant(t,0, units='A')
    current_lock_enable.go_low(t)

    if MagnetometryPulse == 0:
        red_MOT_shutter.go_low(t)
    else:
        red_MOT_VCO.constant(t+.0002,RedMOTNarrowFrequency+MagPulseDetuning,units='MHz')
        red_MOT_power.constant(t+.0002,RedMOTRampPower0)
        red_MOT_Int_Disable.go_high(t+.0003)

    return TimeOfFlight

################################################################################
#   Imaging
################################################################################
def grasshopper_exposure(t,name,exposure):

    if Absorption:
        imtype = 'absorption'
    else:
        imtype = 'fluorescence'

    cameras = ImagingCamera.split(',')
    ExposureTime = PulseDuration + ExposurePadding
    if 'XZ' in cameras:
        cam_gh_0.expose(t-TriggerAdvance,imtype,name, ExposureTime+2*TriggerAdvance)
    if 'YZ' in cameras:
        cam_bf_0.expose(t-TriggerAdvance,imtype,name, ExposureTime+2*TriggerAdvance)
    
    if exposure:
        if Absorption:
            if MagnetometryPulse>0:
                #red_MOT_RF_TTL.go_low(t-.02-MagnetometryPulse)
                #red_MOT_shutter.go_high(t-.02-MagnetometryPulse)
                red_MOT_RF_TTL.go_high(t-MagnetometryPulse)
                red_MOT_RF_TTL.go_low(t)
                #red_MOT_shutter.go_low(t+PulseDuration)
                #red_MOT_RF_TTL.go_high(t+PulseDuration+.02)
            probe_RF_TTL.go_low(t-.02)
            probe_shutter.go_high(t-.02)
            probe_RF_TTL.go_high(t)
            probe_RF_TTL.go_low(t+PulseDuration)
            probe_shutter.go_low(t+PulseDuration)
            probe_RF_TTL.go_high(t+PulseDuration+.02)
        else:
            #blue_MOT_RF_TTL.go_high(t-.02)
            #blue_MOT_shutter.go_high(t-.02)
            blue_MOT_RF_TTL.go_low(t)
            blue_MOT_RF_TTL.go_high(t+PulseDuration)

    return ExposureTime+2*TriggerAdvance

################################################################################
#   Resore defaults
################################################################################
def return_to_defaults(t):
    t+=.01
    scope_trigger.go_low(t)

    # Set probe frequency
    probe_VCO.constant(t,ProbeVCOVoltage)

    # AOMs are on
    blue_MOT_RF_TTL.go_low(t)
    red_MOT_RF_TTL.go_high(t)
    probe_RF_TTL.go_high(t)
    MOT_2D_RF_TTL.go_low(t)

    # Set red MOT RF source to internal VCO, and set voltage
    red_MOT_RF_select.go_low(t)
    red_MOT_VCO.constant(t, RedLoadPumpFreq, units = 'MHz')
    #red_AOM_DDS.setfreq(t,RedMOTNarrowFrequency, units = 'MHz')

    # Set blue sat abs AOM driver VCO offset voltage
    blue_sat_abs_AOM_offset.constant(t,SatAbsOffset)

    # Enable red MOT power intensity lock
    red_MOT_Int_Disable.go_low(t)

    # MOT shutters are open
    blue_MOT_shutter.go_high(t)
    red_MOT_shutter.go_high(t)

    # Repump shutters are open
    repump_707_shutter.go_high(t)
    repump_679_RF_TTL.go_low(t)

    # Probe shutter is closed
    probe_shutter.go_low(t)

    # Set beatnote frequencies
    blue_BN_DDS.setfreq(t,BlueMOTBeatnote / 5, units = 'MHz')
    red_BN_DDS.setfreq(t,RedBeatnote/48, units = 'MHz')
    #blue_broken_DDS.setfreq(t,25 , units = 'MHz')
    #red_AOM_DDS.setfreq(t,RedMOTNarrowFrequency, units = 'MHz')


    # Turn MOT field on
    current_lock_enable.go_high(t)
    MOT_field.constant(t,BlueMOTField, units='A')

    # closing the dipole shutter
    DP_main_shutter.go_low(t)

    return(.02)

################################################################################
#   Experiment Sequence
################################################################################

start()

t=0
t+=blow_away(t)
t+=initialize(t)
t+=load_blue_MOT(t)
if RampDownBlue:
    t+=ramp_down_blue(t)
t+=hold_blue(t)
if RedMOTOn:
    t+=ramp_down_red(t)
    t+=red_MOT_narrow(t)
    t_exp = t
    t+=red_MOT_off(t)
else:
    t_exp = t
    t+=blue_MOT_off(t)
t+=grasshopper_exposure(t,'atoms',True)
t+=DownTime
if Absorption:
    t+=grasshopper_exposure(t,'reference',True)
    t+=DownTime
t+=grasshopper_exposure(t,'background',False)
t+=DownTime
t+=return_to_defaults(t)


stop(t+.001)