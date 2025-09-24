from labscript import start, stop
from labscript_devices.lsduino import lsduino
from labscript_devices.AD9910 import AD9910
from labscript_devices.PrawnBlaster.labscript_devices import PrawnBlaster

PrawnBlaster(name='prawn', com_port='COM8', num_pseudoclocks=1,clock_frequency=100e6)
lsduino(name='dds_controller', ndev=1, parent_device=prawn.clocklines[0], com_port='com7', 
            baud_rate=115200, synchronous_first_line_repeat=True)

AD9910(name='dds_0',   parent_device=dds_controller, connection='channel 0')
#AD9910(name='dds_1',   parent_device=dds_controller, connection='channel 1')
#AD9910(name='dds_2',   parent_device=dds_controller, connection='channel 2')
#AD9910(name='dds_3',   parent_device=dds_controller, connection='channel 3')

if __name__ == '__main__':
    # Begin issuing labscript primitives
    # start() elicits the commencement of the shot
    start()

    # Stop the experiment shot with stop()
    stop(1.0)
