import django_filters
from django.contrib.gis.geos import Polygon
from geoapp.models import Feature

class FeatureFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='properties__name', lookup_expr='icontains')
    bbox = django_filters.CharFilter(method='filter_bbox')

    class Meta:
        model = Feature
        fields = ['name', 'bbox']

    def filter_bbox(self, queryset, value):
        """
        Filter the queryset by a bounding box.
        :param queryset: Comes from the view
        :param value: The value of the bbox parameter, e.g. '4.0,52.0,5.0,53.0'
        :return: A filtered queryset
        """
        minx, miny, maxx, maxy = map(float, value.split(',')) # get the values
        bbox = Polygon.from_bbox((minx, miny, maxx, maxy)) # create a Polygon object
        return queryset.filter(geometry__intersects=bbox) # filter the queryset by the bbox, use intersects to also get features that are partially in the bbox