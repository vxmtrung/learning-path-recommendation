from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LearnlogImportView

urlpatterns = [
    path('import/', LearnlogImportView.as_view(), name='learnlog-import'),
]
