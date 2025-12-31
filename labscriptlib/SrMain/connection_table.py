from labscript import start, stop
from labscript import ClockLine, DigitalOut, AnalogOut, Trigger
from labscript_devices.Pyncmaster import Pyncmaster as PulseBlasterUSB
from labscript_devices.NI_DAQmx.labscript_devices import NI_PCI_6733, NI_PXIe_6361
from labscript_devices.Arduino_DDS import Arduino_DDS
from labscript_devices.Arduino_DDS_n_ch import Arduino_DDS_n_ch
from labscript_devices.Arduino_Single_DDS import Arduino_Single_DDS
from labscript_devices.Arduino_Repump_DDS import Arduino_Repump_DDS
from labscript_devices.RepumpDDS import RepumpDDS
from labscript_devices.DDSAD9954 import DDSAD9954
from labscript_devices.IMAQdxCamera.labscript_devices import IMAQdxCamera
from labscript_devices.SpinnakerCamera.labscript_devices import SpinnakerCamera
from labscript_devices.PrincetonInstrumentsCamera.labscript_devices import PrincetonInstrumentsCamera
from labscript_devices.LightCrafterDMD import LightCrafterDMD, ImageSet
from labscript_devices.AD9914 import AD9914
from labscript_devices.lsduino import lsduino
from labscript_devices.AD9910 import AD9910
import logging

from labscript_utils.unitconversions.AOM_VCO import AOMVCO
from labscript_utils.unitconversions import UnidirectionalCoilDriver

from labscriptlib.SrMain.Subroutines.ConnectionTableSubs import black_level

###############################################################################
#    CONNECTION TABLE
###############################################################################

###############################################################################
#    PULSEBLASTER
###############################################################################

PulseBlasterUSB(name='pulseblaster_0', board_number=0, #programming_scheme='pb_stop_programming/STOP',
                time_based_stop_workaround=True, time_based_stop_workaround_extra_time=0,
                clock_rate=20,log_level=logging.INFO)

ClockLine(name='pulseblaster_0_ni_0_clock',				pseudoclock=pulseblaster_0.pseudoclock, connection='flag 0')
ClockLine(name='pulseblaster_0_ni_1_clock',             pseudoclock=pulseblaster_0.pseudoclock, connection='flag 11')
ClockLine(name='pulseblaster_0_ni_2_clock',             pseudoclock=pulseblaster_0.pseudoclock, connection='flag 14')
ClockLine(name='pulseblaster_0_blue_BN_arduino_clock', 	pseudoclock=pulseblaster_0.pseudoclock, connection='flag 1')
ClockLine(name='pulseblaster_0_red_BN_arduino_clock',   pseudoclock=pulseblaster_0.pseudoclock, connection='flag 9')
ClockLine(name='pulseblaster_0_lsduino_clock',          pseudoclock=pulseblaster_0.pseudoclock, connection='flag 24')
ClockLine(name='pulseblaster_0_lsduino_clock_2',          pseudoclock=pulseblaster_0.pseudoclock, connection='flag 34')

#Trigger(   name='pulseblaster_0_lsduino_clock',        parent_device=pulseblaster_0.direct_outputs, connection = 'flag 24',  trigger_edge_type = 'falling')

Trigger(   name='GH_camera_trigger',        parent_device=pulseblaster_0.direct_outputs, connection = 'flag 3',  trigger_edge_type = 'falling')
Trigger(   name='Blackfly_camera_trigger',        parent_device=pulseblaster_0.direct_outputs, connection = 'flag 23',  trigger_edge_type = 'falling')

DigitalOut(name='current_lock_enable',      parent_device=pulseblaster_0.direct_outputs, connection = 'flag 4')
DigitalOut(name='scope_trigger',   		parent_device=pulseblaster_0.direct_outputs, connection = 'flag 5')
DigitalOut(name='probe_shutter',            parent_device=pulseblaster_0.direct_outputs, connection = 'flag 6')
DigitalOut(name='probe_RF_TTL',             parent_device=pulseblaster_0.direct_outputs, connection = 'flag 7')
DigitalOut(name='red_MOT_RF_select',        parent_device=pulseblaster_0.direct_outputs, connection = 'flag 8')
DigitalOut(name='red_MOT_Int_Disable',      parent_device=pulseblaster_0.direct_outputs, connection = 'flag 10')
DigitalOut(name='red_aux_shutter',          parent_device=pulseblaster_0.direct_outputs, connection = 'flag 16')
DigitalOut(name='dipole_RF_TTL',         parent_device=pulseblaster_0.direct_outputs, connection = 'flag 17')
DigitalOut(name='dipole_shutter',         parent_device=pulseblaster_0.direct_outputs, connection = 'flag 18')

