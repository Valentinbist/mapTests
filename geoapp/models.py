from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser


class FeatureCollection(models.Model):
    """
    A collection of features. Thereby the code supports multiple collections.
    """
    name = models.CharField(max_length=255)
    crs = models.CharField(max_length=255)

class Feature(models.Model):
    """
    A feature with a geometry and properties.
    """
    feature_collection = models.ForeignKey(FeatureCollection, related_name='features', on_delete=models.CASCADE) # each feature is in a collection
    geometry = models.MultiPolygonField()
    properties = models.JSONField()  # Store arbitrary properties in JSON format
    type = models.CharField(max_length=255, default='Feature')
