# This script is intended to do a simple scan of the red beatnote frequency
# without using BLACS. Either disable the red beatnote device in the
# connection table, recompile and restart BLACS, or set things up to have 
# a MOT with BLACS and then turn it off, and monitor the MOT in NI-MAX while
# running this script. All it does is sweep the beatnote frequency over some
# range, and with some step size, both setable with input arguments. Start 
# and stop frequencies are required inputs, and the step size defaults to 6kHz
# if not provided.

import serial

