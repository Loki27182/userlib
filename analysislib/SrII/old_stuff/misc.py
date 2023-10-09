from lyse import *
import matplotlib.pyplot as plt
import numpy as np

import AnalysisSettings
import SrConstants

from Subroutines.splice_gaussian_fit_sub import splice_gaussian_fit_sub
from Subroutines.FitFunctions import gauss

ser = data(path)
run = Run(path)

camera = AnalysisSettings.Camera

im_probe = run.get_image(camera, 'absorption', 'probe').astype('float')


x, imageX, pOptX, pCovX, z, imageZ, pOptZ, pCovZ = splice_gaussian_fit_sub(im_probe, False)

fig = plt.figure()
fig.suptitle(pOptX[0], fontsize=70)
ax_image = fig.add_subplot(221)
ax_x = fig.add_subplot(223)
ax_z = fig.add_subplot(222)
ax_image.imshow(im_probe, vmin=min(pOptX[3], pOptX[0]), vmax=max(pOptX[3] + pOptX[0], 0.01))
ax_x.plot(x, imageX)
ax_x.plot(x, gauss(x, *pOptX))
ax_z.plot(z, imageZ)
ax_z.plot(z, gauss(z, *pOptZ))
ax_image.plot(pOptX[1],pOptZ[1],'bo')

print(pOptX[2]*SrConstants.pixelSizeDict[camera])
print(pOptZ[2]*SrConstants.pixelSizeDict[camera])
