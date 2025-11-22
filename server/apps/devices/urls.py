from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('device-types', views.DeviceTypeViewSet, basename='devicetype')
router.register('personality-traits', views.PersonalityTraitViewSet, basename='personalitytrait')
router.register('device-relationships', views.DeviceRelationshipViewSet, basename='devicerelationship')
router.register('', views.DeviceViewSet, basename='device')

urlpatterns = [
    path('', include(router.urls)),
]
