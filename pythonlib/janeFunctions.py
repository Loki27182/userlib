#####################################################################
#                                                                   #
# spinapi.py                                                        #
#                                                                   #
# Copyright 2013, Christopher Billington, Philip Starkey            #
#                                                                   #
# This file is part of the spinapi project                          #
# (see https://bitbucket.org/cbillington/spinapi )                  #
# and is licensed under the Simplified BSD License.                 #
# See the LICENSE.txt file in the root of the project               #
# for the full license.                                             #
#                                                                   #
#####################################################################

#import imp
from pynqcom.pynqcom import LINK
#from pynqcom import pynqcom
import logging
#import time
import numpy as np
from threading import Timer
from time import time
from datetime import datetime
from sipyco.pc_rpc import Client

SERVER_IP_ADDRESS = '192.168.2.22'
SERVER_PORT = 6750

# Minimum time between sending signals
DelayTime = 0.1
EnableDelay = False

# Whether or not to tell the spincore library to write debug logfiles.
# User can set to False before calling any spinapi functions to disable debugging.
debug = False

# Defines for different pb_instr instruction types
CONTINUE = 0
STOP = 1
LOOP = 2
END_LOOP = 3
JSR = 4
RTS = 5
BRANCH = 6
LONG_DELAY = 7
WAIT = 8
RTI = 9

# Defines for using different units of time
ns = 1.0
us = 1000.0
ms = 1000000.0
s  = 1000000000.0

# Defines for using different units of frequency
MHz = 1.0
kHz = .001
Hz = .000001

# Defines for start_programming
PULSE_PROGRAM  = 0
FREQ_REGS = 1
PHASE_REGS = 2

# Defines for enabling analog output
ANALOG_ON = 1
ANALOG_OFF = 0

# Defines for resetting the phase:
PHASE_RESET = 1
NO_PHASE_RESET = 0

def restartRemoteJane():
    global RemoteJane
    RemoteJane = Client(SERVER_IP_ADDRESS, SERVER_PORT, "RemoteJaneServer")
    RemoteJane.addr_range = 524288
    RemoteJane.program = [np.array(np.zeros([RemoteJane.addr_range//16,4]),dtype = np.uint32)]
    RemoteJane.current_addr = 0
    RemoteJane.current_bank = 0
    RemoteJane.max_banks = 250
    return 0

def janeCheck():
    if 'RemoteJane' not in globals():
        restartRemoteJane()

def pb_read_status():
    janeCheck()
    status = RemoteJane.send_status()
    status = np.frombuffer(status, dtype = np.uint8)
    return {"stopped":bool(int(status%2)),
            "reset":bool(int((status//2)%2)),
            "running":bool(int((status//4)%2)),
            "waiting":bool(int((status//8)%2))}

def pb_select_board(board_num):
    return 0

def pb_init():
    janeCheck()
    return 0

def pb_core_clock(clock_freq):
    janeCheck()
    return RemoteJane.write_clock_freq(clock_freq)

def pb_start_programming(device):
    return 0

def pb_inst_pbonly(flags, inst, inst_data, length):
    janeCheck()
    if isinstance(flags, str) or isinstance(flags, bytes):
        flags = int(flags[::-1],2)
    create_instruction(RemoteJane.program[RemoteJane.current_bank],RemoteJane.current_addr % (RemoteJane.addr_range//16),flags,inst,inst_data,length)
    RemoteJane.current_addr += 1
    if (RemoteJane.current_addr % (RemoteJane.addr_range//16) == 0):
        RemoteJane.program.append(np.array(np.zeros([RemoteJane.addr_range//16,4]),dtype = np.uint32))
        RemoteJane.current_bank += 1
    assert RemoteJane.current_bank < RemoteJane.max_banks, "Memory overflow"
    return 0

def pb_stop_programming():
    programData = np.concatenate(RemoteJane.program)
    programData = programData.reshape((programData.size,))
    RemoteJane.receive_program(programData)

def pb_start():
    RemoteJane.toggle_start()

def pb_stop():
    result = RemoteJane.reset_brd()
    if not (result == 0):
        raise RuntimeError("PYNQ was not reset.")
    return result

def pb_close():
    pass

def pb_reset():
    janeCheck()
    RemoteJane.program = [np.array(np.zeros([RemoteJane.addr_range//16,4]),dtype = np.uint32)]
    RemoteJane.current_addr = 0
    RemoteJane.current_bank = 0
    
def create_instruction(program,n,flags,opcode,data,time):
    flags = int(flags)

    flags_low=np.array(0xFFFFFFFF&flags,dtype=np.uint32)
    flags_hi=np.array(0xFFFFFFFF&(flags>>32),dtype=np.uint32)

    clock_rate = RemoteJane.read_clk_freq()

    new_time = int(time/1e3*clock_rate) - 1 #time is in ns

    if (new_time <= 0):
        raise RuntimeError(f"Time is too short. Time = {time}, new_time = {new_time}")

    logging.debug("n = {}, flags = {}, opcode = {}, data = {}, time = {}".format(n, flags, opcode, data, time))
    program[n][0] = new_time
    program[n][1] = ((0x000FFFFF & data) | ((0x0000000F & opcode)<<20) | ((0xFF & flags_low)<<24)).astype(np.uint32, casting = 'unsafe')
    program[n][2] = ((flags_low>>8) | ((0x00FFFFFF & flags_hi)<<24)).astype(np.uint32, casting = 'unsafe')
    program[n][3] = flags_hi>>8

