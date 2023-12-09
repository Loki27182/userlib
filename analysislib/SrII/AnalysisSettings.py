"""This is a place for all the things we change on a day to day basis"""
import Subroutines.FitFunctions as Functions

# Multi-script variables
Camera = 'horizontal'
Isotope = 88

# Single-Script variables

# single_gaussian_analysis parameters
#SGROI = [00,1600,0,1200]
SGROI = [25,-25,25,-25]
SGMedFilterWidth = 11
SGGaussFilterWidth = 5

dfdV = 41.63

# ParameterOptimization:
#POIndependentVar = "PixisBrightTime"
#POMiscDependentVar1 = ("DisplayImage", "avg_count")
#POMiscDependentVar2 = ("DisplayImage", "avg_count")
#POFitFunction = Functions.temp_fit
#POFitParameters = [0,0]
#PONumPoints =15

#FitMOTLoad settings:
#FMLMaxCull = 1e10
#FMLMinCull = 1e5
#FMLBadShots = [0]

#BlueMOTBeatnote
#RepumpFreq1
#RepumpFreq2
#RepumpFreq3
#RepumpFreq4
#RepumpAmp1
#RepumpAmp2
#RepumpAmp3
#RepumpAmp4
