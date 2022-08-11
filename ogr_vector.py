from osgeo import ogr

district_path = 'C:\\Users\\qw2\\Desktop\\Feed_Outlook_Data\\Pastoral_districts\\NT_pastoral_districts_WGS84.gpkg'

def loop_zonal_stats(input_zone_polygon):
    shp = ogr.Open(input_zone_polygon)
    lyr = shp.GetLayer()
    featList = range(lyr.GetFeatureCount())
    print(shp, lyr, featList)
    for fid in featList:
        print(lyr.GetFeature(fid))
    
loop_zonal_stats(district_path)