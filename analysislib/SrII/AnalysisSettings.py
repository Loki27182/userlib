import numpy as np

Sr = {'sigma0': 1.015*10**(-13), 'mass': 87.906*1.661*10**(-27)}

camera = {'GH':{'pixel_size': 3.69*10**-6,'sensor_size':  [1928,1448]}}

ROI = {'small':[700,1300,800,1300],
        'large':[200,1800,300,1448]}

filters = {'median': {'small': 3, 'large': 7}, 
           'gaussian': {'small': 3, 'large': 7}, 
           'binning': {'none': 0, 'small': 2, 'medium': 4, 'large': 8}}

