from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('usage-data', views.UsageDataViewSet, basename='usagedata')
router.register('app-usage', views.AppUsageViewSet, basename='appusage')
router.register('patterns', views.UsagePatternViewSet, basename='usagepattern')
router.register('goals', views.UsageGoalViewSet, basename='usagegoal')

urlpatterns = [
    path('', include(router.urls)),
]
