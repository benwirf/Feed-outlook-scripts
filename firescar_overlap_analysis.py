district_lyr = QgsProject.instance().mapLayersByName('Pastoral_Districts_GDA94')[0]
fs_lyr = QgsProject.instance().mapLayersByName('fs_3_July_22_clipped_to_districts')[0]

#Check fire_scar layer for invalid geometries
invalid_ids = [f.id() for f in fs_lyr.getFeatures() if not f.geometry().isGeosValid()]
#print(len(invalid_ids))
if len(invalid_ids) > 0:
    print(len(invalid_ids))
    fs_lyr.selectByIds(invalid_ids)

fs_da = QgsDistanceArea()
fs_da.setSourceCrs(fs_lyr.crs(), QgsProject.instance().transformContext())
fs_da.setEllipsoid(fs_lyr.crs().ellipsoidAcronym())

district_da = QgsDistanceArea()
district_da.setSourceCrs(district_lyr.crs(), QgsProject.instance().transformContext())
district_da.setEllipsoid(district_lyr.crs().ellipsoidAcronym())

sp_idx = QgsSpatialIndex(fs_lyr.getFeatures())

for district in district_lyr.getFeatures():
    district_area = district_da.measureArea(district.geometry())
    intersecting_features = [f for f in fs_lyr.getFeatures(sp_idx.intersects(district.geometry().boundingBox()))]
    intersection_area = sum([fs_da.measureArea(ft.geometry().intersection(district.geometry())) for ft in intersecting_features])
    print(f'{district["DISTRICT"]} area: {district_area}')
    print(f'Burnt area: {intersection_area}')
    print(f'Percentage of {district["DISTRICT"]} burnt: {(intersection_area/district_area)*100}')
