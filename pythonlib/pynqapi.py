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

#SERVER_IP_ADDRESS = '192.168.2.22' # Old Jane
SERVER_IP_ADDRESS = '192.168.2.32' # New (evil) Jane
SERVER_PORT = 6750

#LINK = imp.load_source('LINK', './pynqcom/pynqcom.py')


# Levels of log CRITICAL ERROR WARNING INFO DEBUG NOTSET

#logging.basicConfig(level = logging.DEBUG)
#log_name = 'BLACS.%s_%s.worker'%("pynqapi","pynqapi") # Jeff's debugging code
#pynqapilogger = logging.getLogger(log_name) # Jeff's debugging code

def _check():
    global _pynqcom
    try:
        _pynqcom
    except NameError:
        #logging.debug("Creating _pynqcom")
        #pynqapilogger.debug('Creating _pynqcom')
        _pynqcom = LINK(server_ip_address = SERVER_IP_ADDRESS, server_port = SERVER_PORT)
        _pynqcom.addr_range = 524288
        _pynqcom.program = [np.array(np.zeros([_pynqcom.addr_range//16,4]),dtype = np.uint32)]
        _pynqcom.current_addr = 0
        _pynqcom.current_bank = 0
        _pynqcom.max_banks = 250
        #_pynqcom.timer = Timer(2, watchdog)
        #_pynqcom.timer.start()
        _pynqcom.lastSignalTime = time() # Jeff's debugging code

# Minimum time between sending signals
DelayTime = 0.15
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

#def watchdog():
#    min_wait(DelayTime)
#    _pynqcom.send_string("watchdog()")
#    _pynqcom.timer = Timer(2, watchdog)
#    _pynqcom.lastWatchdogTime = time()
#    _pynqcom.timer.start()
#
#def restart_watchdog():
#    _pynqcom.timer = Timer(2, watchdog)
#    _pynqcom.timer.start()
#
#def stop_watchdog():
#    _pynqcom.timer.cancel()

#def watchdog2():
#    pynqapilogger.debug('Watchdog2 triggered') # Jeff's debugging code
#    _pynqcom.send_string("send_status()")
#    _pynqcom.timer.start()

def min_wait(dt):
    if EnableDelay:
        while time() - _pynqcom.lastSignalTime < dt:
            pass
        _pynqcom.lastSignalTime = time()


def pb_read_status():
    '''
    returns a dictionary of booleans with keys "stopped", "reset", "running", "waiting"

    _checkloaded()
    _spinapi.pb_read_status.restype = ctypes.c_uint32
    status = _spinapi.pb_read_status()

    # convert to reversed binary string
    # convert to binary string, and remove 0b
    status = bin(status)[2:]
    # reverse string
    status = status[::-1]
    # pad to make sure we have enough bits!
    status = status + "0000"

    return {"stopped":bool(int(status[0])),"reset":bool(int(status[1])),"running":bool(int(status[2])), "waiting":bool(int(status[3]))}
    '''

    #stop_watchdog()
    _check()
    min_wait(DelayTime) 
    _pynqcom.send_string("send_status()")
    #pynqapilogger.debug('Sent "send_status()"') # Jeff's debugging code
    #_pynqcom.timer = Timer(1, watchdog2)
    #pynqapilogger.debug('Starting watchdog2 timer') # Jeff's debugging code
    #_pynqcom.timer.start()
    #pynqapilogger.debug('Waiting for data') # Jeff's debugging code
    status = _pynqcom.read_all_data(1)
    #pynqapilogger.debug('Data read') # Jeff's debugging code
    #pynqapilogger.debug('Stopping watchdog2 timer') # Jeff's debugging code
    #_pynqcom.timer.cancel()
    status = np.frombuffer(status, dtype = np.uint8)
    #restart_watchdog()
    #status = [int(status)]
    # Convert to binary string representation, remove 0b
    #status = bin(status)[2:]
    # Reverse string
    #status = status[::-1]
    # Append "0000" to string so that it will have at least 4 elements
    #status = status + "0000"
    
    #pynqapilogger.debug('Returning results') # Jeff's debugging code
    return {"stopped":bool(int(status%2)),
            "reset":bool(int((status//2)%2)),
            "running":bool(int((status//4)%2)),
            "waiting":bool(int((status//8)%2))}
    #        "waiting":bool(int((status//8)%2))}

def pb_select_board(board_num):
    '''
    _checkloaded()
    _spinapi.pb_select_board.restype = ctypes.c_int
    result = _spinapi.pb_select_board(ctypes.c_int(board_num))
    if result < 0: raise RuntimeError(pb_get_error())
    return result
    '''
    # Function is unnecessary since we only have one board, but kept it just in case

    return 0

def pb_init():
    '''
    _checkloaded()
    _spinapi.pb_init.restype = ctypes.c_int
    result = _spinapi.pb_init()
    if result != 0: raise RuntimeError(pb_get_error())
    return result
    '''

    # Initializes board selected from pb_select_board

    return 0

def pb_core_clock(clock_freq):
    '''_checkloaded()
    _spinapi.pb_core_clock.restype = ctypes.c_void_p
    _spinapi.pb_core_clock(ctypes.c_double(clock_freq)) # returns void, so ignore return value.
    '''
    # Reads clock speed of PYNQ board and passes on to driver, does not set the speed

    _check()
    #stop_watchdog()
    min_wait(DelayTime) 
    #pynqapilogger.debug('Sending clock set command')
    _pynqcom.send_string("read_clk_freq()")
    min_wait(DelayTime) 
    data = np.array(clock_freq, dtype = np.float64)
    #pynqapilogger.debug('Sending clock rate: {:f}'.format(data))
    _pynqcom.connection.sendall(data)
    #pynqapilogger.debug('Reading clock rate')
    buff = _pynqcom.read_all_data(8)
    return_val = np.frombuffer(buff,dtype = np.float64)
    _pynqcom.frequency  = return_val*3/2
    #pynqapilogger.debug('Clock rate read')
    #pynqapilogger.debug('Saving clock rate')
    #pynqapilogger.debug('Jane says frequency is {:f}'.format(np.float64(return_val)))
    #print('Jane says frequency is {:f}'.format(np.float64(return_val)))
    #_pynqcom.frequency = np.frombuffer(buff,dtype = np.float64)
    #restart_watchdog()
    return _pynqcom.frequency

def pb_start_programming(device):
    '''_checkloaded()
    _spinapi.pb_start_programming.restype = ctypes.c_int
    result = _spinapi.pb_start_programming(ctypes.c_int(device))
    if result != 0: raise RuntimeError(pb_get_error())
    return result
    '''

    _check()
    return 0


def pb_select_dds(dds): # only for PulseBlaster.py
    '''
    _checkloaded()
    _spinapi.pb_select_dds.restype = ctypes.c_int
    result = _spinapi.pb_select_dds(ctypes.c_int(dds))
    if result < 0: raise RuntimeError(pb_get_error())
    return result
    '''
    return 0

def pb_set_phase(phase): # possible DDS extension
    '''_spinapi.pb_set_phase.restype = ctypes.c_int
    result = _spinapi.pb_set_phase(ctypes.c_double(phase))
    if result < 0: raise RuntimeError(pb_get_error())
    return result
    '''
    #stop_watchdog()
    _check()
    # _pynqcom.send_string('print("Received phase {}")'.format(phase))
    #restart_watchdog()
    return 0


def pb_set_freq(freq): # possible DDS extension
    '''_checkloaded()
    _spinapi.pb_set_freq.restype = ctypes.c_int
    result = _spinapi.pb_set_freq(ctypes.c_double(freq))
    if result < 0: raise RuntimeError(pb_get_error())
    return result
    '''
    #stop_watchdog()
    _check()
    # _pynqcom.send_string('print("Received freq {}")'.format(freq))
    #restart_watchdog()
    return 0

def pb_set_amp(amp, register): # possible DDS extension
    '''
    _checkloaded()
    _spinapi.pb_set_amp.restype = ctypes.c_int
    result = _spinapi.pb_set_amp(ctypes.c_float(amp),ctypes.c_int(register))
    if result < 0: raise RuntimeError(pb_get_error())
    return result
    '''
    #stop_watchdog()
    _check()
    # _pynqcom.send_string('print("Received amplitude {} to register {}")'.format(amp, register))
    #restart_watchdog()
    return 0


def pb_inst_pbonly(flags, inst, inst_data, length):
    '''
    _checkloaded()
    _spinapi.pb_inst_pbonly.restype = ctypes.c_int
    if isinstance(flags, str) or isinstance(flags, bytes):
        flags = int(flags[::-1],2)
    result = _spinapi.pb_inst_pbonly(ctypes.c_uint32(flags), ctypes.c_int(inst),
                                     ctypes.c_int(inst_data),ctypes.c_double(length))
    if result < 0: raise RuntimeError(pb_get_error())
    return result
    '''
    #pb_dtype = [('flags',np.int32), ('inst',np.int32),
    #                ('inst_data',np.int32), ('length',np.float64)]
    # _check()


#    def print_program_line(program, n):
#        print("{:032b}|{:032b}|{:032b}|{:032b}".format(program[n][3],program[n][2],program[n][1],program[n][0]))

    #program = memory.array

    # create_instruction(_pynqcom.program[_pynqcom.current_bank],_pynqcom.current_addr % (_pynqcom.addr_range//16),flags,inst,inst_data,length)
    # _pynqcom.current_addr += 1
    # if (_pynqcom.current_addr % (_pynqcom.addr_range//16) == 0):
    #     _pynqcom.program.append(np.array(np.zeros([_pynqcom.addr_range//16,4]),dtype = np.uint32))
    #     _pynqcom.current_bank += 1
    # assert _pynqcom.current_bank < _pynqcom.max_banks, "Memory overflow"

    _check()
    if isinstance(flags, str) or isinstance(flags, bytes):
        flags = int(flags[::-1],2)
    create_instruction(_pynqcom.program[_pynqcom.current_bank],_pynqcom.current_addr % (_pynqcom.addr_range//16),flags,inst,inst_data,length)
    _pynqcom.current_addr += 1
    if (_pynqcom.current_addr % (_pynqcom.addr_range//16) == 0):
        _pynqcom.program.append(np.array(np.zeros([_pynqcom.addr_range//16,4]),dtype = np.uint32))
        _pynqcom.current_bank += 1
    assert _pynqcom.current_bank < _pynqcom.max_banks, "Memory overflow"
    return 0


def pb_inst_dds2(freq0,phase0,amp0,dds_en0,phase_reset0,
                 freq1,phase1,amp1,dds_en1,phase_reset1,
                 flags, inst, inst_data, length):
    """Gives a full instruction to the pulseblaster, with DDS included. The flags argument can be
       either an int representing the bitfield for the flag states, or a string of ones and zeros.
       Note that if passing in a string for the flag states, the first character represents flag 0.
       Eg.
       If it is a string:
            flag: 0          12
                 '101100011111'

       If it is a binary number (or integer:
            flag:12          0
                0b111110001101
                3981    <---- integer representation
       """
    '''
    _checkloaded()
    _spinapi.pb_inst_dds2.restype = ctypes.c_int
    if isinstance(flags, str) or isinstance(flags, bytes):
        flags = int(flags[::-1],2)
    result = _spinapi.pb_inst_dds2(ctypes.c_int(freq0),ctypes.c_int(phase0),ctypes.c_int(amp0),
                                  ctypes.c_int(dds_en0),ctypes.c_int(phase_reset0),
                                  ctypes.c_int(freq1),ctypes.c_int(phase1),ctypes.c_int(amp1),
                                  ctypes.c_int(dds_en1),ctypes.c_int(phase_reset1),
                                  ctypes.c_int(flags),ctypes.c_int(inst),
                                  ctypes.c_int(inst_data),ctypes.c_double(length))
    if result < 0: raise RuntimeError(pb_get_error())
    return result
    '''
    _check()
    if isinstance(flags, str) or isinstance(flags, bytes):
        flags = int(flags[::-1],2)
    create_instruction(_pynqcom.program[_pynqcom.current_bank],_pynqcom.current_addr % (_pynqcom.addr_range//16),flags,inst,inst_data,length)
    _pynqcom.current_addr += 1
    if (_pynqcom.current_addr % (_pynqcom.addr_range//16) == 0):
        _pynqcom.program.append(np.array(np.zeros([_pynqcom.addr_range//16,4]),dtype = np.uint32))
        _pynqcom.current_bank += 1
    assert _pynqcom.current_bank < _pynqcom.max_banks, "Memory overflow"
    return 0

# More convenience functions:
def program_freq_regs(*freqs, **kwargs):

    call_stop_programming = kwargs.pop('call_stop_programming', True)
    pb_start_programming(FREQ_REGS)
    for freq in freqs:
        pb_set_freq(freq)
    if call_stop_programming:
        pb_stop_programming()
    if len(freqs) == 1:
        return 0
    else:
        return tuple(range(len(freqs)))

def program_phase_regs(*phases, **kwargs):

    call_stop_programming = kwargs.pop('call_stop_programming', True)
    pb_start_programming(PHASE_REGS)
    for phase in phases:
        pb_set_phase(phase)
    if call_stop_programming:
        pb_stop_programming()
    if len(phases) == 1:
        return 0
    else:
        return tuple(range(len(phases)))

def program_amp_regs(*amps):

    for i, amp in enumerate(amps):
        pb_set_amp(amp,i)
    if len(amps) == 1:
        return 0
    else:
        return tuple(range(len(amps)))

def pb_stop_programming(trans_to_buffered=False):
    '''
    _checkloaded()
    _spinapi.pb_stop_programming.restype = ctypes.c_int
    result = _spinapi.pb_stop_programming()
    if result != 0: raise RuntimeError(pb_get_error())
    return result
    '''
    #stop_watchdog()
    _check()
    min_wait(DelayTime) 
    _pynqcom.send_string("receive_program(connection)")
    # length_of_program = np.array(_pynqcom.current_addr,dtype=np.uint32)
    length_of_program = np.array((_pynqcom.current_bank + 1) * _pynqcom.addr_range,dtype=np.uint32)
    _pynqcom.send_buff(memoryview(length_of_program))
    # _pynqcom.send_string("connection.receive_program(memory.array)")

    for i in _pynqcom.program:
        i.resize(_pynqcom.addr_range//4)
        _pynqcom.send_buff(memoryview(i))


    ###########
    ## Reading back data
    ###########
    ##   Receiving data size as 4 bytes to firm a 32 bit number
    #pynqapilogger.debug('Reading data back...')
    #data_size = np.array(0,dtype=np.uint32)
    ##buff = _pynqcom.read_all_data(4)
    ##np.copyto(data_size,np.frombuffer(buff,dtype=np.uint32))
    ##pynqapilogger.debug('Size read: %d' %data_size)
    ###Receiving program
    ##buff = _pynqcom.read_all_data(data_size)
    ###print("Buffer received {} bytes".format(len(buff)))
    ###with open(r'C:\Users\jqisr\labscript-suite\userlib\pythonlib\readback.log','a') as f:
    ###    f.write('Data read back: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + ": ")
    ###    f.write(buff.hex() + '\n')
    ###    #f.write(str(len(buff)) + '\n')
    ##pynqapilogger.debug('Read-back data written to file')
#
    #buff = _pynqcom.read_all_data(4)
    #np.copyto(data_size,np.frombuffer(buff,dtype=np.uint32))
    #pynqapilogger.debug('Size read: %d' %data_size)
    ##Receiving program
    #buff = _pynqcom.read_all_data(data_size)
    ##print("Buffer received {} bytes".format(len(buff)))
    #pynqapilogger.debug('Data read')
#
    #if trans_to_buffered:
    #    with open(r'C:\Users\jqisr\labscript-suite\userlib\pythonlib\send.log','a') as f:
    #        f.write('Data sent: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + ": ")
    #        s = ''
    #        for i in _pynqcom.program:
    #            i.resize(_pynqcom.addr_range//4)
    #            for j in i:
    #                #format(j, 'x')
    #                s += j.tobytes().hex()
    #        f.write(s.rstrip('0') + '\n')
#
    #    s = buff.hex()
    #    with open(r'C:\Users\jqisr\labscript-suite\userlib\pythonlib\readback.log','a') as f:
    #        f.write('Data read back: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + ': ' + s.rstrip('0') + '\n')# + ": " + buff.hex() + "\n")
    #        #f2.write('\n')
    #    pynqapilogger.debug('Read data written to file')
#
    ###########

    _pynqcom.program = [np.array(np.zeros([_pynqcom.addr_range//16,4]),dtype = np.uint32)]
    _pynqcom.current_addr = 0
    _pynqcom.current_bank = 0
    #restart_watchdog()

def pb_start():
    '''
    _checkloaded()
    _spinapi.pb_start.restype = ctypes.c_int
    result = _spinapi.pb_start()
    if result != 0: raise RuntimeError(pb_get_error())
    return result
    '''
    #stop_watchdog()
    _check()
    min_wait(DelayTime) 
    _pynqcom.send_string("toggle_start()")
    status = _pynqcom.read_all_data(1)
# Should be external trigger
    # _pynqcom.send_string("toggle_trigger()")
    #restart_watchdog()

def pb_stop():
    '''
    _checkloaded()
    _spinapi.pb_stop.restype = ctypes.c_int
    result = _spinapi.pb_stop()
    if result != 0: raise RuntimeError(pb_get_error())
    return result
    '''
    #stop_watchdog()
    _check()
    min_wait(DelayTime) 
    _pynqcom.send_string("reset_brd()")
    result = _pynqcom.read_all_data(1)
    #print(result)
    if not (result == b'\x00'):
        raise RuntimeError("PYNQ was not reset.")
    #restart_watchdog()
    return result

def pb_close():
    '''
    _checkloaded()
    _spinapi.pb_close.restype = ctypes.c_int
    result = _spinapi.pb_close()
    if result != 0: raise RuntimeError(pb_get_error())
    return result
    '''
    #stop_watchdog()
    _check()
#    _pynqcom.send_string("abort()")
#   _pynqcom.close()
    # del _pynqcom

def pb_reset():
    '''
    _checkloaded()
    _spinapi.pb_reset.restype = ctypes.c_int
    result = _spinapi.pb_reset()
    if result != 0: raise RuntimeError(pb_get_error())
    return result
    '''
    _check()
    _pynqcom.program = [np.array(np.zeros([_pynqcom.addr_range//16,4]),dtype = np.uint32)]
    _pynqcom.current_addr = 0
    _pynqcom.current_bank = 0

#INTERNAL FUNCTIONS

def debug_program_line(program, n):
    logging.debug("{:032b}|{:032b}|{:032b}|{:032b}".format(program[n][3],program[n][2],program[n][1],program[n][0]))

def create_instruction(program,n,flags,opcode,data,time):
    #flags=np.array(flags,dtype=np.uint32)
    #opcode=np.array(opcode,dtype=np.uint32)
    #data=np.array(data,dtype=np.uint32)
    #time=np.array(time,dtype=np.uint32)
    #offset = 524288//16\

    logging.debug("Flags type is: {}".format(type(flags)))
    logging.debug("Flags value is: {}".format(flags))
    flags = int(flags)

    flags_low=np.array(0xFFFFFFFF&flags,dtype=np.uint32)
    flags_hi=np.array(0xFFFFFFFF&(flags>>32),dtype=np.uint32)
    message = (0x000FFFFF & data)+((0x0000000F & opcode)<<20)|((0xFF & flags_low)<<24)

    logging.debug("message = {}".format(message))
    logging.debug("opcode = {}".format(opcode))
    logging.debug("data = {}".format(data))
    logging.debug("time = {}".format(time))
    logging.debug("flags_low = {:032b}".format(flags_low))
    logging.debug("flags_hi = {:032b}".format(flags_hi))
    logging.debug("flags = {:064b}".format(flags))

    #clock_rate = 20.0 #MHz
    clock_rate = _pynqcom.frequency

    new_time = int(time/1e3*clock_rate) - 1 #time is in ns

    if (new_time <= 0):
        raise RuntimeError(f"Time is too short. Time = {time}, new_time = {new_time}")

    logging.debug("n = {}, flags = {}, opcode = {}, data = {}, time = {}".format(n, flags, opcode, data, time))
    program[n][0] = new_time
    program[n][1] = ((0x000FFFFF & data) | ((0x0000000F & opcode)<<20) | ((0xFF & flags_low)<<24)).astype(np.uint32, casting = 'unsafe')
    program[n][2] = ((flags_low>>8) | ((0x00FFFFFF & flags_hi)<<24)).astype(np.uint32, casting = 'unsafe')
    program[n][3] = flags_hi>>8

    debug_program_line(program,n)
