# Name all blacs controls and global for proper highlighting
from userlib.labscriptlib.SrMain.Subroutines.define_constants import *
import numpy as np

# Define some constants that we might want to make globals at some point
ShutterDelay = 0.01
AOMDelay = 0.0002
BlowawayDuration = 0.04

################################################################################
#   Setup
################################################################################
def initialize(t, blowaway = True):
    # Set analog values (ni_0)
    dipole_power.constant(t,DipoleLoadDepth)                                  # Set default dipole beam power to zero
    red_MOT_VCO.constant(t, RedLoadPumpFreq, units = 'MHz')     # Set red MOT light to pump frequency for gray MOT
    mot_field.constant(t,BlueMOTField, units='A')               # Set default MOT field
    shim_X.constant(t,BlueMOTShimX, units = 'A')                # Set default X trim
    shim_Y.constant(t,BlueMOTShimY, units = 'A')                # Set default Y trim
    shim_Z.constant(t,BlueMOTShimZ, units = 'A')                # Set default Z trim
    blue_MOT_power.constant(t,BlueMOTPower)                     # Set default blue MOT power
    red_MOT_power.constant(t,RedMOTRampPower0)                  # Set default red MOT power
    # Set analog values (ni_1)
    probe_VCO.constant(t,ProbeVCOVoltage)                       # Set default probe power
    unused_0.constant(t,0)                                      # Set unused channel so analog card doesn't do wierd things
    # Set normal digital values
    blue_MOT_RF_TTL.go_low(t)                                   # Turn on (low) blue MOT AOM driver
    source_RF_TTL.go_low(t)                                     # Turn on (low) 2D MOT AOM driver
    red_MOT_shutter.go_low(t)                                   # Open red MOT shutter (not currently actually hooked up)
    red_MOT_RF_TTL.go_high(t)                                   # Turn on red RF
    red_SRS_TTL.go_low(t)                                       # Not currently used(?)
    repump_707_shutter.go_high(t)                               # Open 707 repump shutter
    repump_679_RF_TTL.go_low(t)                                 # Turn on 679 repump AOM
    scope_trigger.go_low(t)                                     # Reset scope trigger
    probe_RF_TTL.go_high(t)                                     # Turn on probe AOM
    red_MOT_RF_select.go_low(t)                                 # Select VCO as LF AOM frequency source
    red_MOT_Int_Disable.go_low(t)                               # Enable red cooling intensity lock integrator
    red_aux_shutter.go_low(t)                                   # Close red aux beam shutter
    dipole_shutter.go_low(t)                                    # Close dipole shutter
    dipole_RF_TTL.go_high(t)                                    # Turn on RF so AOM stays warm
    # Set conditional digital values
    if blowaway:                                        # If initializing and blowing away (start of experiment)
        dt = BlowawayDuration                                # Set a duration for blowaway
        current_lock_enable.go_low(t)                           # Turn off MOT field
        current_lock_enable.go_high(t + dt)        # And back on
        probe_shutter.go_high(t)                                # Open probe shutter
        probe_shutter.go_low(t + dt)               # Then close it
        blue_MOT_shutter.go_low(t)                              # Close blue MOT shutter
    else:                                               # If initializing and loading (end of experiment)
        dt = 0                                                  # Set zero duration
        current_lock_enable.go_high(t)                          # Turn on MOT field
        probe_shutter.go_low(t)                                 # Close probe shutter
        blue_MOT_shutter.go_high(t)                             # Open blue MOT shutter
    # Set DDS frequencies
    blue_BN_DDS.setfreq(t,BlueMOTBeatnote / 5, units = 'MHz')   # Set blue beatnote frequency
    blue_broken_DDS.setfreq(t, 25, units = 'MHz')               # Set unused blue DDS source to some value
    red_BN_DDS.setfreq(t,RedBeatnote/48, units = 'MHz')         # Set red DDS frequency (not actually used, because it doesn't work for some reason)
    return(dt + ShutterDelay)

def field_off(t):
    # Turn the field off with analog and digital controls
    mot_field.constant(t,0,units='A')
    current_lock_enable.go_low(t)
    return 0

