import django_filters
from django.contrib.gis.geos import Polygon
from geoapp.models import FeatureCollection, Feature

"""
class FeatureFilter(django_filters.FilterSet):
    print("filter")
    bbox = django_filters.CharFilter(method='filter_bbox')

    class Meta:
        model = FeatureCollection
        fields = ['bbox']

    def filter_bbox(self, queryset, name, value):
        minx, miny, maxx, maxy = map(float, value.split(','))
        print(minx, miny, maxx, maxy)
        bbox = Polygon.from_bbox((minx, miny, maxx, maxy))
        return queryset.filter(features__geometry__intersects=bbox) #53.15,6,53.9,7
    """ # the stupid one operation on the collection...

class FeatureFilter(django_filters.FilterSet):
    bbox = django_filters.CharFilter(method='filter_bbox')

    class Meta:
        model = Feature
        fields = ['bbox']

    def filter_bbox(self, queryset, name, value):
        minx, miny, maxx, maxy = map(float, value.split(','))
        bbox = Polygon.from_bbox((minx, miny, maxx, maxy))
        return queryset.filter(geometry__intersects=bbox)