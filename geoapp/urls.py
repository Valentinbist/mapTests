from django.urls import path, include
from rest_framework.routers import DefaultRouter
from geoapp.views import FeatureCollectionViewSet, FeatureViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'featurecollections', FeatureCollectionViewSet)
router.register(r'features', FeatureViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api-auth/', include('rest_framework.urls')),  # Enable the default login
    path('gui/', views.index, name='index'),
    path('edit/', views.edit, name='edit'),
]