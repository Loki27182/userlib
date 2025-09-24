from labscript import start, stop
from labscript_utils import import_or_reload
from labscriptlib.common.functions import *
import numpy as np

import_or_reload('labscriptlib.SrMain.connection_table_simulated')

start()
t = 0

for freq in np.arange(201.1,201.901,0.005):
    dds_0.setfreq(t, freq, units = 'MHz') 
    t += .05

stop(t)