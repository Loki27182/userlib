from labscript import start, stop, add_time_marker
from labscript_utils import import_or_reload
from labscriptlib.common.functions import *
import numpy as np
# Load connection table
import_or_reload('labscriptlib.SrMain.connection_table')

# Load all experimental sequence functions 
# (also defines constants, globals, and controls for proper highlighting )
from labscriptlib.SrMain.Subroutines.define_functions import initialize, field_off, load_blue_MOT, red_swap_MOT, red_narrow_MOT, red_light_off, dipole_trap, exposure, AOMDelay, ShutterDelay

# Uncomment the line below to make highlighting work better, but recomment to actually run
#from labscriptlib.SrMain.Subroutines.define_constants import *

################################################################################
#   Experiment Sequence
################################################################################
# Let's do this!
start()

# Starting at time=DelayBeforeStart
# This might need to me slightly positive to avoid errors...we'll see when we try it! Hopefully can be zero
add_time_marker(0, 'start_delay')
t = DelayBeforeStart

# Initialize things and blow away old atoms
add_time_marker(t, 'blow_away')
t += initialize(t)

## Load atoms into the blue MOT - includes ramp down if that is happening
## and also blue light turn-off
t += load_blue_MOT(t)
t_blue_off = t

## Make the red MOT if doing that
## Should think about starting SWAP prior to blue shutoff, but not now
if RedMOTOn:
    # SWAP MOT (which ramps down)
    t += red_swap_MOT(t)
    # Narrow MOT (skips if narrow MOT duration is set to 0)
    t += red_narrow_MOT(t)

## Turn red light off
## This needs to happen, even with just the blue MOT, since we are doing the gray MOT
red_light_off(t)
## Turn the field off
field_off(t)

## Set reference for earliest imaging if magnetometry is happening
t_mag = t + 2*AOMDelay
## Set reference time for imaging at end of MOT stages
t_red_off = t

if DipoleOn > 0:
    if DipoleTurnOnDelay < -DipoleHoldTime:
        raise Exception('Error: End of dipole trap must go past end of red MOT')
    # Adjust turn-on time
    t += DipoleTurnOnDelay
    # Ramp up, hold, then drop the dipole trap
    t += dipole_trap(t)
    t_dipole = t

# TOF
t += TimeOfFlight

# Set up imaging to happen offset from one of the reference times set earlier
# May be earlier or later than that time or the end of experiment, which should mostly be constant
if ImagingOffsetRef == 'red':
    t_im = t_red_off + ImagingOffset
elif ImagingOffsetRef == 'blue':
    t_im = t_blue_off + ImagingOffset
elif ImagingOffsetRef == 'dipole':
    t_im = t_dipole + ImagingOffset
else:
    raise Exception("Error: ImagingOffsetRef must be either 'red' or 'blue'")

# Not sure what happens if this time is during the blue MOT section, so force to this value if too early
if t_im < t_blue_off + 3*AOMDelay:
    t_im = t_blue_off + 3*AOMDelay
    
# If we are doing magnetometry, and the imaging is being requested before the red is turned off, raise an exception, since the magnetometry pulse
# will not yet have been properly set up - this should be changed so the setup happens in the exposure function
if MagnetometryPulse != 0 and  t_im < t_mag:
    raise Exception('Error: Magnetometry pulse cannot happen prior to red light turn-off plus 2 times the AOM turn on/off delay')
        
# Take an actual exposure, named atoms 
# (used whether or not this is absorption or fluorescence, and exposes whatever cameras are selected with global definitions)
t_im += exposure(t_im, 'atoms', True)

# Wait until the later of:
#  - the end of the TOF
#  - the end of the atoms exposure 
t = np.max((t, t_im))

# Add camera downtime
t += DownTime

if Absorption:
    # Take a reference image of the probe beam if this is an absorption image
    # This is an actual exposure, but the atoms will have had time to go out of frame...probably...
    t += exposure(t, 'reference', True)
    # Add camera downtime
    t += DownTime

# Take a background image, which is not an actual exposure. This is used for both absorption and fluorescence imaging
t += exposure(t,'background',False)

# Initialize things to default, but don't blow away atoms (default on state)
t += initialize(t, blowaway = False)
t+= ShutterDelay

# All done!
stop(t)