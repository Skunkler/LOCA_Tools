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
rastersOut = arcpy.GetParameterAsText(1)
output_gdb = arcpy.GetParameterAsText(2)
inYear = int(arcpy.GetParameterAsText(3))
outYear = int(arcpy.GetParameterAsText(4))
shp = arcpy.GetParameterAsText(5)

#set up workspace based on user input
env.workspace = rastersOut

env.overwriteOutput = True


#This function initiates the date decode object and calls the AnnualAverageCall() function at the end
#and inputs the parameters from the user and the date decode object
def Startup(startYear, finalYear, IMGFile, output):
    DateDecodeObj = GetDate(startYear, finalYear, IMGFile)
    DateDecodeObj.Main_controller()
    
    AnnualAverageCall(inYear, outYear, DateDecodeObj, output)
    

#builds up a list of raster bands that correspond to a specified year
#calls the cellstatistics method from arcpy spatial analyst
#saves the output raster to a specified location
def RasterStats(filteredDates, save_location, DateDecodeObj,year):
    RasterList = [DateDecodeObj.ws + '\\' + i for i in filteredDates.filteredDateList]
    calc = arcpy.sa.CellStatistics(RasterList, statistics_type = "SUM")
    calc.save(save_location + '\\' + DateDecodeObj.ws.split('\\')[-1][:-4] + '_' +str(year)+'.img')


#calls the yearsFilter class and filters for a specific year
def getAnnualBands(year, DateObj):
    
    YearFilter = YearsFilter(DateObj.DateDict)
    YearFilter.get_a_year(year)
    return YearFilter

#This function loops through the years of interest as specified by the user
#returns each filtered year based on the year filter and date decode objects
#then it calculates the statistics with the RasterStats function
def AnnualAverageCall(inputYear, outputYear, DateObj, output):
    for i in range(inputYear, outputYear+1):
        ListYear = getAnnualBands(i, DateObj)
        
        RasterStats(ListYear, output, DateObj,i)        


#if the user's start year is before 2006, initiate the program as historical scenario
#otherwise set it up as a futuristic scenario
if inYear >= 2006:
    Startup(2006, 2099, inputIMG, rastersOut)
else:
    Startup(1950, 2005, inputIMG, rastersOut)


#list all rasters that are outputted from RasterStats() and run zonal statistics as table
#on all of them and save the results to output_gdb
rasters = arcpy.ListRasters()
arcpy.MakeFeatureLayer_management(shp, "lyr")

for raster in rasters:
    outstats = ZonalStatisticsAsTable("lyr", "Id", raster, output_gdb + '\\' + raster[:-4], "NODATA", "ALL")

#change the workspace environment to output_gdb and now loop through
#all tables adding and calculating the year field in each, add all but the first
#table to the tables list so that it can later be appended onto the first table


env.workspace = output_gdb
tables = arcpy.ListTables()
Tables_List = []

for table in tables:
    print table
    arcpy.AddField_management(table, "Year", "TEXT")
    arcpy.CalculateField_management(table,"Year", table.split('_')[1], "PYTHON_9.3")
    if table != table.split('_')[0] +"_"+ str(inYear):
        Tables_List.append(table)


if len(Tables_List) != 0:
    arcpy.Append_management(Tables_List, table.split('_')[0] + "_" + str(inYear), "NO_TEST")
    arcpy.AddMessage("calculations are complete, please see " + table.split("_")[0] + "_" + str(inYear) + " in " output_gdb + " to see final results.")
else:
    arcpy.AddMessage("calculations are complete, please see " + table.split("_")[0] + "_" + str(inYear) + " in " output_gdb + " to see final results.")
