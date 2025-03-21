zonal_stats_params = {'INPUT':'Feed_Outlook_Data/Pastoral_districts/NT_pastoral_districts_WGS84.gpkg|layername=NT_pastoral_districts_WGS84',
                        'INPUT_RASTER':'AppData/Local/Temp/processing_EQkBVS/5a5185346e7842b999d1fafa59027709/OUTPUT.tif',
                        'RASTER_BAND':1,
                        'COLUMN_PREFIX':'_',
                        'STATISTICS':[2,3],
                        'OUTPUT':'TEMPORARY_OUTPUT'}

processing.run("native:zonalstatisticsfb", zonal_stats_params)
