import numpy as np

Sr = {'sigma0': 1.015*10**(-13), 'mass': 87.906*1.661*10**(-27), 'tau': 5e-9}

camera = {'GH':{'pixel_size': 3.69*10**-6,'sensor_size':  [1928,1448], 'magnification': 0.91, 'quantum_efficiency': 0.68,
                 'losses': 0.61, 'focal_length': 200e-3, 'aperture_diameter': 25e-3},
        'Flea':{'pixel_size': 2.5*10**-6,'sensor_size':  [2080,1552], 'magnification': 1.0, 'quantum_efficiency': 0.67,
                 'losses': 0.61, 'focal_length': 150e-3, 'aperture_diameter': 25e-3},
        'Blackfly':{'pixel_size': 4.5*10**-6,'sensor_size':  [1936,1464], 'magnification': 1.0, 'quantum_efficiency': 0.67,
                 'losses': 0.61, 'focal_length': 175e-3, 'aperture_diameter': 12e-3}}

ROI_GH = {'small':[450,1150,800,1300],
        'medium':[450,1600,650,1448],
        'medium_high':[300,1400,200,1248],
        'small_high':[550,1050,650,1050],
        'large':[300,1800,1,1448],
        'full':[1,1927,1,1448],
        'column':[450,1150,800,1448]}
ROI_BF = {}

filters = {'median': {'small': 3, 'large': 7}, 
           'gaussian': {'small': 3, 'large': 7}, 
           'binning': {'none': 0, 'small': 2, 'medium': 4, 'large': 8}}

result_plot = 'atomNumber'

variable_info = {'BlueMOTShimX': {'plot_title': 'Varying X-axis Shim Current','axis_label': 'X Coil current (A)','scale': 1.0},
                 'BlueMOTShimY': {'plot_title': 'Varying X-axis Shim Current','axis_label': 'Y Coil current (A)','scale': 1.0},
                 'BlueMOTShimZ': {'plot_title': 'Varying X-axis Shim Current','axis_label': 'Z Coil current (A)','scale': 1.0},
                 'PulseDuration': {'plot_title': 'Varying X-axis Shim Current','axis_label': 'Probe duration ($\mu$s)','scale': 1000000.0},
                 }