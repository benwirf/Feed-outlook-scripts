
fy = '2022-2023 FY'

latest_month = 'July'

months = ['January', 'February',  'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

northern_district_medians = {'Darwin': 2010, 'Katherine': 2097, 'Victoria River': 1842, 'Sturt Plateau': 2031, 'Roper': 2215, 'Gulf': 2083}
southern_district_medians = {'Barkly': 664, 'Tennant Creek': 288, 'Northern Alice Springs': 495, 'Plenty': 328, 'Southern Alice Springs': 232}

district_path = '/home/ben/Feed_Outlook/Feed_Outlook_Data/Pastoral_districts/NT_pastoral_districts_WGS84.gpkg'

data_path = '/home/ben/Feed_Outlook/MONTHLY GROWTH'

fy_folders = []

fy_folders.append((f"{int(fy.split(' ')[0].split('-')[0])-2}-{int(fy.split(' ')[0].split('-')[1])-2} FY"))
fy_folders.append((f"{int(fy.split(' ')[0].split('-')[0])-1}-{int(fy.split(' ')[0].split('-')[1])-1} FY"))
fy_folders.append(fy)

#print(fy_folders)
all_districts = list(northern_district_medians.keys()) + list(southern_district_medians.keys())

district_results = [list() for i in range(11)]

for fy_folder in fy_folders:
#    print(fy_folder)
    fyear = fy_folder.split(' ')[0]
#    print('####################################################')
    raw_inputs = []
    dir_path = os.path.join(data_path, fy_folder)
#        print(dir_path)
    for file in os.scandir(dir_path):
        if file.name.split('.')[-1] == 'img':
#                print(file.name)
            raster_path = os.path.join(dir_path, file.name)
            raw_inputs.append(raster_path)
    # os.scandir() does not return files in directory order...
    # we need to return a sorted (yyyymm) version of the input list e.g. [202107, 202108, 202109] etc.
    inputs = sorted(raw_inputs)
    for i in range(len(inputs)):
        ##########Get calendar year and month###################
#        print(inputs[i])
        calendar_yr = inputs[i].split('/')[-1].split('.')[0][:4]
        mnth_digit = inputs[i].split('/')[-1].split('.')[0][-2:]
        mnth_name = months[int(mnth_digit)-1]
        ########################################################
        # add next input to stack on each iteration e.g. [1], [1,2], [1,2,3] etc
        rstack = inputs[:i+1]
        if len(rstack) == 1:
            # just run zonal stats on single input
            zonal_stats_params = {'INPUT':f'{district_path}|layername=NT_pastoral_districts_WGS84',
                        'INPUT_RASTER':rstack[0],
                        'RASTER_BAND':1,
                        'COLUMN_PREFIX':'_',
                        'STATISTICS':[2,3],
                        'OUTPUT':'TEMPORARY_OUTPUT'}

            stats = processing.run("native:zonalstatisticsfb", zonal_stats_params)['OUTPUT']

        elif len(rstack) > 1:
            # run cell stats to sum pixels of rasters in rstack, then zonal stats for mean & median for each district
            cell_stat_params = {'INPUT':rstack,
                    'STATISTIC':0,
                    'IGNORE_NODATA':True,
                    'REFERENCE_LAYER':rstack[0],
                    'OUTPUT_NODATA_VALUE':-9999,
                    'OUTPUT':'TEMPORARY_OUTPUT'}
            cell_sum = processing.run("native:cellstatistics", cell_stat_params)
            
            zonal_stats_params = {'INPUT':f'{district_path}|layername=NT_pastoral_districts_WGS84',
                        'INPUT_RASTER':cell_sum['OUTPUT'],
                        'RASTER_BAND':1,
                        'COLUMN_PREFIX':'_',
                        'STATISTICS':[2,3],
                        'OUTPUT':'TEMPORARY_OUTPUT'}

            stats = processing.run("native:zonalstatisticsfb", zonal_stats_params)['OUTPUT']
            
        for f in stats.getFeatures():
#                print(f['DISTRICT'], f['_mean'], f['_median'])
            for i, district in enumerate(all_districts):
                if f['DISTRICT'] == district or (district == 'Victoria River' and f['DISTRICT'] == 'V.R.D.'):
#                        district_results[i].append([f['DISTRICT'], f['_mean'], f['_median']])
                    if district in northern_district_medians.keys():
                        long_term_median = northern_district_medians[district]
                    elif district in southern_district_medians.keys():
                        long_term_median = southern_district_medians[district]
                    # Write all column values as a row/feature attributes
                    district_results[i].append([fyear, calendar_yr, mnth_name, f['DISTRICT'], f['_mean'], long_term_median, f['_median']])
                
output_layers = []
            
#        print(stack)
for district_result in district_results:
#    print('#####################################################################')
#    print(district_result)
    district_name = district_result[0][3]
    layer = QgsVectorLayer('Point', district_name, 'memory')
    layer.dataProvider().addAttributes([
        QgsField('Financial_year', QVariant.String),
        QgsField('Calendar_year', QVariant.String),
        QgsField('Month', QVariant.String),
        QgsField('District', QVariant.String),
        QgsField('Cumulative_mean', QVariant.Double),
        QgsField('Long_term_median', QVariant.Int),
        QgsField('Cumulative_median', QVariant.Double)
    ])
    #### Working up to here TODO: create feature for each row in district result,
    #### add to layer, then save each layer as spreadsheet (processing), with
    #### option to overwrite existing file so each district will be a separate
    #### sheet in the workbook
    for row in district_result:
        feat = QgsFeature()
        feat.setAttributes(row)
        layer.dataProvider().addFeatures([feat])
        layer.updateFeature(feat)
    
    output_layers.append(layer)
    
# Export layers to spreadsheet

save_2_xls_params = {'LAYERS': output_layers,
    'USE_ALIAS':False,
    'FORMATTED_VALUES':False,
    'OUTPUT':'/home/ben/Feed_Outlook/monthly_growth_totals.xlsx',
    'OVERWRITE':True}

processing.run("native:exporttospreadsheet", save_2_xls_params)

print('Done')