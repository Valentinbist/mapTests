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
router.register(r'featurecollections', FeatureCollectionViewSet) # CRUD also for the collections
router.register(r'features', FeatureViewSet) # CRUD for the features

urlpatterns = [
    path('', include(router.urls)), # api root
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # backend for the JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # backend for the JWT

    path('api-auth/', include('rest_framework.urls')),  # Enable the default login
    path('gui/', views.gui_map, name='gui_map'), # GUI for the map
    path('get_jwt/', views.get_jwt, name='get_jwt'), # GUI for the jwt, sort of a login page
    path('features_gui/list/', list_features_page, name='list_features_page'), # GUI for the features
    path('edit/', views.edit, name='edit'), # GUI for the edit page, where you can load a feature to edit
    path('edit/<int:feature_id>/', views.edit, name='edit_feature_page'), # GUI for the edit page, where you can edit a feature (forwarded from map and list)
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'), # to check if the token is valid, used for the "logged in"

]