from labscript import *

from labscript_utils import import_or_reload
from labscriptlib.common.functions import *

#import_or_reload('labscriptlib.example_experiment.connectiontable')
import_or_reload('labscriptlib.SrMain.connection_table')

start()

t = 0
dt = 0.1

scope_trigger.go_high(t)
MOT_field.constant(t,0)
t+=dt
MOT_field.ramp(t,dt,0,.5,1000)
t+=dt
MOT_field.constant(t,.5)
t+=dt
MOT_field.ramp(t,2*dt,.5,.25,1000)
t+=2*dt
MOT_field.constant(t,.25)
t+=dt/2
MOT_field.ramp(t,2*dt,.25,1,1000)
t+=2*dt
MOT_field.constant(t,1)
t+=dt
MOT_field.ramp(t,2*dt,1,0,1000)
t+=2*dt
MOT_field.constant(t,0)
t+=dt/2
MOT_field.ramp(t,dt,0,3,100)
t+=dt
MOT_field.constant(t,3)
t+=dt/2
MOT_field.ramp(t,dt,3,0,100)
t+=dt
MOT_field.constant(t,0)
t+=1.5*dt
scope_trigger.go_low(t)

stop(t)