################################################################################
#   Blue MOT
################################################################################
def load_blue_MOT(t):
    # Open MOT shutters with light off
    blue_MOT_RF_TTL.go_high(t - ShutterDelay)
    blue_MOT_shutter.go_high(t - ShutterDelay) 
    blue_MOT_RF_TTL.go_low(t)
    dt = BlueMOTLoadTime
    if RampDownBlue:
        if BlueMOTRampDuration <= dt:
            t_ramp_start = dt - BlueMOTRampDuration
        else:
            raise Exception('Error: BlueMOTRampDuration must be less than or equal to BlueMOTLoadTime')
        
        blue_MOT_power.ramp(t_ramp_start,BlueMOTRampDuration,BlueMOTPower,BlueMOTTransferPower,100000)
        mot_field.ramp(t_ramp_start,BlueMOTRampDuration,BlueMOTField,BlueMOTCompressionField,100000,units='A')
    # Go to end of blue hold stage (usually short, if not 0)
    dt += BlueMOTHoldTime
    # Turn off blue MOT light
    blue_MOT_RF_TTL.go_high(t + dt)
    # Reset intensity setpoint after RF has turned off
    blue_MOT_power.constant(t + dt + AOMDelay, BlueMOTPower)
    # If this is an absorption image, close the blue shutter and turn the AOM back on to reset,
    # otherwise leave shutter open and RF off, since it will be pulsed back on later for imaging
    if Absorption:
        blue_MOT_shutter.go_low(t + BlueMOTHoldTime) 
        blue_MOT_RF_TTL.go_low(t + BlueMOTHoldTime + ShutterDelay)
    # Turn 2D MOT off when that should happen
    source_RF_TTL.go_high(t + dt - SourceShutoffTime - ShutterDelay)
    return dt

################################################################################
#   Red MOT
################################################################################
def swap_ramp(t,dur,V_low_i,V_high_i,V_low_f,V_high_f,f_ramp):
    # Ramped sawtooth function for SWAP MOT
    tau = t/dur
    dV_i = V_high_i - V_low_i
    dV_f = V_high_f - V_low_f
    dvdt = f_ramp*dV_i
    scale_factor = (dV_i - tau*(dV_i - dV_f))/dV_i
    offset = V_low_i + tau*(V_low_f - V_low_i)
    return scale_factor*np.mod(dvdt*t,dV_i) + offset

def red_swap_MOT(t):
    # Disable the intensity lock integrator in preparation for turning the light off to switch frequency (avoid windup)
    red_MOT_Int_Disable.go_high(t - 3*AOMDelay)
    # Turn off RF to red cooling AOM (LF)
    red_MOT_RF_TTL.go_low(t - 2*AOMDelay)
    # Change LF AOM frequency to starting point for SWAP
    red_MOT_VCO.constant(t - AOMDelay,RedMOTRamp0L,units='MHz')
    # Turn RF back on at requested time
    red_MOT_RF_TTL.go_high(t)
    # Turn intensity lock integrator back on
    red_MOT_Int_Disable.go_low(t + AOMDelay)
    # Power ramp down
    red_MOT_power.ramp(t, RedMOTRampTime, RedMOTRampPower0, RedMOTRampPowerF, 500000)
    # Ramped sawtooth frequency modulation
    red_MOT_VCO.customramp(t, RedMOTRampTime, swap_ramp, 
                           RedMOTRamp0L, RedMOTRamp0H, RedMOTRampFL, 
                           RedMOTRampFH, RedMOTRampFreq, 
                           samplerate=500000, units='MHz')
    # Ramp field
    mot_field.ramp(t, RedMOTRampTime, RedMOTField, RedMOTFieldFinal, 500000, units='A')
    return(RedMOTRampTime)

def red_narrow_MOT(t):
    # Only set the narrow MOT parameters if we're actually doing a narrow MOT
    if RedMOTNarrowTime > 0:
        # Set frequency
        red_MOT_VCO.constant(t, RedMOTNarrowFrequency, units='MHz')
        # Set power
        red_MOT_power.constant(t, RedMOTNarrowPower)
    return(RedMOTNarrowTime)

