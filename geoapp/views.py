from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from geoapp.models import FeatureCollection, Feature
from geoapp.serializers import FeatureCollectionSerializer, FeatureSerializer
from geoapp.filters import FeatureFilter
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def edit(request):
    return render(request, 'edit.html')

class FeatureCollectionPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100

class FeaturePagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class FeatureCollectionViewSet(viewsets.ModelViewSet):
    queryset = FeatureCollection.objects.all()
    serializer_class = FeatureCollectionSerializer
    pagination_class = FeatureCollectionPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = FeatureFilter
    permission_classes = [IsAuthenticated]


class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    pagination_class = FeaturePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = FeatureFilter
    permission_classes = [IsAuthenticated]