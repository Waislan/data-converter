import os
from osgeo import gdal, ogr, osr

os.chdir(r'../data/')

raster = gdal.Open(r'ba_20221016_Pantanal_PUBLICx.tif')
band = raster.GetRasterBand(1)
band.ReadAsArray()

proj = raster.GetProjection()
shp_proj = osr.SpatialReference()
shp_proj.ImportFromWkt(proj)

output_file = 'ba_20221016_Pantanal_PUBLICx.shp'
call_drive = ogr.GetDriverByName('ESRI Shapefile')
create_shp = call_drive.CreateDataSource(output_file)
shp_layer = create_shp.CreateLayer('layername', srs = shp_proj)
new_field = ogr.FieldDefn(str('ID'), ogr.OFTInteger)
shp_layer.CreateField(new_field)

gdal.Polygonize(band, None, shp_layer, 0, [], callback = None)
create_shp.Destroy()
raster = None

shp_file = gpd.read_file('ba_20221016_Pantanal_PUBLICx.shp')
shp_file.to_file('ba_20221016_Pantanal_PUBLICx.geojson', driver='GeoJSON')