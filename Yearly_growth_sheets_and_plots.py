import os

current_fy = '2022-2023 FY'

latest_month = 'July'

months = ['January', 'February',  'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

northern_district_medians = {'Darwin': 2010, 'Katherine': 2097, 'Victoria River': 1842, 'Sturt Plateau': 2031, 'Roper': 2215, 'Gulf': 2083}
southern_district_medians = {'Barkly': 664, 'Tennant Creek': 288, 'Northern Alice Springs': 495, 'Plenty': 328, 'Southern Alice Springs': 232}

district_path = 'Feed_Outlook_Data\\Pastoral_districts\\NT_pastoral_districts_WGS84.gpkg'

district_lyr = QgsVectorLayer(district_path, 'Pastoral_districts', 'ogr')

#zonal_stats = QgsZonalStatistics(district_lyr, )

data_path = 'PROJECTS\\Northern Territory\\Feed Outlook\\MONTHLY GROWTH'

fy_folders = []

fy_folders.append((f"{int(fy.split(' ')[0].split('-')[0])-2}-{int(fy.split(' ')[0].split('-')[1])-2} FY"))
fy_folders.append((f"{int(fy.split(' ')[0].split('-')[0])-1}-{int(fy.split(' ')[0].split('-')[1])-1} FY"))
fy_folders.append(current_fy)

#print(fy_folders)
monthly_growth_layers = []

for fy_folder in fy_folders:
    dir_path = os.path.join(data_path, fy_folder)
#        print(dir_path)
    for file in os.scandir(dir_path):
        if file.name.split('.')[-1] == 'img':
#                print(file.name)
            raster_path = os.path.join(dir_path, file.name)
            raster_lyr = QgsRasterLayer(raster_path, f"Monthly_growth_{file.name.split('.')[0]}", 'gdal')
            if raster_lyr.isValid():
                monthly_growth_layers.append(raster_lyr)

for district in district_lyr.getFeatures([1]):
    district_name = district['DISTRICT']
    for rl in monthly_growth_layers:
#        print(rl.name())
        raster_stats = 
