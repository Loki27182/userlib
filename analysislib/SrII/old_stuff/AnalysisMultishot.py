from lyse import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import scipy.constants as constants
import AnalysisSettings
import SrConstants
from Subroutines.FitFunctions import gauss
from scipy import stats


camera = AnalysisSettings.Camera
pixelSize = SrConstants.pixelSizeDict[camera]

name = "Different_Loading_Curves_20_02_04"
path = "C:\\Experiments\\example_experiment\\grating_MOT\\AnalysisData\\" + name + ".h5"
run = Run(path)
df = data()

sequence_index = df["sequence_index"]
run_number = df["run number"]
filepath = df["filepath"]
norms = df['FitMOTLoad','fluorNorm']
BlueMOTLoadTime = df['BlueMOTLoadTime']
BlueMOTBeatnote = df['BlueMOTBeatnote']
BlueMOTPower_V = df['BlueMOTPower']
atomNumber = df["splice_gaussian_fit","atomNumber"]
loadingTimeConstant = df["FitMOTLoad", "loadingTimeConstant"]
loadingRate = df["FitMOTLoad", "loadingRate"]
widthX = df["splice_gaussian_fit","widthX"]
widthZ = df["splice_gaussian_fit","widthZ"]
TimeOfFlight = df["TimeOfFlight"]
avgWidth = df["splice_gaussian_fit","avgWidth"]
avgPeakOD = df["splice_gaussian_fit","avgPeakOD"]
avgNorm = 0.04
normFlrNum = loadingRate * loadingTimeConstant * avgNorm/ norms
avgNormRate = loadingRate * avgNorm / norms
SourceCurrent = df["SourceCurrent"]
runtime = df["run time"]

fluorCounts = []
fluorCountsCulled = range(len(filepath))
time = range(len(filepath))
timeCulled = range(len(filepath))

i = 0
for file in filepath:
    fluorCounts.append(np.zeros(1))
    with h5py.File(file,'a') as f:
        for result in f['results']['FitMOTLoad']['atomNummbers']:
            np.append(fluorCounts[i],result)
    i+= 1
print(fluorCounts)

FluorCounts = df["FitMOTLoad","atomNummbers"]
FluorCountsCulled = df["FitMOTLoad","atomNummbersCulled"]
time = df["FitMOTLoad", "time"]
timeCulled = df["FitMOTLoad", "timeCulled"]

def parabola(v,a,b,c):
    return a*(v-c)**2 +b

power_params = [-758.105, 92.576, 4.087]

gaussianWidth = 0.00914
Isat = 403
BlueMOTPower_mW = parabola(BlueMOTPower_V, *power_params)
I_Isat = (BlueMOTPower_mW*(10**-3)/(np.pi*gaussianWidth**2))/Isat

#Do Calculations

pOpt, pCov = curve_fit(gauss, BlueMOTBeatnote, atomNumber, p0 = (1000, 95, 10, 0))

PeakBeatnote = pOpt[1]

Detuning = BlueMOTBeatnote - PeakBeatnote

linewidth = 30.5

# SourceCurrentSing = [12,12.5,13,13.5,14]
DetuningSing = []
normFlrNumSing = []
normFlrNumSingDev =[]
#
for beatnote in Detuning:
    if beatnote not in DetuningSing:
        DetuningSing.append(beatnote)
#
#
atomNumberSing = []
atomNumberSingDev =[]
normTauSing = []
normTauSingDev =[]
normRateSing = []
normRateSingDev = []
#
for beatnote in DetuningSing:
    points1 = []
    #points2 = []
    #points3 = []
    for i in range(len(run_number)):
        if Detuning[i] == beatnote:
            points1.append(atomNumber[i])
            # points2.append(avgNormRate[i])
            # points3.append(normFlrNum[i])
    atomNumberSing.append(np.average(points1))
    atomNumberSingDev.append(stats.sem(points1))
    # normRateSing.append(np.average(points2))
    # normRateSingDev.append(np.std(points2))
    # normFlrNumSing.append(np.average(points3))
    # normFlrNumSingDev.append(np.std(points3))


corAtomNumberSing = np.array(atomNumberSing) * 1/(1 + 4*(np.array(DetuningSing)/linewidth)**2)
corAtomNumberSingDev = np.array(atomNumberSingDev) * 1/(1 + 4*(np.array(DetuningSing)/linewidth)**2)

# fig, ax1 = plt.subplots(1)
# #plot = ax.errorbar(BlueMOTPower_V, normFlrNum, fmt = 'bo', label = 'norms')
# #plot = plt.scatter(SourceCurrent, loadingTimeConstant)
# ax1.errorbar(DetuningSing, atomNumberSing, yerr = atomNumberSingDev,fmt = 'bo')
# ax1.errorbar(DetuningSing, corAtomNumberSing, yerr = corAtomNumberSingDev,fmt = 'go')
# ax1.plot(np.linspace(-18,9,100), gauss(np.linspace(-18,9,100) + PeakBeatnote,*pOpt), 'r-')

run.save_result('norms',norms)
run.save_result('atomNumber', atomNumber)
run.save_result("loadingRate", loadingRate)
run.save_result("loadingTimeConstant", loadingTimeConstant)
run.save_result("avgWidth", avgWidth)
run.save_result("avgPeakOD", avgPeakOD)
run.save_result("avgNorm", np.average(norms))
run.save_result("TimeOfFlight", TimeOfFlight)
run.save_result("widthX", widthX)
run.save_result("widthZ", widthZ)
run.save_result("FluorCounts",FluorCounts)
run.save_result("FluorCountsCulled", FluorCountsCulled)
run.save_result("time", time)
run.save_result("timeCulled", timeCulled)
#run.save_result("BlueMOTPower_V", BlueMOTPower_V)
# run.save_result("Detuning", Detuning)
# run.save_result("DetuningSing", DetuningSing)
# run.save_result("corAtomNumberSing", corAtomNumberSing)
# run.save_result("corAtomNumberSingDev",corAtomNumberSingDev)
# run.save_result("PeakBeatnote" ,PeakBeatnote)
# run.save_result("linewidth", linewidth)
# run.save_result("atomNumberSing",atomNumberSing)
# run.save_result("atomNumberSingDev",atomNumberSingDev)
# run.save_result("SourceCurrent", SourceCurrent)
run.save_result("normFlrNum", normFlrNum)
#run.save_result("normFlrNumSing", normFlrNumSing)
#run.save_result("normFlrNumSingDev", normFlrNumSingDev)
#run.save_result("normTauSing", normTauSing)
#run.save_result("normTauSingDev", normTauSingDev)
#run.save_result("normRateSing", normRateSing)
#run.save_result("normRateSingDev", normRateSingDev)
#run.save_result("SourceCurrentSing", SourceCurrentSing)
# run.save_result("gaussianWidth", gaussianWidth)
# run.save_result("Isat", Isat)
# run.save_result("BlueMOTPower_mW", BlueMOTPower_mW)
# run.save_result("I_Isat", I_Isat)
# run.save_result("avgNormRate", avgNormRate)
# run.save_result("avgNorm", avgNorm)

files = []
for i in range(len(sequence_index)):
    files.append(str(sequence_index[i]) + '_' + str(run_number[i]))
    run.save_result("files", files)
run.save_result("filepath", filepath)
