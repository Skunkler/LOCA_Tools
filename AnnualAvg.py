#This script was written by Warren Kunkler in support of the 2020 LOCA project
#This script composes three different classes which are used to filter out which bands from the
#The input raster files correspond to user specified and year and month ranges

import math, arcpy
import numpy as np
from arcpy import env
from arcpy.sa import *



arcpy.CheckOutExtension("Spatial")



"""class AvgTable():

    
    def __init__(self, rasterImg, boundaryShp, county):
        self.raster=rasterImg
        self.boundary = boundaryShp
        self.county = county

    def CalcZonalStats(self, outputLoc):
        env.workspace = outputLoc
        env.overwriteOutput = True
        try:
            arcpy.MakeFeatureLayer_management(self.boundary, "shplyr", "STNAME = 'Nevada' AND COUNTY = '{}'".format(self.county))
            outStats = ZonalStatisticsAsTable("shplyr", "COUNTY", self.raster, outputLoc, "NODATA", "MEAN") 
            arcpy.AddMessage("complete calculating zonal stats")
        except:
            ouch = arcpy.GetMessages(2)
            arcpy.AddMessage(ouch)"""

#The years filter class creates an object with a dictionary containing which bands in the file correspond to a specified year

class YearsFilter():

    def __init__(self,DataDict):
        self.Dictionary = DataDict

    
    def get_mult_years(self, yearStart, yearEnd ):
        
        self.filteredDates = dict(filter(lambda DataDict: int(DataDict[1].split('_')[-1]) >= yearStart or int(DataDict[1].split('_')[-1]) <= yearEnd, self.Dictionary.items()))
        self.filteredDatesList = self.filteredDates.keys()                                                                                                      


    def get_a_year(self, yearVal):
        self.filteredDate = dict(filter(lambda DataDict: int(DataDict[1].split('_')[-1]) == yearVal, self.Dictionary.items()))
        self.filteredDateList = self.filteredDate.keys()
        

#The month filter class creates an object with a dictionary containing which bands in the file correspond to a specified month
class MonthFilter():
    def __init__(self, inputDict):
        self.DataDict = inputDict
        
    def getMonths(self, MonthVal):
        filteredMonth = dict(filter(lambda DataDict: int(DataDict[1].split('_')[0]) == MonthVal, self.DataDict.items()))
        self.filteredMonthLst = filteredMonth.keys()


