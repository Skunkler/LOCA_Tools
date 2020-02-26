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



def Startup(inYear, OutYear, IMGFile, IMGFile2=None):
    DateDecodeObj = GetDate(InYear, OutYear, IMGFile)
    DateDecodeObj.Main_controller()
    if IMGFile2 != None:
        DateDecodeObj2 = GetDate(inYear, OutYear, IMGFile2)
        DateDecodeObj2.Main_controller()
        return (DateDecodeObj,DateDecodeObj2)

    return (DateDecodeObj)

    
    
    

shp = r"D:\LoCA_Project\new\Boundary\ClarkCountyCalAdapt3.shp"


"""def getAnnualAverages(startYear, endYear):
    YearFilter = YearsFilter(DateDecodeObj.DateDict)
    YearFilter.get_mult_years(startYear, endYear)
    return YearFilter"""


    
def RasterStats(filteredDates, save_location):
    RasterList = [DateDecodeObj.ws + '\\' + i for i in filteredDates.filteredMonthLst]
    calc = arcpy.sa.CellStatistics(RasterList, statistics_type = "MEAN")
    calc.save(save_location)
    
    

def getAnnualBands(year, DateObj):
    
    YearFilter = YearsFilter(DateObj.DateDict)
    YearFilter.get_a_year(year)
    return YearFilter



def RasterCalc(monthObj, plantStressVal):
    Celsius = (plantStressVal-32)*(5.0/9.0)
    count = 0
    
    for i in range(len(monthObj.filteredMonthLst)):
        raster = DateDecodeObj.ws + '\\' + monthObj.filteredMonthLst[i]
        print raster
        ASCIIObj = TextRead()
        ASCIIObj.areaDailyAvg(raster)
        if ASCIIObj.avg >= Celsius:
            count += 1
    
    return count

def TaveDaily(rasterObj, rasterObj2, output):
    inputList = []
    
    listRas = rasterObj.filteredDateList
    listRas.sort()
    for i in range(len(listRas)):
        raster1 = DateDecodeObj.ws + '\\' + listRas[i]
        raster2 = DateDecodeObj2.ws + '\\' + listRas[i]

        outraster = (Raster(raster1) + Raster(raster2)) / 2
        inputList.append(outraster)
        print("done processing")

    arcpy.CompositeBands_management(inputList, output + "\\Tave_comp2.img")






yearsObj = {}
def DailyCountPlantStress(YearDictObj):
    
    MonthDict = dict()
    m = MonthFilter(YearDictObj.filteredDate)
    m.getMonths(8)
    MonthDict[6] = RasterCalc(m, 101)
    
    """for i in range(1,13):
        m = MonthFilter(YearDictObj.filteredDate)
        m.getMonths(i)
        tempRas = RasterCalc(m, 86)
        MonthDict[i] = tempRas"""

    print MonthDict
        
        
       
    
def callTave():
    
    RasterYear = getAnnualBands(1970, DateDecodeObj)
    Raster2Year = getAnnualBands(1970, DateDecodeObj2)

    TaveDaily(RasterYear, Raster2Year, r"D:\LoCA_Project\new\CNRMCM5")
    
    

callTave()





#MonthsList = []
for i in range(1951, 1960):
    
    
    ListYear = getAnnualAvg(i)
    m = MonthFilter(ListYear.filteredDate)
    m.getMonths(11)
    MonthsList.append(m)
    


for i in range(len(MonthsList)):
    startVal = 1951
    print startVal + i
    RasterStats(MonthsList[i], "D:\\LoCA_Project\\new\\CNRMCM5\\historic\\MonthAvg_test\\CNRMCM5_"+str(startVal + i)+".img")


"""for i in range(1951, 1960):
    print i
    FilteredDictionary = getAnnualAvg(i)
    
    
    #RasterStats(FilteredDictionary, "D:\\LoCA_Project\\new\\CNRMCM5\\historic\\AnnualAvg_test\\CNRMCM5_"+str(i)+".img")
    del FilteredDictionary
    print("finished calculating annual averages for year " + str(i))"""

