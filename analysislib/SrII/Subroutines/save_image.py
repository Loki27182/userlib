from lyse import *
import numpy as np
from labscript_utils.camera_server import CameraServer
import labscript_utils.shared_drive
# importing this wraps zlock calls around HDF file openings and closings:
import labscript_utils.h5_lock
import h5py

def save_image(run, data, group, name):
    with h5py.File(h5_filepath, 'r+') as h5_file:
        image_group = h5_file.require_group(group)
        image_group.attrs['camera'] = "processed_images".encode('utf8')
        image_group.attrs.create(
            'ExposureTimeAbs', self.exposure_time, dtype='float64')
        image_group.attrs.create(
            'Width', self.width, dtype='int64')
        image_group.attrs.create(
            'Height', self.height, dtype='int64')
        if self.binning_horizontal:
            image_group.attrs.create(
                'BinningHorizontal', self.binning_horizontal, dtype='int8')
        if self.binning_vertical:
            image_group.attrs.create(
                'BinningVertical', self.binning_vertical, dtype='int8')
        if self.named_exposures:
            for i, exposure in enumerate(self.exposures):
                group = image_group.require_group(exposure['name'])
                dset = group.create_dataset(exposure['frametype'], data=self.imgs[i],
                                            dtype='uint16', compression='gzip')
                if self.imageify:
                    # Specify this dataset should be viewed as an image
                    dset.attrs['CLASS'] = np.string_('IMAGE')
                    dset.attrs['IMAGE_VERSION'] = np.string_('1.2')
                    dset.attrs['IMAGE_SUBCLASS'] = np.string_(
                        'IMAGE_GRAYSCALE')
                    dset.attrs['IMAGE_WHITE_IS_ZERO'] = np.uint8(0)
                print('Saved frame {:}'.format(exposure['frametype']))
        else:
            image_group.create_dataset('Raw', data=np.array(self.imgs))