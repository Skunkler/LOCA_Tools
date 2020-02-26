#This script was written by Warren Kunkler in support of the 2020 LOCA project
#This script takes input from the user to calculate the min and max of temperature data

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
output_gdb = arcpy.GetParameterAsText(1)
rastersOut = arcpy.GetParameterAsText(2)
inYear = int(arcpy.GetParameterAsText(3))
outYear = int(arcpy.GetParameterAsText(4))
shp = arcpy.GetParameterAsText(5)


#This checks to see in the input is tasmax or tasmin and names the inputVal param accordingly
if inputIMG.split("\\")[-1][:-4] == "tasmax":
    inputVal = "max"
elif inputIMG.split("\\")[-1][:-4] == "tasmin":
    inputVal = "min"


env.workspace = rastersOut

env.overwriteOutput = True


#This function initiates the date decode object and returns it
def Startup(inYear, outYear, IMGFile, output):
    DateDecodeObj = GetDate(inYear, outYear, IMGFile)
    DateDecodeObj.Main_controller()
    
    return DateDecodeObj


#This function filters for the appropriate bands that correspond to a specified year
def getAnnualBands(year, DateObj):
    
    YearFilter = YearsFilter(DateObj.DateDict)
    YearFilter.get_a_year(year)
    return YearFilter

#this function calculates both the minimum and maximum of the input image and saves the results
def RasterStats(filteredDates, save_location, DateDecodeObj,year,TempVar):
    RasterList = [DateDecodeObj.ws + '\\' + i for i in filteredDates.filteredDateList]
    Mincalc = arcpy.sa.CellStatistics(RasterList, statistics_type = "MINIMUM")
    Mincalc.save(save_location + '\\' + DateDecodeObj.ws.split('\\')[-1][:-4] + '_' + TempVar + '_Min_' +str(year)+'.img')
    MaxCalc = arcpy.sa.CellStatistics(RasterList, statistics_type = "MAXIMUM")
    MaxCalc.save(save_location+'\\' + DateDecodeObj.ws.split('\\')[-1][:-4] + '_' + TempVar + '_Max_' + str(year) + '.img')

#this function creates a Global date decoder object that can be used throughout the program
def LaunchStart(TempVar):
    TempType = TempVar
    if inYear >= 2006:
        GlobalDateDecode = Startup(2006, 2099, inputIMG, rastersOut)
    else:
        GlobalDateDecode = Startup(1950, 2005, inputIMG, rastersOut)

    #this loop grabs the specifed year and calculates statistics for the bands that correspond to that year
    for i in range(inYear, outYear+1):
        ListYear = getAnnualBands(i, GlobalDateDecode)
        RasterStats(ListYear, rastersOut, GlobalDateDecode, i, TempType)


#This function calculates zonal statistics as a table for each output raster
def ZonalStats(tempVar):
    rasters = arcpy.ListRasters()
    arcpy.MakeFeatureLayer_management(shp, "lyr")

    for raster in rasters:
        outstats = ZonalStatisticsAsTable("lyr", "Id", raster, output_gdb + '\\' + raster[:-4], "NODATA", "ALL")

    env.workspace = output_gdb
    tables = arcpy.ListTables()
    maxTableLst = []
    minTableLst = []

    #loop through each table, and append only the appropriate tables to each table list
    for table in tables:
        print table
        arcpy.AddField_management(table, "Year", "TEXT")
        arcpy.CalculateField_management(table,"Year", table.split('_')[-1], "PYTHON_9.3")
        if table.split('_')[-1] != str(inYear) and '_Min_' in table:
            minTableLst.append(table)
        elif table.split('_')[-1] != str(inYear) and "_Max_" in table:
            maxTableLst.append(table)
            

    #append the appropriate tables to each other
    if len(minTableLst) > 0:
        arcpy.Append_management(minTableLst, table.split('_')[0] + "_" + tempVar + "_Min_" + str(inYear), "NO_TEST")
        arcpy.AddMessage("completed calculations, please see final data in " + table.split('_')[0] + "_" + tempVar + "_Min_" + str(inYear) + " at " + output_gdb)
    if len(maxTableLst) > 0:
        arcpy.Append_management(maxTableLst, table.split('_')[0] + "_" + tempVar + "_Max_" + str(inYear), "NO_TEST")
        arcpy.AddMessage("completed calculations, please see final data in " + table.split('_')[0] + "_" + tempVar + "_Max_" + str(inYear) + " at " + output_gdb)
    else:
        arcpy.AddMessage("Error: there were no associated tables, check that naming convention adheres to somthing like 'TMAX_Min'")









#these simple statements launch the program based on user input
if inputVal.lower() == "min":
    TempType = "TMIN"
    LaunchStart(TempType)
    ZonalStats(TempType)

        
        
elif inputVal.lower() == "max":
    TempType = "TMAX"
    LaunchStart(TempType)
    ZonalStats(TempType)

        
else:
    arcpy.AddMessage("error, please check the values you entered")
    
    



        

