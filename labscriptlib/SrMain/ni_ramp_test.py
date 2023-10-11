from labscript import *

from labscript_utils import import_or_reload
from labscriptlib.common.functions import *

#import_or_reload('labscriptlib.example_experiment.connectiontable')
import_or_reload('labscriptlib.SrMain.connection_table')

start()


t = 0
dt = 0.01

scope_trigger.go_high(t)

for ii in range(10):
    MOT_field.constant(t,ii/10)
    t += dt

level = 0
dt = 0.1
for ii in range(9):
    if level==0:
        newlevel = ii/10
        print(newlevel)
    else:
        newlevel = 0
    MOT_field.ramp(t,0.1,level,newlevel,1000)
    level = newlevel
    t += dt

scope_trigger.go_low(t)

stop(t+.01)