DigitalOut(name='repump_707_TTL',          parent_device=pulseblaster_0.direct_outputs, connection = 'flag 19')
DigitalOut(name='repump_707_shutter',      parent_device=pulseblaster_0.direct_outputs, connection = 'flag 20')
DigitalOut(name='repump_679_RF_TTL',         parent_device=pulseblaster_0.direct_outputs, connection = 'flag 21')
DigitalOut(name='repump_679_shutter',         parent_device=pulseblaster_0.direct_outputs, connection = 'flag 22')
DigitalOut(name='repump_688_RF_TTL',         parent_device=pulseblaster_0.direct_outputs, connection = 'flag 26')
DigitalOut(name='repump_688_shutter',         parent_device=pulseblaster_0.direct_outputs, connection = 'flag 27')
DigitalOut(name='h_bridge_enable',         parent_device=pulseblaster_0.direct_outputs, connection = 'flag 32')

###############################################################################
#    NI CARD 1
###############################################################################

NI_PCI_6733(name='ni_0', parent_device=pulseblaster_0_ni_0_clock, clock_terminal='/Dev1/PFI1', MAX_name = 'Dev1')

AnalogOut(name='unused_0',          parent_device=ni_0, connection='ao0')
AnalogOut(name='red_MOT_VCO',           parent_device=ni_0, connection='ao1',
          unit_conversion_class=AOMVCO,                     unit_conversion_parameters={'m':1.0282*10**6, 'b':79.9881*10**6, 'magnitudes':['k','M']})   # From data on 2024-04-01
