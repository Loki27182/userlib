from lyse import *
import numpy as np

ser = data(path)
run = Run(path)

absorptionWidthX = ser["splice_gaussian_fit", "widthX"]
absorptionWidthZ = ser["splice_gaussian_fit", "widthZ"]
fluorescenceWidthX = run.get_result_array("FitMOTLoad","widthsX")[-1]
fluorescenceWidthZ = run.get_result_array("FitMOTLoad","widthsZ")[-1]

widthRatioX = absorptionWidthX/fluorescenceWidthX
widthRatioZ = absorptionWidthZ/fluorescenceWidthZ

print("widthRaioX = " + str(widthRatioX))
print("widthRaioZ = " + str(widthRatioZ))

run.save_result("widthRatioX", widthRatioX)
run.save_result("widthRatioZ", widthRatioZ)
