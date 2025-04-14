from labscript import *

from labscript_utils import import_or_reload
from labscriptlib.common.functions import *
import numpy as np

#import_or_reload('labscriptlib.example_experiment.connectiontable')
import_or_reload('labscriptlib.SrMain.connection_table')

dt = 1

start()

t = 0
red_MOT_RF_select.go_high(t)

df = 20
N = 10

for i in range(N):
    scope_trigger.go_low(t)
    red_AOM_DDS.setfreq(t,70+2*i*df/(2*N), units = 'MHz') 
    #red_MOT_VCO.constant(t, 70+2*i*df/(2*N), units = 'MHz')
    t += dt
    scope_trigger.go_high(t)
    red_AOM_DDS.setfreq(t,70+(2*i+1)*df/(2*N), units = 'MHz') 
    #red_MOT_VCO.constant(t, 70+(2*i+1)*df/(2*N), units = 'MHz')
    t += dt

stop(t)