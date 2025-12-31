from labscript import *
from labscriptlib.common.functions import *

from labscript_utils import import_or_reload
import_or_reload('labscriptlib.SrMain.connection_table')

t = 0
add_time_marker(t, 'Start', verbose=True)
start()
t += 0.01
add_time_marker(t, "Start expose", verbose=True)
#camera.expose(t,'test1','test2',0.01)
t += 0.01
add_time_marker(t, "End expose", verbose=True)
t += 0.01
add_time_marker(t, "End", verbose=True)
stop(t)
