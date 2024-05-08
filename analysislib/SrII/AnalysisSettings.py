import numpy as np

Sr = {'sigma0': 1.015*10**(-13), 'mass': 87.906*1.661*10**(-27), 'tau': 5e-9}

camera = {'GH':{'pixel_size': 3.69*10**-6,'sensor_size':  [1928,1448], 'magnification': 0.91, 'quantum_efficiency': 0.68,
                 'losses': 0.61, 'focal_length': 200e-3, 'aperture_diameter': 25e-3}}

ROI = {'small':[650,1350,800,1300],
        'medium':[450,1600,650,1448],
        'large':[300,1800,1,1448]}

filters = {'median': {'small': 3, 'large': 7}, 
           'gaussian': {'small': 3, 'large': 7}, 
           'binning': {'none': 0, 'small': 2, 'medium': 4, 'large': 8}}

result_plot = 'atomNumber'

variable_info = {'BlueMOTShimX': {'plot_title': 'Varying X-axis Shim Current','axis_label': 'Coil current (A)','scale': 1.0},
                 'PulseDuration': {'plot_title': 'Varying X-axis Shim Current','axis_label': 'Probe duration ($\mu$s)','scale': 1000000.0},
                 }