from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('stats', views.UserStatsViewSet, basename='userstats')
router.register('trends', views.TrendAnalysisViewSet, basename='trendanalysis')

urlpatterns = [
    path('', include(router.urls)),
]
