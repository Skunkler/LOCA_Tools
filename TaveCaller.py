#This script was written by Warren Kunkler in support of the 2020 LOCA Project
#This is the script that calls the objects from other scripts such as AnnualAvg and DateAssignment
#This takes user input, and calculates the necessary data products from the raw daily data



import math, arcpy
import numpy as np
from arcpy import env
from arcpy.sa import *
from AnnualAvg import AvgTable
from AnnualAvg import YearsFilter
from AnnualAvg import MonthFilter
from DateAssignment import GetDate
from TextRead import TextRead
arcpy.CheckOutExtension("Spatial")


tasminRaw = arcpy.GetParameterAsText(0)
tasmaxRaw = arcpy.GetParameterAsText(1)
outputLoc = arcpy.GetParameterAsText(2)
Model = arcpy.GetParameterAsText(5)
startYear = int(arcpy.GetParameterAsText(3))
endYear = int(arcpy.GetParameterAsText(4))

Mod = Model.replace("-","")

inModel = Mod.replace(" ","")

#calls the yearsFilter class and filters for a specific year
def getAnnualBands(year, DateObj):
    
    YearFilter = YearsFilter(DateObj.DateDict)
    YearFilter.get_a_year(year)
    return YearFilter


#This function uses the raster object to access both input tasmin and tasmax rasters from
#appropriate years to calculate the daily TAVE and stack each back together
def TaveDaily(rasterObj, rasterObj2, output, DateDecodeObj, DateDecodeObj2):
    inputList = []
    
    listRas = rasterObj.filteredDateList
    listRas.sort()
    for i in range(len(listRas)):
        raster1 = DateDecodeObj.ws + '\\' + listRas[i]
        raster2 = DateDecodeObj2.ws + '\\' + listRas[i]

        outraster = (Raster(raster1) + Raster(raster2)) / 2
        inputList.append(outraster)
        

    arcpy.CompositeBands_management(inputList, output)
    

#This function initiates the date decode object and returns it
def Startup(inYear, outYear, IMGFile):
    DateDecodeObj = GetDate(inYear, outYear, IMGFile)
    DateDecodeObj.Main_controller()
    return DateDecodeObj



#if the user's start year is before 2006, initiate the program as historical scenario
#otherwise set it up as a futuristic scenario

if startYear < 2006:
    TasminDateDecodeObj = Startup(1950, 2005, tasminRaw)
    TasmaxDateDecodeObj = Startup(1950, 2005, tasmaxRaw)
else:
    TasminDateDecodeObj = Startup(2006, 2099, tasminRaw)
    TasmaxDateDecodeObj = Startup(2006, 2099, tasmaxRaw)


#Launches the calculation on each band of the input raster and outputs the calculated rasters
for i in range(startYear, endYear+1):
    RasterYear = getAnnualBands(i,TasminDateDecodeObj)
    Raster2Year = getAnnualBands(i, TasmaxDateDecodeObj)
    TaveDaily(RasterYear, Raster2Year, outputLoc + '\\' + inModel + "_" + str(i)+ "_TAVE.img", \
              TasminDateDecodeObj, TasmaxDateDecodeObj)

    arcpy.AddMessage("finished calculating TAVE for " + str(i) + " final dataset located here: " + outputLoc + '\\' + inModel + "_" + str(i)+ "_TAVE.img")


