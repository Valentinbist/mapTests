from rest_framework import serializers
from geoapp.models import FeatureCollection, Feature

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        geo_field = 'geometry'
        fields = ('id', 'name', 'geometry')

class FeatureCollectionSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True, read_only=True)

    class Meta:
        model = FeatureCollection
        fields = ('id', 'name', 'crs', 'features')