AnalogOut(name='mot_field',             parent_device=ni_0, connection='ao2',
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
DigitalOut(name='source_RF_TTL',        parent_device=ni_0, connection='port0/line2')
DigitalOut(name='red_MOT_shutter',      parent_device=ni_0, connection='port0/line3')
DigitalOut(name='red_MOT_RF_TTL',       parent_device=ni_0, connection='port0/line4')
DigitalOut(name='red_SRS_TTL',          parent_device=ni_0, connection='port0/line5')
#DigitalOut(name='repump_707_shutter',   parent_device=ni_0, connection='port0/line6')
#DigitalOut(name='repump_679_RF_TTL',   parent_device=ni_0, connection='port0/line7')

###############################################################################
#    NI CARD 2
###############################################################################

NI_PCI_6733(name='ni_1', parent_device=pulseblaster_0_ni_1_clock, clock_terminal='/Dev2/PFI1', MAX_name = 'Dev2')

AnalogOut(name='probe_VCO', parent_device=ni_1, connection='ao0')
AnalogOut(name='dipole_power',  parent_device=ni_1, connection='ao1')

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

#################################################################################
##    Testing new DDS arduino controller
#################################################################################
#lsduino(name='dds_controller', ndev=2, parent_device=pulseblaster_0_lsduino_clock, com_port='com15', 
#            baud_rate=115200, synchronous_first_line_repeat=True)
#
#AD9910(name='dds_0',   parent_device=dds_controller, connection='channel 0')
#AD9910(name='dds_1',   parent_device=dds_controller, connection='channel 1')
#
#lsduino(name='dds_controller_2', ndev=2, parent_device=pulseblaster_0_lsduino_clock_2, com_port='com21', 
#            baud_rate=115200, synchronous_first_line_repeat=True)
#
#AD9910(name='dds_2',   parent_device=dds_controller_2, connection='channel 0')
#AD9910(name='dds_3',   parent_device=dds_controller_2, connection='channel 1')

#################################################################################################################
# Change these values to set up the grasshopper camera
# Basic device setup
gh_name = 'cam_xz'
gh_trig = GH_camera_trigger
gh_SN = '1E1000E6C21E'
gh_image_folder = 'xz'

# Exposure settings
gh_mode = 7                     # Camera mode, must be 0 or 7. Mode 0 is higher noise, but also higher frame rate.
gh_exp = 5000.0   # Camera exposure time in us for manual mode (40us to 30s, but timeout needs to be increased from 5s for long exposures)
gh_gain_man =  0                    # Camera gain setting in dB. Must be between 0 and 24 (inclusive)
gh_gain_seq =  0                    # Camera gain setting in dB. Must be between 0 and 24 (inclusive)
gh_acceptable_zeros = 100       # The black level is calculated such that you will on average
                                    # have camera_acceptable_zeros zero counts on the low end of the distribution.
                                    # This should be small, as any pixel that would be less than zero 
                                    # will be clipped to 0, which we don't want for actual data

#################################################################################################################
# # Change these values to set up the blackfly camera
# Basic device setup
bf_name = 'cam_yz'
bf_trig = Blackfly_camera_trigger
bf_SN = '1E1001674ED9'
bf_image_folder = 'yz'

# Exposure settings
bf_mode = 7
bf_exp = 5000.0
bf_gain_man = 0
bf_gain_seq = 24
# Still need to calibrate black level function for the blackfly, and standardize that process

#################################################################################################################
# You shouldn't need to change anything below here for camera settings
#################################################################################################################

# Calculating correct black level for given settings
gh_black_level_man = black_level(gh_gain_man,gh_mode,gh_acceptable_zeros)
gh_black_level_seq = black_level(gh_gain_seq,gh_mode,gh_acceptable_zeros)

# Make attributes dict for GH manual and sequence modes
gh_attr_man = {
    'CameraAttributes::ImageFormatControl::OnBoardColorProcessEnabled': 0,
    'CameraAttributes::AnalogControl::GainAuto': 'Off',
	'CameraAttributes::AnalogControl::Gain': gh_gain_man,
	'CameraAttributes::AnalogControl::BlackLevel': gh_black_level_man,
	'CameraAttributes::AnalogControl::GammaEnabled': 0,
    'CameraAttributes::AcquisitionControl::TriggerMode': 'Off',
    'CameraAttributes::AcquisitionControl::AcquisitionFrameRateEnabled': 0,
    'CameraAttributes::AcquisitionControl::TriggerSelector': 'Frame Start',
    'CameraAttributes::AcquisitionControl::TriggerSource': 'Line 0',
    'CameraAttributes::AcquisitionControl::TriggerActivation': 'Falling Edge',
    'CameraAttributes::AcquisitionControl::ExposureMode': 'Timed',
    'CameraAttributes::AcquisitionControl::ExposureAuto': 'Off',
	'CameraAttributes::AcquisitionControl::ExposureTime': gh_exp,
    'CameraAttributes::AcquisitionControl::pgrExposureCompensationAuto': 'Off',
    'CameraAttributes::AcquisitionControl::pgrExposureCompensation': 0,
    'CameraAttributes::ImageFormatControl::VideoMode': gh_mode
}
gh_attr_seq = {
    'CameraAttributes::ImageFormatControl::OnBoardColorProcessEnabled': 0,
    'CameraAttributes::AnalogControl::GainAuto': 'Off',
	'CameraAttributes::AnalogControl::Gain': gh_gain_seq,
	'CameraAttributes::AnalogControl::BlackLevel': gh_black_level_seq,
	'CameraAttributes::AnalogControl::GammaEnabled': 0,
	'CameraAttributes::AcquisitionControl::ExposureTime': gh_exp,
    'CameraAttributes::AcquisitionControl::ExposureAuto': 'Off',
    'CameraAttributes::AcquisitionControl::pgrExposureCompensation': 0,
    'CameraAttributes::AcquisitionControl::pgrExposureCompensationAuto': 'Off',
    'CameraAttributes::AcquisitionControl::AcquisitionFrameRateEnabled': 0,
    'CameraAttributes::AcquisitionControl::TriggerSelector': 'Exposure Active',
    'CameraAttributes::AcquisitionControl::TriggerMode': 'On',
    'CameraAttributes::AcquisitionControl::TriggerSource': 'Line 0',
    'CameraAttributes::AcquisitionControl::TriggerActivation': 'Falling Edge',
    'CameraAttributes::AcquisitionControl::ExposureMode': 'Trigger Width',
    'CameraAttributes::ImageFormatControl::VideoMode': gh_mode
}

# Make attributes dict for Blackfly manual and sequence modes
bf_attr_man = {
    'CameraAttributes::AnalogControl::GainAuto': 'Off',
	'CameraAttributes::AnalogControl::Gain': bf_gain_man,
	'CameraAttributes::AnalogControl::GainConversion': 'HCG',
	'CameraAttributes::AnalogControl::BlackLevel': 0,
	'CameraAttributes::AnalogControl::BlackLevelClampingEnable': 1,
	'CameraAttributes::AnalogControl::GammaEnable': 0,
    'CameraAttributes::AcquisitionControl::ExposureMode': 'Timed',
    'CameraAttributes::AcquisitionControl::TriggerMode': 'Off',
    'CameraAttributes::AcquisitionControl::AcquisitionFrameRateEnable': 0,
    'CameraAttributes::AcquisitionControl::TriggerDelay': 25.0,
    'CameraAttributes::AcquisitionControl::TriggerSource': 'Line 0',
    'CameraAttributes::AcquisitionControl::TriggerActivation': 'Falling Edge',
    'CameraAttributes::AcquisitionControl::ExposureAuto': 'Off',
	'CameraAttributes::AcquisitionControl::ExposureTime': bf_exp,
    'CameraAttributes::ImageFormatControl::PixelFormat': 'Mono16',
    'CameraAttributes::ImageFormatControl::AdcBitDepth': '12 Bit',
    'CameraAttributes::ImageFormatControl::ReverseX': 0,
    'CameraAttributes::ImageFormatControl::ReverseY': 1,
}

bf_attr_seq = {
    'CameraAttributes::AnalogControl::GainAuto': 'Off',
	'CameraAttributes::AnalogControl::Gain': bf_gain_seq,
	'CameraAttributes::AnalogControl::GainConversion': 'HCG',
	'CameraAttributes::AnalogControl::BlackLevel': 0,
	'CameraAttributes::AnalogControl::BlackLevelClampingEnable': 1,
	'CameraAttributes::AnalogControl::GammaEnable': 0,
	'CameraAttributes::AcquisitionControl::ExposureTime': bf_exp,
    'CameraAttributes::AcquisitionControl::ExposureAuto': 'Off',
    'CameraAttributes::AcquisitionControl::AcquisitionFrameRateEnable': 0,
    'CameraAttributes::AcquisitionControl::TriggerDelay': 25.0,
    'CameraAttributes::AcquisitionControl::TriggerMode': 'On',
    'CameraAttributes::AcquisitionControl::TriggerSource': 'Line 0',
    'CameraAttributes::AcquisitionControl::TriggerActivation': 'Falling Edge',
    'CameraAttributes::AcquisitionControl::ExposureMode': 'Trigger Width',
    'CameraAttributes::ImageFormatControl::PixelFormat': 'Mono16',
    'CameraAttributes::ImageFormatControl::AdcBitDepth': '12 Bit',
    'CameraAttributes::ImageFormatControl::ReverseX': 0,
    'CameraAttributes::ImageFormatControl::ReverseY': 1,
}

# Make actual GH camera device
IMAQdxCamera(
    name = gh_name,
    parent_device=gh_trig,
    connection='trigger',
    serial_number=gh_SN,
    trigger_edge_type='falling',
	orientation = gh_image_folder,
    camera_attributes=gh_attr_seq,
    manual_mode_camera_attributes=gh_attr_man,
)

# Make actual Blackfly camera device
IMAQdxCamera(
    name = bf_name,
    parent_device = bf_trig,
    connection = 'trigger',
    serial_number = bf_SN,
    trigger_edge_type = 'falling',
    orientation = bf_image_folder,
    camera_attributes=bf_attr_seq,
    manual_mode_camera_attributes=bf_attr_man,
)


################################################################################
if __name__ == '__main__':
    start()
    stop(1)
