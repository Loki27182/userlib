from labscript import *

# from labscript_devices.PulseBlasterUSB import PulseBlasterUSB
from labscript_devices.Pyncmaster import Pyncmaster as PulseBlasterUSB
from labscript_devices.NI_DAQmx.labscript_devices import NI_PCI_6733, NI_PXIe_6361
from labscript_devices.Arduino_DDS import Arduino_DDS
from labscript_devices.Arduino_Single_DDS import Arduino_Single_DDS
from labscript_devices.Arduino_Repump_DDS import Arduino_Repump_DDS
from labscript_devices.RepumpDDS import RepumpDDS
from labscript_devices.DDSAD9954 import DDSAD9954
from labscript_devices.IMAQdxCamera.labscript_devices import IMAQdxCamera
from labscript_devices.PrincetonInstrumentsCamera.labscript_devices import PrincetonInstrumentsCamera
from labscript_devices.LightCrafterDMD import LightCrafterDMD, ImageSet

from labscript_utils.unitconversions.AOM_VCO import AOMVCO
from labscript_utils.unitconversions import UnidirectionalCoilDriver

###############################################################################
#    CONNECTION TABLE
###############################################################################

###############################################################################
#    PULSEBLASTER
###############################################################################

PulseBlasterUSB(name='pulseblaster_0', board_number=0, time_based_stop_workaround=True, time_based_stop_workaround_extra_time=0,clock_rate=20)

ClockLine(name='pulseblaster_0_ni_0_clock',				pseudoclock=pulseblaster_0.pseudoclock, connection='flag 0')
ClockLine(name='pulseblaster_0_ni_1_clock',             pseudoclock=pulseblaster_0.pseudoclock, connection='flag 11')
ClockLine(name='pulseblaster_0_ni_2_clock',             pseudoclock=pulseblaster_0.pseudoclock, connection='flag 14')
ClockLine(name='pulseblaster_0_blue_BN_arduino_clock', 	pseudoclock=pulseblaster_0.pseudoclock, connection='flag 1')
ClockLine(name='pulseblaster_0_red_AOM_arduino_clock',  pseudoclock=pulseblaster_0.pseudoclock, connection='flag 2')
ClockLine(name='pulseblaster_0_red_BN_arduino_clock',  pseudoclock=pulseblaster_0.pseudoclock, connection='flag 9')
ClockLine(name='pulseblaster_0_707_repump_arduino_clock',  pseudoclock=pulseblaster_0.pseudoclock, connection='flag 20')
ClockLine(name='pulseblaster_0_clock_EOM_arduino_clock',  pseudoclock=pulseblaster_0.pseudoclock, connection='flag 12')
# ClockLine(name='DMD_clock',                            pseudoclock=pulseblaster_0.pseudoclock, connection = 'flag 25')

