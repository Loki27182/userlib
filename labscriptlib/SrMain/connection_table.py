from labscript import start, stop, add_time_marker, AnalogOut, DigitalOut, Trigger
from labscript_devices.DummyPseudoclock.labscript_devices import DummyPseudoclock
from labscript_devices.DummyIntermediateDevice import DummyIntermediateDevice
from labscript_devices.IMAQdxCamera.labscript_devices import IMAQdxCamera

DummyPseudoclock(name='pseudoclock')
DummyIntermediateDevice(name='intermediate_device', parent_device=pseudoclock.clockline)
Trigger(name='camera_trigger',parent_device=intermediate_device, connection = 'flag 3',  trigger_edge_type = 'rising')

IMAQdxCamera(
    name ='camera',
    parent_device=camera_trigger,
    connection='trigger',
    serial_number='B0BA19C9AD9FCC97',
    trigger_edge_type='rising',
    camera_attributes={},
    manual_mode_camera_attributes={},
)

if __name__ == '__main__':
    # Begin issuing labscript primitives
    # start() elicits the commencement of the shot
    start()

    # Stop the experiment shot with stop()
    stop(1.0)
