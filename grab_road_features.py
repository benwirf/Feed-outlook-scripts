project = QgsProject.instance()

simple_roads = project.mapLayersByName('NT_Major_Roads_4326')[0]
complex_roads = project.mapLayersByName('Roads')[0]

sandover_feats = [f for f in complex_roads.getFeatures() if f['ROAD_NAME'] == 'ROPER']
sandover = [f.geometry() for f in sandover_feats]
#print(len(sandover))
feat_geom = QgsGeometry.collectGeometry(sandover)
#print(feat_geom)
with edit(simple_roads):
    ft = QgsFeature()
    ft.setGeometry(feat_geom)
    ft.setFields(simple_roads.fields())
    ft.setAttributes(sandover_feats[0].attributes())
    simple_roads.dataProvider().addFeatures([ft])
