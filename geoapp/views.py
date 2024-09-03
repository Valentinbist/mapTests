from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from geoapp.models import FeatureCollection, Feature
from geoapp.serializers import FeatureCollectionSerializer, FeatureSerializer
from geoapp.filters import FeatureFilter
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

def gui_map(request):
    return render(request, 'map.html')

def start_page(request):
    return render(request, 'start.html')

def edit(request, feature_id=None):
    #print(f"Received feature_id: {feature_id}")  # Debugging: log the received feature_id
    if feature_id:
        feature = get_object_or_404(Feature, id=feature_id)
    else:
        feature = None
    return render(request, 'edit.html', {'feature': feature})

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
    permission_classes = [IsAuthenticated]


class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    pagination_class = FeaturePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = FeatureFilter
    permission_classes = [IsAuthenticated]


def get_jwt(request):
    return render(request, 'get_jwt.html')

def list_features_page(request):
    return render(request, 'list.html')