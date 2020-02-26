import arcpy
arcpy.CheckOutExtension("Spatial")


class RasterManipulation:

    def __init__(self, boundaryShp, county):
       
        self.boundary = boundaryShp
        self.county = county
        self.expression = ""

    def calcRasters(ListRasters, save_location):
        try:
            calc = arcpy.sa.CellStatistics(ListRasters, statistics_type = "MEAN")
            calc.save(save_location)
        except:
            print(arcpy.GetMessages(2))
            

    
        
    
    
e
