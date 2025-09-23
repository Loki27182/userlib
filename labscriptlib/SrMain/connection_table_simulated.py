from labscript import start, stop, add_time_marker, AnalogOut, DigitalOut, ClockLine
from labscript_devices.DummyPseudoclock.labscript_devices import DummyPseudoclock
from labscript_devices.DummyIntermediateDevice import DummyIntermediateDevice
from labscript_devices.lsduino import lsduino
from labscript_devices.AD9910 import AD9910

DummyPseudoclock(name='pseudoclock')

lsduino(name='dds_controller', ndev=2, parent_device=pseudoclock.clockline, com_port='com6', 
            baud_rate=115200, synchronous_first_line_repeat=True)

AD9910(name='dds_0',   parent_device=dds_controller, connection='channel 0')
AD9910(name='dds_1',   parent_device=dds_controller, connection='channel 1')
#AD9910(name='dds_2',   parent_device=dds_controller, connection='channel 2')
#AD9910(name='dds_3',   parent_device=dds_controller, connection='channel 3')

if __name__ == '__main__':
    # Begin issuing labscript primitives
    # start() elicits the commencement of the shot
    start()

    # Stop the experiment shot with stop()
    stop(1.0)