def red_light_off(t):
    # Turn red light off
    red_MOT_RF_TTL.go_low(t)
    if MagnetometryPulse == 0:
        # Close red shutter if not doing magnetometry
        red_MOT_shutter.go_low(t)
    else:
        # If doing magnetomety:
        # Set correct frequency for magnetometry pulse after light has turned off
        red_MOT_VCO.constant(t + AOMDelay, RedMOTNarrowFrequency + MagPulseDetuning, units = 'MHz')
        # Set intensity lock setpoint back up to high initial value (this will saturate the integrator)
        red_MOT_power.constant(t + AOMDelay, RedMOTRampPower0)
        # Disable integrator after it has saturated 
        # (this will result in a very intense magnetometry pulse - might want to fix that somehow)
        red_MOT_Int_Disable.go_high(t + 2*AOMDelay)
    # Pretending like this happens instantly - it doesn't
    # don't apply a magnetometry pulse sooner than 2*AOMDelay after this step
    # NOTE: this shoud be updated to do the mag setup in the exposure function
    return 0

################################################################################
#   Dipole!!!!!!!!!!!!!!!!!!!!!
################################################################################
def dipole_trap(t):
    # Start by lowering intensity setpoint so the integrator saturates toward 0,
    # naturally turning the RF power down to 0, so we don't need to switch it off separately
    # Leave plenty of time for the integrator to do its thing
    dipole_power.constant(t - DipoleRampDuration - 10*ShutterDelay, 0)  
    # Open the dipole shutter, but the power will be nominally 0
    # Leave plenty of time for the shutter to open
    dipole_shutter.go_high(t - DipoleRampDuration - 5*ShutterDelay)  
    # Ramp up the setpoint so that it is at full power at the requested time
    # The anti-windup feature of the SRS lockbox should make this smooth, but we should measure
    # NOTE: The input to the setpoint needs to have a 22nF cap put in parallel with the existing 1k reisitor 
    # NOTE: This will low pass at 8kHz (50kHz/(2pi)), which will work well for a 50kHz samplerate
    dipole_power.ramp(t - DipoleRampDuration, DipoleRampDuration, 0, DipoleLoadDepth, 50000)
    # Snap dipole trap off after holdtime
    dipole_RF_TTL.go_low(t + DipoleHoldTime)
    return DipoleRampDuration

################################################################################
#   Imaging
################################################################################
def exposure(t,name,exposure):
    # Set imtype constant
    if Absorption:
        imtype = 'absorption'
    else:
        imtype = 'fluorescence'
    # See what cameras we are using 
    # (use both to avoid errors when going back to manual, 
    # or just manually reset the cameras that have errors when necessary)
    cameras = ImagingCamera.split(',')
    # Pad exposure time
    ExposureTime = PulseDuration + ExposurePadding
    # Set up camera exposures with trigger advance added
    if 'XZ' in cameras:
        cam_xy.expose(t - TriggerAdvance, imtype, name, ExposureTime + 2*TriggerAdvance)
    if 'YZ' in cameras:
        cam_yz.expose(t - TriggerAdvance, imtype, name, ExposureTime + 2*TriggerAdvance)
    if exposure:    # If we are actually applying an imaging pulse...
        if Absorption:  # If it is an absorption image...
            # If we are applying a magnetometry pulse...
            if MagnetometryPulse>0:
                # Apply the pulse at the specified time, just prior to the probe pulse
                red_MOT_RF_TTL.go_high(t - MagnetometryPulse)
                red_MOT_RF_TTL.go_low(t)
            # Apply the probe pulse, with shutter/AOM combo, to expose
            probe_RF_TTL.go_low(t - ShutterDelay)
            probe_shutter.go_high(t - ShutterDelay)
            probe_RF_TTL.go_high(t)
            probe_RF_TTL.go_low(t + PulseDuration)
            probe_shutter.go_low(t + PulseDuration)
            probe_RF_TTL.go_high(t + PulseDuration + ShutterDelay)
        else:           # If this is a fluorescence image...
            # Pulse the cooling light on to expose
            blue_MOT_RF_TTL.go_low(t)
            blue_MOT_RF_TTL.go_high(t + PulseDuration)
    # If not applying an imaging pulse (background image), there is nothing to do but set the cameras up
    return ExposureTime + 2*TriggerAdvance
