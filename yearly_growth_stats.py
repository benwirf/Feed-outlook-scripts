from osgeo import gdal
from osgeo import ogr
import os
import numpy as np
import pandas as pd


fy = '2022-2023 FY'

latest_month = 'July'

months = ['January', 'February',  'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

northern_district_medians = {'Darwin': 2010, 'Katherine': 2097, 'Victoria River': 1842, 'Sturt Plateau': 2031, 'Roper': 2215, 'Gulf': 2083}
southern_district_medians = {'Barkly': 664, 'Tennant Creek': 288, 'Northern Alice Springs': 495, 'Plenty': 328, 'Southern Alice Springs': 232}

district_path = 'Feed_Outlook_Data\\Pastoral_districts\\NT_pastoral_districts_WGS84.gpkg'

data_path = 'PROJECTS\\Northern Territory\\Feed Outlook\\MONTHLY GROWTH'

fy_folders = []

# Determine the 3 folders to use (current and previous 2 financial based on current FY
fy_folders.append((f"{int(fy.split(' ')[0].split('-')[0])-2}-{int(fy.split(' ')[0].split('-')[1])-2} FY"))
fy_folders.append((f"{int(fy.split(' ')[0].split('-')[0])-1}-{int(fy.split(' ')[0].split('-')[1])-1} FY"))
fy_folders.append(fy)

#print(fy_folders)
monthly_growth_inputs = []

for fy_folder in fy_folders:
    dir_path = os.path.join(data_path, fy_folder)
#        print(dir_path)
    for file in os.scandir(dir_path):
        if file.name.split('.')[-1] == 'img':
#                print(file.name)
            raster_path = os.path.join(dir_path, file.name)
            if os.path.exists(raster_path):
                monthly_growth_inputs.append(raster_path)

#for pth in monthly_growth_inputs:
#    print(pth)
########################################################################################################################

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
#######################################################################################################################
p_ds = ogr.Open(district_path)
lyr = p_ds.GetLayer()
#feat_list = range(1, lyr.GetFeatureCount()+1)
feat_list = [1]
#print(feat_list)

for fid in feat_list:
    stats = []
    feat = lyr.GetFeature(fid)
    district_name = feat.GetField('DISTRICT')
#    print(district_name)
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
        
        for growth_raster in monthly_growth_inputs:
#            print(growth_raster)
            # Format current financial year string e.g. '2022/2023'
            yr1 = growth_raster.split('\\')[7].split(' ')[0].split('-')[0]
            yr2 = growth_raster.split('\\')[7].split(' ')[0].split('-')[1]
            FY = f"{yr1}/{yr2}"
            # Extract current year and month
            yyyy_mm = growth_raster.split('\\')[-1].split('.')[0]
            CY = yyyy_mm[:4]
            mm = yyyy_mm[-2:]
            if mm[0] == '0':
                mm = mm[-1]
            MTH = months[int(mm)-1]
            # Retrieve long term district median value
            if district_name in northern_district_medians.keys():
                LT_MED = northern_district_medians[district_name]
            elif district_name in southern_district_medians.keys():
                LT_MED = southern_district_medians[district_name]
            r_ds = gdal.Open(growth_raster)
            r_array = r_ds.GetRasterBand(1).ReadAsArray(offsets[2], offsets[0], offsets[3] - offsets[2], offsets[1] - offsets[0])

            if r_array is not None:
                maskarray = np.ma.MaskedArray(r_array, np.logical_or(r_array==nodata, np.logical_not(tr_array)))
                if maskarray is not None:
                    zstats = [district_name, FY, CY, MTH, maskarray.mean(), 0, LT_MED, np.ma.median(maskarray), 0]
                    
            tp_ds = None
            tp_lyr = None
            tr_ds = None
            
            stats.append(zstats)
    df = pd.DataFrame(stats, columns= ['District', 'Financial Year', 'Year', 'Month', 'Mean', 'Stacked Mean', 'LT Median', 'Monthly Median', 'Stacked Median'])
#    df['Stacked Median'] = df['Monthly Median'].cumsum()
#    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#        print (df)
    f_years = df['Financial Year'].unique()
    
    chunks = []
    
    for f_year in f_years:
        f_year_chunk = df[df['Financial Year'] == f_year]
        f_year_chunk['Stacked Mean'] = f_year_chunk['Mean'].cumsum()
        f_year_chunk['Stacked Median'] = f_year_chunk['Monthly Median'].cumsum()
        chunks.append(f_year_chunk)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(pd.concat(chunks))
        
