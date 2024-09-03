from rest_framework import serializers
from geoapp.models import FeatureCollection, Feature

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        geo_field = 'geometry'
        fields = ('id', 'geometry', 'properties', 'type', 'feature_collection')

class FeatureCollectionSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True, read_only=True) # one could discuss not to show the features in the collection, since they can get very large, and then add a filter for the features using the collection ID

    class Meta:
        model = FeatureCollection
        fields = ('id', 'name', 'crs', 'features')