#This script was written by Warren Kunkler in support of the 2020 LOCA Project
#this script decodes the input raw raster image so that each band is decoded into the correct
#day, month, and year


import math, arcpy
import numpy as np
from arcpy import env

#This class creates an object that stores the decoded band values and associated dates into a dictionary

class GetDate():
    
    non_Leap_year = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    Leap_year = {1:31, 2:29, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    Leap_listVal = list([range(Leap_year[key]) for key in Leap_year.keys()])
    NonLeap_listVal = list([range(non_Leap_year[key]) for key in non_Leap_year.keys()])
    
    #our constructor takes start and end dates along with a specified img ws
    def __init__(self, inDate, outDate,ws):
        
       
        self.inDate = inDate
        self.outDate = outDate + 1
        self.ws = ws
        self.DateDict = dict()


    
    #this private method takes the sublist and yearval list and first creates a two dimensional array consisting of days and months
    #the collapsed list uses numpy to collapse the values into a single array then produces another array of the filtered list
    #then assigns he appropriate values for each band within DateDict
    def __assignDate(self, sublist, YearValList):
        monthVals = [[str(i+1)+ '_' + str(val+1) for val in YearValList[i]] for i in range(12)]
        CollapsedList = list(np.concatenate((monthVals)))

        NewDateList = list(map(lambda x: x + '_' + str(self.inDate), CollapsedList))


        

        
        for i in range(0,len(sublist)):
            
            self.DateDict["\\Layer_" + str(sublist[i])] = NewDateList[i]
            
        
        
        
    #another private method that simply loops through each band within the input raster
    #builds up a list of each band and returns the list
    def __setUpData(self):

       
        Raster = self.ws
        
        bandcount = arcpy.GetRasterProperties_management(Raster, "BANDCOUNT")

        RasterList = [i for i in range(1, int(bandcount.getOutput(0)) + 1)]
        
        
        return RasterList

    #This main method sets up the list of raster bands, and increments the inDate until it equals the outDate
    #next it checks to see in the year is a leap year or not so that it can correctly assign the number of days
    #deletes the first 366 or 365 values thus treating RasList somewhat like a stack
    #in the end the software has a usable date decoded object
    def Main_controller(self):
        
        
        RasList = self.__setUpData()
        while self.inDate < self.outDate:
            if self.inDate%4 == 0 or self.inDate%100 == 0 or self.inDate%400 == 0:
                self.__assignDate(RasList[:366], GetDate.Leap_listVal)
                del RasList[:366]
                self.inDate+= 1
            else:
                self.__assignDate(RasList[:365], GetDate.NonLeap_listVal)
                del RasList[:365]
                self.inDate += 1
        arcpy.AddMessage("Date decoder object constructed")


