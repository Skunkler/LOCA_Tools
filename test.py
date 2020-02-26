import arcpy
Raster = r"D:\LoCA_Project\CNRM_CM5_Historic_Test\rasterTest\CNRMCM5.img"


bandcount = arcpy.GetRasterProperties_management(Raster, "BANDCOUNT")

for i in range(1, int(bandcount.getOutput(0))):
    print Raster + '\\Layer_' + str(i)
