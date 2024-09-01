import json
from django.core.management.base import BaseCommand
from geoapp.models import FeatureCollection, Feature
from django.contrib.gis.geos import MultiPolygon, Polygon

class Command(BaseCommand):
    help = 'Load GeoJSON data into the database'

    def handle(self, *args, **kwargs):
        with open('municipalities_nl.geojson', 'r') as file:
            data = json.load(file)

        feature_collection = FeatureCollection.objects.create(
            name=data.get('name', 'Unnamed Collection'),
            crs=data.get('crs', {}).get('properties', {}).get('name', 'Unknown CRS')
        )

        features = data.get('features', [])
        for feature in features:
            geometry = feature.get('geometry', {})
            coordinates = geometry.get('coordinates', [])
            multipolygon = MultiPolygon([Polygon(coords[0]) for coords in coordinates])
            Feature.objects.create(
                feature_collection=feature_collection,
                name=feature.get('properties', {}).get('name', 'Unnamed Feature'),
                geometry=multipolygon
            )

        self.stdout.write(self.style.SUCCESS('Successfully loaded GeoJSON data'))