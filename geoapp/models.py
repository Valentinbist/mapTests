from django.db import models

from django.contrib.gis.db import models

class FeatureCollection(models.Model):
    name = models.CharField(max_length=255)
    crs = models.CharField(max_length=255)

class Feature(models.Model):
    feature_collection = models.ForeignKey(FeatureCollection, related_name='features', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    geometry = models.MultiPolygonField()