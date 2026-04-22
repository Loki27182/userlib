import numpy as np

Sr = {'sigma0': 1.015*10**(-13), 'mass': 87.906*1.661*10**(-27), 'tau': 5e-9}

camera = {'GH':{'pixel_size': 3.69*10**-6,'sensor_size':  [1928,1448], 'magnification': 1.96, 'quantum_efficiency': 0.68,
                 'losses': 0.61, 'focal_length': 200e-3, 'aperture_diameter': 25e-3, 'transpose': False, 'rotate': 3},
        'Flea':{'pixel_size': 2.5*10**-6,'sensor_size':  [2080,1552], 'magnification': 1.0, 'quantum_efficiency': 0.67,
                 'losses': 0.61, 'focal_length': 150e-3, 'aperture_diameter': 25e-3, 'transpose': False, 'rotate': 0},
        'Blackfly':{'pixel_size': 4.5*10**-6,'sensor_size':  [1936,1464], 'magnification': 175.0/150.0, 'quantum_efficiency': 0.67,
                 'losses': 0.34, 'focal_length': 175e-3, 'aperture_diameter': 12e-3, 'transpose': False, 'rotate': 1}}

ROI_GH = {'small':[450,1150,800,1300],
        'medium':[450,1400,650,1448],
        'medium_high':[300,1400,200,1248],
        'small_high':[600,950,825,1000],
        'large':[600,1900,0,1200],
        'full':[1,1927,1,1448],
        'column':[1000,1924,200,750],
        'test':[400,1300,550,1200],
        'red':[1000,1500,100,900],
        'red_small':[1100,1400,200,700],
        'red_large':[700,1800,0,1000],
        'red_tof':[1500,1900,100,900],
        'red_low':[1325,1800,675,1200],
        'dipole':[1100,1300,0,1448],
        'dipole_mag':[1100,1300,250,700],
        'dipole_sideband':[1155,1245,350,625],
        'dipole_low':[1400,1850,700,1300],
        'dipole_long':[1100,1350,0,1000],
        'dipole_short':[1100,1350,250,690],
        'dipole2':[880,1000,200,1443],
        'dipole_tof':[1500,1924,700,1200],
        'dipole3':[925,1425,700,1175]}
ROI_BF = {'test':[0,1935,0,1463],
          'red':[835,1335,550,1150],
          'dipole_sideband':[985,1185,775,975]}

filters = {'median': {'small': 1, 'large': 3}, 
           'gaussian': {'small': 1, 'large': 2}, 
           'binning': {'none': 0, 'small': 2, 'medium': 4, 'large': 8},
           '2D': {'small': 0}}

result_plot = 'atomNumber'

variable_info = {'BlueMOTShimX': {'plot_title': 'Varying X-axis Shim Current','axis_label': 'X trim current (A)','scale': 1.0, 'prefer_x': 1},
                 'BlueMOTShimZ': {'plot_title': 'Varying Z-axis Shim Current','axis_label': 'Z trim current (A)','scale': 1.0, 'prefer_x': 1},
                 'BlueMOTShimY': {'plot_title': 'Varying Y-axis Shim Current','axis_label': 'Y trim current (A)','scale': 1.0, 'prefer_x': 1},
                 'PulseDuration': {'plot_title': 'Varying Pulse Duration','axis_label': 'Probe duration ($\mu$s)','scale': 1.0e6, 'prefer_x': 1},
                 'ImagingOffset': {'plot_title': 'Varying Imaging Time','axis_label': 'Imaging pulse offset (s)','scale': 1.0, 'prefer_x': 0},
                 'DummyVariable': {'plot_title': 'Repeating','axis_label': 'Dummy variable','scale': 1.0, 'prefer_x': 0},
                 #'MagPulseDetuning': {'plot_title': 'Magnetometry','axis_label': 'Field magnitude (mG)','scale': 952.620, 'prefer_x': 0},
                 'MagPulseDetuning': {'plot_title': 'Magnetometry','axis_label': 'Detuning (MHz)','scale': 1, 'prefer_x': 0},
                 }

result_info = {'atomNumber': {'axis_label': 'Atom number (millions)','scale': 1.0e-6,'plot_flag':True},
                 'x_position': {'axis_label': 'X-position ($\mu$m)','scale': 1.0e6,'plot_flag':False},
                 'y_position': {'axis_label': 'Y-position ($\mu$m)','scale': 1.0e6,'plot_flag':False},
                 'x_width': {'axis_label': 'X-width ($\mu$m)','scale': 1.0e6,'plot_flag':False},
                 'y_width': {'axis_label': 'Y-width ($\mu$m)','scale': 1.0e6,'plot_flag':False},
                 'x_fit_N': {'axis_label': 'Atom number (arb - from x-fit)','scale': 1.0,'plot_flag':False},
                 'y_fit_N': {'axis_label': 'Atom number (arb - from y-fit)','scale': 1.0,'plot_flag':False},
                 'fit_N': {'axis_label': 'Atom number (arb - from y-fit)','scale': 1.0e0,'plot_flag':False},
                 }