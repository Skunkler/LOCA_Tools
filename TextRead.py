#This script was written by Warren Kunkler in support of the 2020 LOCA Project
#This is the script that calls the objects from other scripts such as AnnualAvg and DateAssignment
#This takes user input, and calculates the necessary data products from the raw daily data



import arcpy
from arcpy import env


#This class creates an object that takes the input raster, converts it to ascii, and runs the calculation
class TextRead():
    
    def __init__(self):
        self.avg = 0
    
    def areaDailyAvg(self, LoCAFile, ws):
        env.workspace = ws
        env.overwriteOutput = True

        #convert input raster to ascii
        arcpy.RasterToASCII_conversion(LoCAFile, ws + "\\TempText.txt")
        arcpy.AddMessage("success converting raster to ascii")

        #read the output ascii file
        readFile = open(ws + "\\TempText.txt", "r")
        lines = readFile.readlines()
        CalcArr = []
        count = 0
        #loop through each line within the ascii, and ignore the header information
        for line in lines:
            if line[0].isdigit() or line[0] == '-':
                #create a list of the filtered input line that removes null values
                ListVals = list(filter(lambda ListElem: ListElem != "-9999", line.split(' ')))
                #get a count as to how many values are in each row
                count += len(ListVals[:-1])

                #map each value in the filtered row to a float value from their native text value
                y = list(map(lambda ListElem: float(ListElem), ListVals[:-1]))

                #reduce each element in the filtered list
                x = reduce(lambda Elem, Elem2: Elem + Elem2, y)

                #append the sum value for each row to the CalcArr array
                CalcArr.append(float(x))
        readFile.close()
        arcpy.AddMessage("daily Avg complete")

        #store the calculated average for the user specified area of interest
        self.avg = sum(CalcArr)/count
        