Trigger(   name='GH_camera_trigger',        parent_device=pulseblaster_0.direct_outputs, connection = 'flag 3',  trigger_edge_type = 'falling')
Trigger(   name='flea_camera_trigger',      parent_device=pulseblaster_0.direct_outputs, connection = 'flag 22', trigger_edge_type = 'falling')
Trigger(   name='PIXIS_camera_trigger',     parent_device=pulseblaster_0.direct_outputs, connection = 'flag 15', trigger_edge_type = 'rising')
DigitalOut(name='current_lock_enable',      parent_device=pulseblaster_0.direct_outputs, connection = 'flag 4')
DigitalOut(name='red_inj_RF_TTL',   		parent_device=pulseblaster_0.direct_outputs, connection = 'flag 5')
DigitalOut(name='probe_shutter',            parent_device=pulseblaster_0.direct_outputs, connection = 'flag 6')
DigitalOut(name='probe_RF_TTL',             parent_device=pulseblaster_0.direct_outputs, connection = 'flag 7')
DigitalOut(name='red_MOT_RF_select',        parent_device=pulseblaster_0.direct_outputs, connection = 'flag 8')
DigitalOut(name='atom_shutter',             parent_device=pulseblaster_0.direct_outputs, connection = 'flag 10')
DigitalOut(name='main_DP_shutter',          parent_device=pulseblaster_0.direct_outputs, connection = 'flag 16')
DigitalOut(name='grating_MOT_AOM_TTL',      parent_device=pulseblaster_0.direct_outputs, connection = 'flag 23')
DigitalOut(name='grating_probe_AOM_TTL',    parent_device=pulseblaster_0.direct_outputs, connection = 'flag 21')
DigitalOut(name='cross_DP_shutter',         parent_device=pulseblaster_0.direct_outputs, connection = 'flag 17')
DigitalOut(name='cross_DP_AOM_TTL',         parent_device=pulseblaster_0.direct_outputs, connection = 'flag 18')
DigitalOut(name='vert_DP_shutter',          parent_device=pulseblaster_0.direct_outputs, connection = 'flag 19')
DigitalOut(name='vert_DP_AOM_TTL',          parent_device=pulseblaster_0.direct_outputs, connection = 'flag 13')
DigitalOut(name='gMOT_coil_TTL',            parent_device=pulseblaster_0.direct_outputs, connection = 'flag 24')
# DigitalOut(name='gMOT_IGBT_TTL',            parent_device=pulseblaster_0.direct_outputs, connection = 'flag 25')
#DigitalOut(name='gMOT_MOS_TTL_t',           parent_device=pulseblaster_0.direct_outputs, connection = 'flag 26')
DigitalOut(name='gMOT_MOS_TTL_b',           parent_device=pulseblaster_0.direct_outputs, connection = 'flag 27')
DigitalOut(name='pixis_ext_shutter',          parent_device=pulseblaster_0.direct_outputs, connection = 'flag 28')
DigitalOut(name='scope_trigger',          parent_device=pulseblaster_0.direct_outputs, connection = 'flag 25')



###############################################################################
#    NI CARD 1
###############################################################################

NI_PCI_6733(name='ni_0', parent_device=pulseblaster_0_ni_0_clock, clock_terminal='/Dev1/PFI1', MAX_name = 'Dev1')

AnalogOut(name='red_MOT_VCO',           parent_device=ni_0, connection='ao0',
          unit_conversion_class=AOMVCO,                     unit_conversion_parameters={'m':-22.422*10**6, 'b':60.831*10**6, 'magnitudes':['k','M']})
AnalogOut(name='red_SRS_amp',           parent_device=ni_0, connection='ao1',
          unit_conversion_class=AOMVCO,                     unit_conversion_parameters={'m':5.4466*10**6, 'b':0.14*10**6, 'magnitudes':['k','M']})
AnalogOut(name='MOT_field',             parent_device=ni_0, connection='ao2',
          unit_conversion_class=UnidirectionalCoilDriver,   unit_conversion_parameters={'slope':25, 'shift':0})
AnalogOut(name='shim_X',                parent_device=ni_0, connection='ao3',
          unit_conversion_class=UnidirectionalCoilDriver,   unit_conversion_parameters={'slope':0.6, 'shift':-0.022})
AnalogOut(name='shim_Y',                parent_device=ni_0, connection='ao4',
          unit_conversion_class=UnidirectionalCoilDriver,   unit_conversion_parameters={'slope':0.6, 'shift':-0.022})
AnalogOut(name='shim_Z',                parent_device=ni_0, connection='ao5',
          unit_conversion_class=UnidirectionalCoilDriver,   unit_conversion_parameters={'slope':0.6, 'shift':-0.022})
AnalogOut(name='blue_MOT_power',        parent_device=ni_0, connection='ao6')
AnalogOut(name='red_MOT_power',         parent_device=ni_0, connection='ao7')

DigitalOut(name='blue_MOT_shutter',     parent_device=ni_0, connection='port0/line0')
DigitalOut(name='blue_MOT_RF_TTL',      parent_device=ni_0, connection='port0/line1')
DigitalOut(name='MOT_2D_RF_TTL',        parent_device=ni_0, connection='port0/line2')
DigitalOut(name='red_MOT_shutter',      parent_device=ni_0, connection='port0/line3')
DigitalOut(name='red_MOT_RF_TTL',       parent_device=ni_0, connection='port0/line4')
DigitalOut(name='red_SRS_TTL',          parent_device=ni_0, connection='port0/line5')
DigitalOut(name='repump_707_shutter',   parent_device=ni_0, connection='port0/line6')
DigitalOut(name='repump_679_shutter',   parent_device=ni_0, connection='port0/line7')

###############################################################################
#    NI CARD 2
###############################################################################

