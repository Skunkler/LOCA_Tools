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



inputIMG = arcpy.GetParameterAsText(0)

clipRasterOut = arcpy.GetParameterAsText(1)
threshHoldVal = int(arcpy.GetParameterAsText(2))
model = arcpy.GetParameterAsText(3)
startYear = int(arcpy.GetParameterAsText(4))
endYear = int(arcpy.GetParameterAsText(5))
outputLoc = arcpy.GetParameterAsText(6)
shp = arcpy.GetParameterAsText(7)

mod = model.replace("-","")
inModel = mod.replace(" ", "")


#This function initiates the date decode object and returns it
def Startup(inYear, outYear, IMGFile):
    DateDecodeObj = GetDate(inYear, outYear, IMGFile)
    DateDecodeObj.Main_controller()
    return DateDecodeObj


#calls the yearsFilter class and filters for a specific year
def getAnnualBands(year, DateObj):
    
    YearFilter = YearsFilter(DateObj.DateDict)
    YearFilter.get_a_year(year)
    return YearFilter


#this function converts the user fahrenheit input to celsius
#creates an instance of the text read class and calculates the spatial average
#for the user specified area of interest on a daily time interval
#if the average is greater than the threshold, increase the count variable
#return the count variable
def RasterCalc(monthObj, plantStressVal):
    Celsius = (plantStressVal-32)*(5.0/9.0)
    count = 0
    for i in range(len(monthObj.filteredMonthLst)):
        raster = InRaster + '\\' + monthObj.filteredMonthLst[i]
        print raster
        
        
        ASCIIObj = TextRead()
        ASCIIObj.areaDailyAvg(InRaster + '\\' + monthObj.filteredMonthLst[i], outputLoc)
        if ASCIIObj.avg >= Celsius:
            count += 1
    
    return count


#this function creates a month dictionary
#and a month object
#loop through each month, and build a dictionary that stores the number of days above the threshold to each month
def DailyCountPlantStress(YearDictObj):
    
    MonthDict = dict()
    m = MonthFilter(YearDictObj.filteredDate)
    
    for i in range(1,13):
        
        m.getMonths(i)
        tempRas = RasterCalc(m, threshHoldVal)
        MonthDict[i] = tempRas
    
    return MonthDict

    
        



#if the user's start year is before 2006, initiate the program as historical scenario
#otherwise set it up as a futuristic scenario

if startYear < 2006:
    GlobalDateDecoder = Startup(1950, 2005, inputIMG)
else:
    GlobalDateDecoder = Startup(2006, 2099, inputIMG)

#clip to just the user specified ROI
InRaster = clipRasterOut+ "\\CRas.img"
arcpy.Clip_management(GlobalDateDecoder.ws, "#", InRaster, shp,"0","ClippingGeometry")


#initiate the output csv file
fileOut = open(outputLoc + '\\' + inModel + ".csv", "w")
#write the csv file with the output results
for i in range(startYear, endYear + 1):
    yearObj = getAnnualBands(i, GlobalDateDecoder)
    MonthObj = DailyCountPlantStress(yearObj)
    
    for key in MonthObj.keys():
        fileOut.write(str(i) + ',' + str(key) + ',' + str(MonthObj[key])+'\n')
    
fileOut.close()    

