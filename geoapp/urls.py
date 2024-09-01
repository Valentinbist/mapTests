from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeatureCollectionViewSet

router = DefaultRouter()
router.register(r'featurecollections', FeatureCollectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]