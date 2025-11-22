from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('categories', views.AppCategoryViewSet, basename='appcategory')
router.register('device-apps', views.DeviceAppViewSet, basename='deviceapp')
router.register('app-relationships', views.AppRelationshipViewSet, basename='apprelationship')
router.register('personality-presets', views.AppPersonalityPresetViewSet, basename='personalitypreset')
router.register('', views.AppViewSet, basename='app')

urlpatterns = [
    path('', include(router.urls)),
]
