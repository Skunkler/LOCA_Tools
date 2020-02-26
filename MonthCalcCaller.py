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
outputLoc = arcpy.GetParameterAsText(1)
output_gdb = arcpy.GetParameterAsText(2)
startYear = int(arcpy.GetParameterAsText(3))
endYear = int(arcpy.GetParameterAsText(4))
startMonth = int(arcpy.GetParameterAsText(5))
endMonth = int(arcpy.GetParameterAsText(6))
inModel = arcpy.GetParameterAsText(7)
shp = arcpy.GetParameterAsText(8)

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



#builds up a list of raster bands that correspond to a specified year and month
#calls the cellstatistics method from arcpy spatial analyst
#saves the output raster to a specified location

def RasterStats(filteredDates, save_location, DateObj):
    RasterList = [DateObj.ws + '\\' + i for i in filteredDates.filteredMonthLst]
    calc = arcpy.sa.CellStatistics(RasterList, statistics_type = "MEAN")
    calc.save(save_location)





#if the user's start year is before 2006, initiate the program as historical scenario
#otherwise set it up as a futuristic scenario

if startYear < 2006:
    GlobalDateObj = Startup(1950, 2005, inputIMG)
else:
    GlobalDateObj = Startup(2006, 2099, inputIMG)


#Launches the calculation on each band of the input raster and outputs the calculated rasters
monthList = []
for i in range(startYear, endYear+1):
    year = getAnnualBands(i, GlobalDateObj)
    
    for x in range(startMonth, endMonth+1):
        month = MonthFilter(year.filteredDate)
        month.getMonths(x)
        RasterStats(month, outputLoc + '\\' + inModel + "_" + str(i) + "_" + str(x) + ".img", GlobalDateObj)


#change workspace to the location of the calculated rasters
env.workspace = outputLoc        
rasters = arcpy.ListRasters()
arcpy.MakeFeatureLayer_management(shp, "lyr")

#loop through each raster and run zonal statistics
for raster in rasters:
    rasName = raster.replace("-", "")
    outstats = ZonalStatisticsAsTable("lyr", "Id", raster, output_gdb + '\\' + rasName[:-4], "NODATA", "ALL")


#change workspace to the output zonal statistics tables
env.workspace = output_gdb
env.overwriteOutput = True
tables = arcpy.ListTables()
Tables_List = []


#loop through each table and add and calculate both the year and month fields
for table in tables:
    arcpy.AddField_management(table, "Year", "TEXT")
    arcpy.AddField_management(table, "Month", "TEXT")
    arcpy.CalculateField_management(table,"Year", table.split('_')[1], "PYTHON_9.3")
    arcpy.CalculateField_management(table, "Month", table.split("_")[2], "PYTHON_9.3")
    
    if table != table.split("_")[0] + "_" + str(startYear) + "_" + str(startMonth):
        Tables_List.append(table)


#if the Tables_List var is not empty, append all appropiate tables together
if len(Tables_List) != 0:
    arcpy.AddMessage("appending all tables to " + table.split("_")[0] + "_" + str(startYear) + "_" + str(startMonth))
    arcpy.Append_management(Tables_List, table.split("_")[0] + "_" + str(startYear) + "_"+ str(startMonth), "NO_TEST")
else:
    arcpy.AddMessage("Calculations complete, check results in " + table.split("_")[0] + "_" + str(startYear) + "_"+ str(startMonth) + " in " + output_gdb)
            
