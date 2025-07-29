import numpy as np

Sr = {'sigma0': 1.015*10**(-13), 'mass': 87.906*1.661*10**(-27), 'tau': 5e-9}

camera = {'GH':{'pixel_size': 3.69*10**-6,'sensor_size':  [1928,1448], 'magnification': 1.96, 'quantum_efficiency': 0.68,
                 'losses': 0.61, 'focal_length': 200e-3, 'aperture_diameter': 25e-3, 'transpose': True},
        'Flea':{'pixel_size': 2.5*10**-6,'sensor_size':  [2080,1552], 'magnification': 1.0, 'quantum_efficiency': 0.67,
                 'losses': 0.61, 'focal_length': 150e-3, 'aperture_diameter': 25e-3, 'transpose': False},
        'Blackfly':{'pixel_size': 4.5*10**-6,'sensor_size':  [1936,1464], 'magnification': 175.0/150.0, 'quantum_efficiency': 0.67,
                 'losses': 0.34, 'focal_length': 175e-3, 'aperture_diameter': 12e-3, 'transpose': False}}

ROI_GH = {'small':[450,1150,800,1300],
        'medium':[450,1400,650,1448],
        'medium_high':[300,1400,200,1248],
        'small_high':[600,950,825,1000],
        'large':[300,1800,1,1448],
        'full':[1,1927,1,1448],
        'column':[450,1550,800,1445],
        'test':[400,1300,550,1200],
        'red':[780,1075,770,1150],
        'red_small':[850,1000,870,1050],
        'red_tof':[800,1924,551,1325],
        'red_low':[1325,1800,675,1200],
        'dipole':[880,1000,870,1050],
        'dipole2':[880,1000,200,1443],
        'dipole_tof':[880,1900,840,1070],
        'dipole3':[925,1425,700,1175]}
ROI_BF = {'test':[850,1250,550,850]}

filters = {'median': {'small': 1, 'large': 3}, 
           'gaussian': {'small': 1, 'large': 1}, 
           'binning': {'none': 0, 'small': 2, 'medium': 4, 'large': 8}}

result_plot = 'atomNumber'

variable_info = {'BlueMOTShimX': {'plot_title': 'Varying X-axis Shim Current','axis_label': 'X trim current (A)','scale': 1.0, 'prefer_x': 1},
                 'BlueMOTShimZ': {'plot_title': 'Varying Z-axis Shim Current','axis_label': 'Z trim current (A)','scale': 1.0, 'prefer_x': 1},
                 'BlueMOTShimY': {'plot_title': 'Varying Y-axis Shim Current','axis_label': 'Y trim current (A)','scale': 1.0, 'prefer_x': 1},
                 'PulseDuration': {'plot_title': 'Varying Pulse Duration','axis_label': 'Probe duration ($\mu$s)','scale': 1.0e6, 'prefer_x': 1},
                 'ImagingOffset': {'plot_title': 'Varying Imaging Time','axis_label': 'Imaging pulse offset (s)','scale': 1.0, 'prefer_x': 0},
                 'DummyVariable': {'plot_title': 'Repeating','axis_label': 'Dummy variable','scale': 1.0, 'prefer_x': 0},
                 'MagPulseDetuning': {'plot_title': 'Magnetometry','axis_label': 'Field magnitude (mG)','scale': 952.620, 'prefer_x': 0},
                 }

result_info = {'atomNumber': {'axis_label': 'Atom number (millions)','scale': 1.0e-6,'plot_flag':True},
                 'x_position': {'axis_label': 'X-position ($\mu$m)','scale': 1.0,'plot_flag':False},
                 'y_position': {'axis_label': 'Y-position ($\mu$m)','scale': 1.0,'plot_flag':False},
                 'x_width': {'axis_label': 'X-width ($\mu$m)','scale': 1.0,'plot_flag':False},
                 'y_width': {'axis_label': 'Y-width ($\mu$m)','scale': 1.0,'plot_flag':False},
                 }