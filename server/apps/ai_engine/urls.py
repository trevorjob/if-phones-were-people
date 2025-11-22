from django.urls import path
from . import views

urlpatterns = [
    path('generate-conversations/', views.generate_conversations_for_user, name='generate-conversations'),
    path('generate-journals/', views.generate_journals_for_user, name='generate-journals'),
]
