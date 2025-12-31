from labscript import *

from labscript_utils import import_or_reload
from labscriptlib.common.functions import *
import numpy as np

#import_or_reload('labscriptlib.example_experiment.connectiontable')
import_or_reload('labscriptlib.SrMain.connection_table')

start()

t = 0
scope_trigger.go_low(t)
t = 0.1
scope_trigger.go_high(t)
t += 0.1
t += wait(label='test',t=t,timeout=0.1)
scope_trigger.go_low(t)
t += 0.1

stop(t)