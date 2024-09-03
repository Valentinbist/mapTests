from django.urls import path, include
from rest_framework.routers import DefaultRouter
from geoapp.views import FeatureCollectionViewSet, FeatureViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.urls import path
from . import views
from .views import  list_features_page

router = DefaultRouter()
router.register(r'featurecollections', FeatureCollectionViewSet)
router.register(r'features', FeatureViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api-auth/', include('rest_framework.urls')),  # Enable the default login
    path('gui/', views.gui_map, name='gui_map'),
    path('get_jwt/', views.get_jwt, name='get_jwt'),
    path('features_gui/list/', list_features_page, name='list_features_page'),
    path('edit/', views.edit, name='edit'),
    path('edit/<int:feature_id>/', views.edit, name='edit_feature_page'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]