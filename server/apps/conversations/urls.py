from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('triggers', views.ConversationTriggerViewSet, basename='conversationtrigger')
router.register('device-journals', views.DeviceJournalViewSet, basename='devicejournal')
router.register('app-journals', views.AppJournalViewSet, basename='appjournal')
router.register('templates', views.ConversationTemplateViewSet, basename='conversationtemplate')
router.register('feedback', views.ConversationFeedbackViewSet, basename='conversationfeedback')
router.register('', views.ConversationViewSet, basename='conversation')

urlpatterns = [
    path('', include(router.urls)),
]
