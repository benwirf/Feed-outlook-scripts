from osgeo import gdal
import numpy as np
import csv

lyr = iface.activeLayer()
pcnt_growth_csv = 'R:\\LID-BigData\\SPATIAL DATA\\PROJECTS\\Northern Territory\\Feed Outlook\\2023\\MARCH-2023\\OUTPUT\\Percentile_growth_summary.csv'

tbl_growth = open(pcnt_growth_csv, mode='w', newline='')

csv_writer = csv.writer(tbl_growth)

csv_writer.writerow(['District', 'Extremely low %', 'Well below average %', 'Below average %', 'Average %', 'Above average %', 'Well above average %', 'Extremely high %', 'Check Sum'])

def get_class_counts(relative_growth_layer):
    path = relative_growth_layer.source()
    ds = gdal.Open(path)
    arr = ds.ReadAsArray()

    # get pixel counts for growth category bins
    extremely_low_count = ((arr > 0)&(arr <= 10)).sum()
    well_below_average_count = ((arr > 10)&(arr <= 20)).sum()
    below_average_count = ((arr > 20)&(arr <= 30)).sum()
    average_count = ((arr > 30)&(arr <= 70)).sum()
    above_average_count = ((arr > 70)&(arr <= 80)).sum()
    well_above_average_count = ((arr > 80)&(arr <= 90)).sum()
    extremely_high_count = ((arr > 90)&(arr <= 100)).sum()
    
    # get pixel counts for seasonally low growth, fire scars & water bodies (not included in total)
    seasonally_low_growth_count = (arr == 255).sum()
    water_count = (arr == 254).sum()
    fire_scar_count = (arr == 253).sum()
    # get no data count (also excluded from total)
    no_data_count = (arr == -999).sum()
    
    # get total count of relevant pixels
    total_valid_pixel_count = sum([extremely_low_count,
                                    well_below_average_count,
                                    below_average_count,
                                    average_count,
                                    above_average_count,
                                    well_above_average_count,
                                    extremely_high_count])
    
    # get each category as a percentage of the total
    extremely_low_pcnt = extremely_low_count/total_valid_pixel_count*100
    well_below_average_pcnt = well_below_average_count/total_valid_pixel_count*100
    below_average_pcnt = below_average_count/total_valid_pixel_count*100
    average_pcnt = average_count/total_valid_pixel_count*100
    above_average_pcnt = above_average_count/total_valid_pixel_count*100
    well_above_average_pcnt = well_above_average_count/total_valid_pixel_count*100
    extremely_high_pcnt = extremely_high_count/total_valid_pixel_count*100
    
    # check that sum of percentages add up to 100
    percent_check_sum = sum([extremely_low_pcnt,
                            well_below_average_pcnt,
                            below_average_pcnt,
                            average_pcnt,
                            above_average_pcnt,
                            well_above_average_pcnt,
                            extremely_high_pcnt])
                            
    # return percentages and check sum
    return (extremely_low_pcnt,
            well_below_average_pcnt,
            below_average_pcnt,
            average_pcnt,
            above_average_pcnt,
            well_above_average_pcnt,
            extremely_high_pcnt,
            percent_check_sum)
    
    
# Iterate over percentiles growth layers for each district,
# write a row to csv for each district

# only the clipped percentile growth raster for each district should be loaded in project
for lyr in QgsProject.instance().mapLayers().values():
    district_name = lyr.name().split('-')[0]
    
    all_counts = get_class_counts(lyr)
    
    csv_writer.writerow([district_name,
                        all_counts[0],
                        all_counts[1],
                        all_counts[2],
                        all_counts[3],
                        all_counts[4],
                        all_counts[5],
                        all_counts[6],
                        all_counts[7]])

tbl_growth.close()
del writer