NI_PCI_6733(name='ni_1', parent_device=pulseblaster_0_ni_1_clock, clock_terminal='/Dev2/PFI1', MAX_name = 'Dev2')

AnalogOut(name='red_inj_VCO',           parent_device=ni_1, connection='ao0',
          unit_conversion_class=AOMVCO,                     unit_conversion_parameters={'m':-21.57549*10**6, 'b':61.48349*10**6, 'magnitudes':['k','M']})
AnalogOut(name='red_inj_power',         parent_device=ni_1, connection='ao1')
AnalogOut(name='grating_MOT_power',     parent_device=ni_1, connection='ao2')
AnalogOut(name='grating_coil_current',         parent_device=ni_1, connection='ao3',
          unit_conversion_class=UnidirectionalCoilDriver,   unit_conversion_parameters={'slope':10, 'shift':0})
AnalogOut(name='main_DP_power',         parent_device=ni_1, connection='ao4')
AnalogOut(name='cross_DP_power',         parent_device=ni_1, connection='ao5')
AnalogOut(name='gMOT_coil_current_t',   parent_device=ni_1, connection='ao6')
AnalogOut(name='gMOT_coil_current_b',   parent_device=ni_1, connection='ao7')

DigitalOut(name='IGBT_TTL',             parent_device=ni_1, connection='port0/line0')
DigitalOut(name='main_DP_AOM_TTL',                parent_device=ni_1, connection='port0/line1')
# Trigger(   name='GH_camera_trigger',        parent_device=ni_1, connection='port0/line2',  trigger_edge_type = 'falling')
DigitalOut(name='fake_do',             parent_device=ni_1, connection='port0/line2')
DigitalOut(name='gMOT_IGBT_TTL',        parent_device=ni_1, connection='port0/line4')

################################################################################
#   NI CARD 4
################################################################################

NI_PXIe_6361(name='ni_2', parent_device=pulseblaster_0_ni_2_clock, clock_terminal='/Dev4/PFI0', MAX_name = 'Dev4')#,acquisition_rate=100000)

AnalogOut(name='grating_shim_y', parent_device=ni_2, connection='ao0')
AnalogOut(name='extra', parent_device=ni_2, connection='ao1')
#AnalogIn(name='Analog_Input_Test', parent_device=ni_2, connection='ai0') # Not working - do not use

# # DigitalOut(name='newNITest',parent_device=ni_2,connection = 'port0/line0')
# DigitalOut(name='fake3',  parent_device=ni_2, connection = 'port0/line1')

################################################################################
#   Wait Monitor
################################################################################

# WaitMonitor(name='blue_fluor_wait',
#             parent_device=ni_2, connection='port0/line0',
#             acquisition_device=ni_2, acquisition_connection='ctr0',
#             timeout_device=ni_2, timeout_connection='pfi13')

################################################################################
#    BLUE BN ARDUINO
################################################################################

Arduino_DDS(name='blue_BN_arduino', parent_device=pulseblaster_0_blue_BN_arduino_clock, com_port='com5', baud_rate=115200, synchronous_first_line_repeat=True)

DDSAD9954(name='blue_BN_DDS',       parent_device=blue_BN_arduino, connection='channel 0')
DDSAD9954(name='blue_broken_DDS',   parent_device=blue_BN_arduino, connection='channel 1')

################################################################################
#    Red BN ARDUINO
################################################################################

Arduino_Single_DDS(name='red_BN_arduino', parent_device=pulseblaster_0_red_BN_arduino_clock, com_port='com7', baud_rate=115200, synchronous_first_line_repeat=True)

DDSAD9954(name='red_BN_DDS',       parent_device=red_BN_arduino, connection='channel 0')

################################################################################
#    RED AOM ARDUINO
################################################################################

# Arduino_DDS(name='red_AOM_arduino', parent_device=pulseblaster_0_red_AOM_arduino_clock, com_port='com5',  baud_rate=115200, synchronous_first_line_repeat=True)
#
# DDSAD9954(name='red_AOM_DDS',       parent_device=red_AOM_arduino, connection='channel 0')
# DDSAD9954(name='red_unused_DDS',    parent_device=red_AOM_arduino, connection='channel 1')

################################################################################
#    707 Repump ARDUINO
################################################################################

#Arduino_Repump_DDS(name='repump_707_arduino', parent_device=pulseblaster_0_707_repump_arduino_clock, com_port='com40', baud_rate=115200, synchronous_first_line_repeat=True)

