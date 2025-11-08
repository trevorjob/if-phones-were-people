from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('friends', views.FriendConnectionViewSet, basename='friendconnection')
router.register('device-visits', views.TemporaryDeviceConnectionViewSet, basename='deviceconnection')
router.register('challenges', views.ChallengeViewSet, basename='challenge')

urlpatterns = [
    path('', include(router.urls)),
]
