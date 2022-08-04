from osgeo import gdalnumeric

raster_path = iface.activeLayer().source()

raster1 = gdalnumeric.LoadFile(raster_path)

def total_growth_counts(raster1, region):
    if region == 'northern':
        # Northern Districts
        class1_count = ((raster1 > 0)&(raster1 <= 1000)).sum()
        class2_count = ((raster1 > 1000)&(raster1 <= 2000)).sum()
        class3_count = ((raster1 > 2000)&(raster1 <= 3000)).sum()
        class4_count = (raster1 > 3000).sum()
        no_data_count = (raster1 == 0).sum()
        #print(class1_count)
        print(f'0-1000: {class1_count}')
        #print(class2_count)
        print(f'1000-2000: {class2_count}')
        #print(class3_count)
        print(f'2000-3000: {class3_count}')
        #print(class4_count)
        print(f'>3000: {class4_count}')
        #print(no_data_count)
        print(f'No Data: {no_data_count}')
        
        total_pixel_count = sum([class1_count, class2_count, class3_count, class4_count, no_data_count])
        total_pixel_count_greater_than_zero = sum([class1_count, class2_count, class3_count, class4_count])

        print(f'Total pixels: {total_pixel_count}')
        print(f'Total pixels excluding no data: {total_pixel_count_greater_than_zero}')
        
        # Northern Districts
        print(f'% < 1000: {class1_count/total_pixel_count_greater_than_zero*100}')
        print(f'% 1000-2000: {class2_count/total_pixel_count_greater_than_zero*100}')
        print(f'% 2000-3000: {class3_count/total_pixel_count_greater_than_zero*100}')
        print(f'% > 3000: {class4_count/total_pixel_count_greater_than_zero*100}')
        ##############################################################################
        ########################################################################

    elif region == 'southern':
        # Southern Districts
        class1_count = ((raster1 > 0)&(raster1 <= 250)).sum()
        class2_count = ((raster1 > 250)&(raster1 <= 500)).sum()
        class3_count = ((raster1 > 500)&(raster1 <= 1000)).sum()
        class4_count = (raster1 > 1000).sum()
        no_data_count = (raster1 == 0).sum()
        #print(class1_count)
        print(f'0-250: {class1_count}')
        #print(class2_count)
        print(f'250-500: {class2_count}')
        #print(class3_count)
        print(f'500-1000: {class3_count}')
        #print(class4_count)
        print(f'>1000: {class4_count}')
        #print(no_data_count)
        print(f'No Data: {no_data_count}')
        ###########################################################################

        total_pixel_count = sum([class1_count, class2_count, class3_count, class4_count, no_data_count])
        total_pixel_count_greater_than_zero = sum([class1_count, class2_count, class3_count, class4_count])

        print(f'Total pixels: {total_pixel_count}')
        print(f'Total pixels excluding no data: {total_pixel_count_greater_than_zero}')

        # Southern Districts
        print(f'% < 250: {class1_count/total_pixel_count_greater_than_zero*100}')
        print(f'% 250-500: {class2_count/total_pixel_count_greater_than_zero*100}')
        print(f'% 500-1000: {class3_count/total_pixel_count_greater_than_zero*100}')
        print(f'% > 1000: {class4_count/total_pixel_count_greater_than_zero*100}')
        ##############################################################################

#total_growth_counts(raster1, region='northern')
total_growth_counts(raster1, region='southern')