#RepumpDDS(name='repump_707_DDS',       parent_device=repump_707_arduino, connection='channel 0')

################################################################################
#   Clock EOM Arduino
################################################################################

# Arduino_Single_DDS(name='clock_EOM_arduino', parent_device=pulseblaster_0_clock_EOM_arduino_clock, com_port='com31', baud_rate=115200, synchronous_first_line_repeat=True)
#
# DDSAD9954(name='clock_EOM_DDS', parent_device=clock_EOM_arduino, connection='channel 0')

################################################################################
#   PIXIS Camera
################################################################################
"""
PIXIS_sequence_camera_attributes = {'ExposureTime': 10, 'SensorTemperatureSetPoint': -75, 'ShutterTimingMode': 3}
#
PrincetonInstrumentsCamera(name='PIXIS', parent_device=PIXIS_camera_trigger, connection = 'trigger', camera_ID = 0, orientation = "vertical"
,camera_attributes=PIXIS_sequence_camera_attributes)
"""
################################################################################
#	FLEA CAMERA
################################################################################

#RemoteBLACS('acquisition_computer', 'Acquisition')

"""FleaCameraUSB_manual_camera_attributes = {
    'AcquisitionAttributes::Timeout': 10000,
    'CameraAttributes::AcquisitionControl::AcquisitionMode': 'Continuous',
    'CameraAttributes::AcquisitionControl::ExposureMode': 'Timed',
    'CameraAttributes::AcquisitionControl::TriggerActivation': 'Falling Edge',
    'CameraAttributes::AcquisitionControl::TriggerDelayEnabled': 0,
    'CameraAttributes::AcquisitionControl::TriggerMode': 'Off',
    'CameraAttributes::AcquisitionControl::TriggerSelector': 'Frame Start',
    'CameraAttributes::AcquisitionControl::TriggerSource': 'Line 0',
    'CameraAttributes::AnalogControl::BlackLevel': 1.46484375,
    'CameraAttributes::AnalogControl::BlackLevelEnabled': 1,
    'CameraAttributes::AnalogControl::GainAuto': 'Off',
    'CameraAttributes::AnalogControl::GammaEnabled': 0,
    'CameraAttributes::AnalogControl::SharpnessEnabled': 0,
    # 'CameraAttributes::ImageFormatControl::OffsetY': 0,
    # 'CameraAttributes::ImageFormatControl::Height': 1024,

    'CameraAttributes::ImageFormatControl::Height': 800,
    'CameraAttributes::ImageFormatControl::OffsetY': 100,
}

FleaCameraUSB_sequence_camera_attributes = {
    'AcquisitionAttributes::Timeout': 10000,
    'CameraAttributes::AcquisitionControl::AcquisitionMode': 'Continuous',
    'CameraAttributes::AcquisitionControl::ExposureMode': 'Trigger Width',
    'CameraAttributes::AcquisitionControl::TriggerActivation': 'Falling Edge',
    'CameraAttributes::AcquisitionControl::TriggerDelayEnabled': 0,
    'CameraAttributes::AcquisitionControl::TriggerMode': 'On',
    'CameraAttributes::AcquisitionControl::TriggerSelector': 'Exposure Active',
    'CameraAttributes::AcquisitionControl::TriggerSource': 'Line 0',
    'CameraAttributes::AnalogControl::BlackLevel': 1.46484375,
    'CameraAttributes::AnalogControl::BlackLevelEnabled': 1,
    'CameraAttributes::AnalogControl::GainAuto': 'Off',
    'CameraAttributes::AnalogControl::GammaEnabled': 0,
    'CameraAttributes::AnalogControl::SharpnessEnabled': 0,
    'CameraAttributes::ImageFormatControl::OffsetY': 0,
    'CameraAttributes::ImageFormatControl::Height': 1024,
}

IMAQdxCamera(
   name ='FleaCamera_gMOT',
   parent_device=flea_camera_trigger,
   connection='trigger',
   serial_number='1E1000F7DC41',
   trigger_edge_type='falling',
   worker=acquisition_computer,
   orientation = 'grating',
   camera_attributes=FleaCameraUSB_sequence_camera_attributes,
   manual_mode_camera_attributes=FleaCameraUSB_manual_camera_attributes
)"""


