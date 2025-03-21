from osgeo import gdalnumeric
#import pandas as pd
import os
import csv

northern_districts = ['darwin', 'katherine', 'VRD', 'sturt-plateau', 'roper', 'gulf']
southern_districts = ['barkly', 'tennant-creek', 'northern-alice-springs', 'plenty', 'southern-alice-springs']

###############################################################################
folder_path = 'Feed_Outlook_Data\\July\\TSDM_total\\TSDM_clipped_to_districts'
###############################################################################

def total_tsdm_counts(raster1, district, region):
    if region == 'northern':
        # Northern Districts
        class1_count = ((raster1 > 0)&(raster1 <= 1000)).sum()
        class2_count = ((raster1 > 1000)&(raster1 <= 2000)).sum()
        class3_count = ((raster1 > 2000)&(raster1 <= 3000)).sum()
        class4_count = (raster1 > 3000).sum()
        no_data_count = (raster1 == 0).sum()
        ########################################################################
        total_pixel_count = sum([class1_count, class2_count, class3_count, class4_count, no_data_count])
        total_pixel_count_greater_than_zero = sum([class1_count, class2_count, class3_count, class4_count])
        ########################################################################
        class1_pcnt = class1_count/total_pixel_count_greater_than_zero*100
        class2_pcnt = class2_count/total_pixel_count_greater_than_zero*100
        class3_pcnt = class3_count/total_pixel_count_greater_than_zero*100
        class4_pcnt = class4_count/total_pixel_count_greater_than_zero*100
        ########################################################################

    elif region == 'southern':
        # Southern Districts
        class1_count = ((raster1 > 0)&(raster1 <= 250)).sum()
        class2_count = ((raster1 > 250)&(raster1 <= 500)).sum()
        class3_count = ((raster1 > 500)&(raster1 <= 1000)).sum()
        class4_count = (raster1 > 1000).sum()
        no_data_count = (raster1 == 0).sum()
        ########################################################################
        total_pixel_count = sum([class1_count, class2_count, class3_count, class4_count, no_data_count])
        total_pixel_count_greater_than_zero = sum([class1_count, class2_count, class3_count, class4_count])
        ########################################################################
        class1_pcnt = class1_count/total_pixel_count_greater_than_zero*100
        class2_pcnt = class2_count/total_pixel_count_greater_than_zero*100
        class3_pcnt = class3_count/total_pixel_count_greater_than_zero*100
        class4_pcnt = class4_count/total_pixel_count_greater_than_zero*100
        ########################################################################
        
    checksum = sum([class1_pcnt, class2_pcnt, class3_pcnt, class4_pcnt])
        
    return [district, class1_count, class2_count, class3_count, class4_count, class1_pcnt, class2_pcnt, class3_pcnt, class4_pcnt, checksum]

output_csv = open('Feed_Outlook_Data\\July\\TSDM_total\\tsdm_summary_july_22.csv', mode='w', newline='')
writer = csv.writer(output_csv)
writer.writerow(['District', 'Low count', 'Low-moderate count', 'Moderate count', 'High count', 'Low pcnt', 'Low-moderate pcnt', 'Moderate pcnt', 'High pcnt', 'checksum'])

for file in os.scandir(folder_path):
    file_ext = file.name.split('.')[-1]
    if file_ext == 'img':
        district_name = file.name.split('.')[0].split('_')[-1]
#        print(district_name)
        raster_path = os.path.join(folder_path, file.name)
#        print(raster_path)
        raster1 = gdalnumeric.LoadFile(raster_path)
        if district_name in northern_districts:
            writer.writerow(total_tsdm_counts(raster1, district_name, 'northern'))
        elif district_name in southern_districts:
            writer.writerow(total_tsdm_counts(raster1, district_name, 'southern'))
        
output_csv.close()
