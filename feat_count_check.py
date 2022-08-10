lyr = QgsProject.instance().mapLayersByName('firescars_Aug_5_22_clipped_to_districts')[0]

total_fts = lyr.featureCount()
fts1 = [f.id() for f in lyr.getFeatures() if f['month'] in [1, 2, 3, 4, 5, 6]]
fts2 = [f.id() for f in lyr.getFeatures() if f['month'] == 7]
print(total_fts)
print(len(fts1))
print(len(fts2))
print(sum([len(fts1), len(fts2)]))