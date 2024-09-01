from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from geoapp.models import FeatureCollection, Feature
from geoapp.serializers import FeatureCollectionSerializer, FeatureSerializer
from geoapp.filters import FeatureFilter

class FeatureCollectionPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100


class FeatureCollectionViewSet(viewsets.ModelViewSet):
    queryset = FeatureCollection.objects.all()
    serializer_class = FeatureCollectionSerializer
    pagination_class = FeatureCollectionPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = FeatureFilter
