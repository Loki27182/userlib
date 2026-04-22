from labscript import *

from labscript_utils import import_or_reload
from labscriptlib.common.functions import *
import numpy as np

#import_or_reload('labscriptlib.example_experiment.connectiontable')
import_or_reload('labscriptlib.SrMain.connection_table')

def dumb_wait(label,t,timeout,delay):
    dt = 0
    dt += wait(label=label + '-1',t=t+dt,timeout=timeout)
    dt += delay
    dt += wait(label=label + '-2',t=t+dt,timeout=timeout)
    dt += delay
    dt += wait(label=label + '-3',t=t+dt,timeout=timeout)
    return dt


start()

t = 0
scope_trigger.go_low(t)
t = 0.1
scope_trigger.go_high(t-.0001)
t += dumb_wait(label='test',t=t,timeout=0.05,delay=0.01)
scope_trigger.go_low(t)
t += 0.1

stop(t)