Grasshopper_manual_camera_attributes = {
    'CameraAttributes::ImageFormatControl::OnBoardColorProcessEnabled': 0,
    'CameraAttributes::AnalogControl::GainAuto': 'Off',
	'CameraAttributes::AnalogControl::Gain': 0,
	'CameraAttributes::AnalogControl::BlackLevelEnabled': 1,
	'CameraAttributes::AnalogControl::BlackLevel': 0.4432,
	'CameraAttributes::AnalogControl::GammaEnabled': 0,
    'CameraAttributes::AcquisitionControl::TriggerSelector': 'Frame Start',
    'CameraAttributes::AcquisitionControl::TriggerMode': 'Off',
    'CameraAttributes::AcquisitionControl::TriggerSource': 'Line 0',
    'CameraAttributes::AcquisitionControl::TriggerActivation': 'Falling Edge',
    'CameraAttributes::AcquisitionControl::ExposureMode': 'Timed',
    'CameraAttributes::AcquisitionControl::ExposureAuto': 'Off',
	'CameraAttributes::AcquisitionControl::ExposureTime': 200.0,
    'CameraAttributes::AcquisitionControl::pgrExposureCompensationAuto': 'Off',
    'CameraAttributes::AcquisitionControl::pgrExposureCompensation': 0,
    'CameraAttributes::ImageFormatControl::VideoMode': 7
}

Grasshopper_sequence_camera_attributes = {
    'CameraAttributes::ImageFormatControl::OnBoardColorProcessEnabled': 0,
    'CameraAttributes::AnalogControl::GainAuto': 'Off',
	'CameraAttributes::AnalogControl::Gain': 0,
	'CameraAttributes::AnalogControl::BlackLevelEnabled': 1,
	'CameraAttributes::AnalogControl::BlackLevel': 0.4432,
	'CameraAttributes::AnalogControl::GammaEnabled': 0,
	'CameraAttributes::AcquisitionControl::ExposureTime': 200.0,
    'CameraAttributes::AcquisitionControl::ExposureAuto': 'Off',
    'CameraAttributes::AcquisitionControl::pgrExposureCompensation': 0,
    'CameraAttributes::AcquisitionControl::pgrExposureCompensationAuto': 'Off',
    'CameraAttributes::AcquisitionControl::TriggerSelector': 'Exposure Active',
    'CameraAttributes::AcquisitionControl::TriggerMode': 'On',
    'CameraAttributes::AcquisitionControl::TriggerSource': 'Line 0',
    'CameraAttributes::AcquisitionControl::TriggerActivation': 'Falling Edge',
    'CameraAttributes::AcquisitionControl::ExposureMode': 'Trigger Width',
    'CameraAttributes::ImageFormatControl::VideoMode': 7
}

# FleaCameraUSB_camera_attributes = {
#     'AcquisitionAttributes::Timeout': 10000,
#     'CameraAttributes::AcquisitionControl::AcquisitionMode': 'Continuous',
#     'CameraAttributes::AcquisitionControl::ExposureMode': 'Trigger Width',
#     'CameraAttributes::AcquisitionControl::TriggerActivation': 'Falling Edge',
#     'CameraAttributes::AcquisitionControl::TriggerDelay': 0.0,
#     'CameraAttributes::AcquisitionControl::TriggerDelayEnabled': 0,
#     'CameraAttributes::AcquisitionControl::TriggerMode': 'On',
#     'CameraAttributes::AcquisitionControl::TriggerSelector': 'Exposure Active',
#     'CameraAttributes::AcquisitionControl::TriggerSource': 'Line 0',
# }

IMAQdxCamera(
    name ='GrassHp_XZ',
    parent_device=GH_camera_trigger,
    connection='trigger',
    serial_number='1E1000E6C21E',
    trigger_edge_type='falling',
	#worker=acquisition_computer,
	orientation = 'horizontal',
    camera_attributes=Grasshopper_sequence_camera_attributes,
    manual_mode_camera_attributes=Grasshopper_manual_camera_attributes,
)

# LightCrafterDMD(
#     name = 'DMD',
#     parent_device = DMD_clock
# )
#
# ImageSet(
#     name = "testImage",
#     parent_device = DMD
# )
################################################################################
if __name__ == '__main__':
    start()
    stop(1)
