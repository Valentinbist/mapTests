from django.db import models

from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser


class FeatureCollection(models.Model):
    name = models.CharField(max_length=255)
    crs = models.CharField(max_length=255)

class Feature(models.Model):
    feature_collection = models.ForeignKey(FeatureCollection, related_name='features', on_delete=models.CASCADE)
    geometry = models.MultiPolygonField()
    properties = models.JSONField()  # Store arbitrary properties in JSON format
    type = models.CharField(max_length=255, default='Feature')
