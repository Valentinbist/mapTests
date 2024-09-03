import django_filters
from django.contrib.gis.geos import Polygon
from geoapp.models import Feature

class FeatureFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='properties__name', lookup_expr='icontains')
    bbox = django_filters.CharFilter(method='filter_bbox')

    class Meta:
        model = Feature
        fields = ['name', 'bbox']

    def filter_bbox(self, queryset, name, value):
        minx, miny, maxx, maxy = map(float, value.split(','))
        bbox = Polygon.from_bbox((minx, miny, maxx, maxy))
        return queryset.filter(geometry__intersects=bbox)