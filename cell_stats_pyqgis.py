cell_stat_params = {'INPUT':['PROJECTS/Northern Territory/Feed Outlook/MONTHLY GROWTH/2021-2022 FY/202107.01months.growth.tot.nt.img',
                            'PROJECTS/Northern Territory/Feed Outlook/MONTHLY GROWTH/2021-2022 FY/202108.01months.growth.tot.nt.img',
                            'PROJECTS/Northern Territory/Feed Outlook/MONTHLY GROWTH/2021-2022 FY/202109.01months.growth.tot.nt.img',
                            'PROJECTS/Northern Territory/Feed Outlook/MONTHLY GROWTH/2021-2022 FY/202110.01months.growth.tot.nt.img',
                            'PROJECTS/Northern Territory/Feed Outlook/MONTHLY GROWTH/2021-2022 FY/202111.01months.growth.tot.nt.img',
                            'PROJECTS/Northern Territory/Feed Outlook/MONTHLY GROWTH/2021-2022 FY/202112.01months.growth.tot.nt.img',
                            'PROJECTS/Northern Territory/Feed Outlook/MONTHLY GROWTH/2021-2022 FY/202201.01months.growth.tot.nt.img',
                            'PROJECTS/Northern Territory/Feed Outlook/MONTHLY GROWTH/2021-2022 FY/202202.01months.growth.tot.nt.img',
                            'PROJECTS/Northern Territory/Feed Outlook/MONTHLY GROWTH/2021-2022 FY/202203.01months.growth.tot.nt.img',
                            'PROJECTS/Northern Territory/Feed Outlook/MONTHLY GROWTH/2021-2022 FY/202204.01months.growth.tot.nt.img',
                            'PROJECTS/Northern Territory/Feed Outlook/MONTHLY GROWTH/2021-2022 FY/202205.01months.growth.tot.nt.img',
                            'PROJECTS/Northern Territory/Feed Outlook/MONTHLY GROWTH/2021-2022 FY/202206.01months.growth.tot.nt.img'],
                    'STATISTIC':0,
                    'IGNORE_NODATA':True,
                    'REFERENCE_LAYER':'PROJECTS/Northern Territory/Feed Outlook/MONTHLY GROWTH/2021-2022 FY/202107.01months.growth.tot.nt.img',
                    'OUTPUT_NODATA_VALUE':-9999,
                    'OUTPUT':'TEMPORARY_OUTPUT'}

processing.run("native:cellstatistics", cell_stat_params)
