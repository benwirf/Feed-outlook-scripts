import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline


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

###************************************************************************************###
###******************Function which creates and returns the graphs********************###

def make_plot(region, median, values1=[], values2=[], values3=[], labels=[], smooth=False):
    
    fy_months = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    
    district_median = [median for i in range(12)]
    
    # Median is constant (doesn't need smoothing)
    plt.plot(fy_months, district_median, label='Median', color='grey', linewidth=5)

    if smooth:
        # Interpolate data points for smooth lines
        idx_for_12_months = range(len(fy_months))
        xnew_for_12_months = np.linspace(min(idx_for_12_months), max(idx_for_12_months), 300)

        idx_for_part_yr = range(len(values3))
        xnew_for_part_yr = np.linspace(min(idx_for_part_yr), max(idx_for_part_yr), 300)

        spl_1 = make_interp_spline(idx_for_12_months, values1, k=3)
        smooth_1 = spl_1(xnew_for_12_months)

        spl_2 = make_interp_spline(idx_for_12_months, values2, k=3)
        smooth_2 = spl_2(xnew_for_12_months)
        
        # k value must be less than number of given points for interpolation
        spl_3 = make_interp_spline(idx_for_part_yr, values3, k=len(values3)-1 if len(values3)<4 else 3)
        smooth_3 = spl_3(xnew_for_part_yr)
        
        # Plot smoothed lines
        plt.plot(xnew_for_12_months, smooth_1, label=labels[0], color='blue', linewidth=5)
        plt.plot(xnew_for_12_months, smooth_2, label=labels[1], color='red', linewidth=5)
        plt.plot(xnew_for_part_yr, smooth_3, label=labels[2], color='lawngreen', linewidth=5)

    else:
        # plot lines without smoothing
        plt.plot(fy_months, values1, label=labels[0], color='blue', linewidth=5)
        plt.plot(fy_months, values2, label=labels[1], color='red', linewidth=5)
        plt.plot(fy_months[:len(values3)], values3, label=labels[2], color='lawngreen', linewidth=5)

    plt.legend(fontsize=18)
    plt.xticks(fontsize=18, rotation=90)
    if region == 'Northern':
        plt.yticks(np.arange(0, 2600, step=500), fontsize=18)
    elif region == 'Southern':
        plt.yticks(np.arange(0, 800, step=250), fontsize=18)
    plt.gca().yaxis.grid(linestyle='dashed')
#    plt.show()
    return plt

###************************************************************************************###
            
for district_result in district_results:
    print('###############')
#    print(district_result)

    district_name = district_result[0][3]
    print(f'Creating graph for {district_name}')
    
    if district_name in northern_district_medians.keys() or district_name == 'V.R.D.':
        region = 'Northern'
    else:
        region = 'Southern'
    
    long_term_district_median = district_result[0][5]

    f_years = sorted(list(set([row[0] for row in district_result])))
#    print(f_years)
    
    yr_labels = [y.replace('-', '/') for y in f_years]
#    print(yr_labels)

    f_yr1 = [row[-1] for row in district_result if row[0] == f_years[0]]
#    print(f_yr1)
    f_yr2 = [row[-1] for row in district_result if row[0] == f_years[1]]
    
    f_yr3 = [row[-1] for row in district_result if row[0] == f_years[2]]
    
    if len(f_yr3) == 1:
        f_yr3.insert(0, 0)
    
#print(district_name)
#print(region)
#print(long_term_district_median)
#print(f_yr1)
#print(f_yr2)
#print(f_yr3)
    
    graph = make_plot(region, long_term_district_median, f_yr1, f_yr2, f_yr3, yr_labels)
    graph.gcf().set_size_inches(10, 7)
    graph.savefig(f'/home/ben/Feed_Outlook/saved_graphs/{district_name}.png', bbox_inches='tight')
    graph.cla()
    
print('Done')