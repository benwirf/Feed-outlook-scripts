from osgeo import gdal
from osgeo import ogr
import os
import numpy as np
import csv


def boundingBoxToOffsets(bbox, geot):
    col1 = int((bbox[0] - geot[0]) / geot[1])
    col2 = int((bbox[1] - geot[0]) / geot[1]) + 1
    row1 = int((bbox[3] - geot[3]) / geot[5])
    row2 = int((bbox[2] - geot[3]) / geot[5]) + 1
    return [row1, row2, col1, col2]


def geotFromOffsets(row_offset, col_offset, geot):
    new_geot = [
    geot[0] + (col_offset * geot[1]),
    geot[1],
    0.0,
    geot[3] + (row_offset * geot[5]),
    0.0,
    geot[5]
    ]
    return new_geot

mem_driver = ogr.GetDriverByName("Memory")
mem_driver_gdal = gdal.GetDriverByName("MEM")
shp_name = "temp"

fn_raster = 'R:\\LID-BigData\\SPATIAL DATA\\PROJECTS\\Northern Territory\\Feed Outlook\\MONTHLY GROWTH\\2022-2023 FY\\202207.01months.growth.tot.nt.img'
fn_zones = 'C:\\Users\\qw2\\Desktop\\Feed_Outlook_Data\\Pastoral_districts\\NT_pastoral_districts_WGS84.gpkg'

r_ds = gdal.Open(fn_raster)
p_ds = ogr.Open(fn_zones)

lyr = p_ds.GetLayer()
geot = r_ds.GetGeoTransform()

#niter = 0

feat_list = range(1, lyr.GetFeatureCount()+1)
print(feat_list)
for fid in feat_list:
    feat = lyr.GetFeature(fid)
#    print(feat.GetField('DISTRICT'))
    if feat.GetGeometryRef() is not None:
        if os.path.exists(shp_name):
            mem_driver.DeleteDataSource(shp_name)
        tp_ds = mem_driver.CreateDataSource(shp_name)
        tp_lyr = tp_ds.CreateLayer('polygons', None, ogr.wkbPolygon)
        tp_lyr.CreateFeature(feat.Clone())
        offsets = boundingBoxToOffsets(feat.GetGeometryRef().GetEnvelope(), geot)
        new_geot = geotFromOffsets(offsets[0], offsets[2], geot)
        
        tr_ds = mem_driver_gdal.Create("", offsets[3] - offsets[2], offsets[1] - offsets[0], 1, gdal.GDT_Byte)
        
        tr_ds.SetGeoTransform(new_geot)
        gdal.RasterizeLayer(tr_ds, [1], tp_lyr, burn_values=[1])
        tr_array = tr_ds.ReadAsArray()
        
        r_array = r_ds.GetRasterBand(1).ReadAsArray(offsets[2], offsets[0], offsets[3] - offsets[2], offsets[1] - offsets[0])
        
        id = p_feat.GetFID()
        
        if r_array is not None:
            maskarray = np.ma.MaskedArray(r_array, np.logical_or(r_array==nodata, np.logical_not(tr_array)))
            if maskarray is not None:
                zstats = [feat.GetField('DISTRICT'), '2022/2023', '2022', 'JUL', maskarray.mean(), 664, np.ma.median(maskarray)]
                
        tp_ds = None
        tp_lyr = None
        tr_ds = None

        print(zstats)