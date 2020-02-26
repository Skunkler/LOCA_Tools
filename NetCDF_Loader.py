import arcpy, os
from arcpy import env



env.overwriteOutput = True
Input_NetCDF_layer = arcpy.GetParameterAsText(0)

Output_Folder = arcpy.GetParameterAsText(1)



Input_Name = Input_NetCDF_layer

Output_Raster = Output_Folder + os.sep + Input_Name + '.img'

arcpy.AddMessage("converting netcdf to raster")

try:
    arcpy.CopyRaster_management(Input_Name, Output_Raster)
    arcpy.AddMessage("Conversion successful")
except:
    arcpy.AddMessage(arcpy.GetMessage(2))

arcpy.AddMessage("Processing complete")

