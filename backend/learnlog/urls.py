from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LearnlogImportView, ImportGradeView

urlpatterns = [
    path('import/', LearnlogImportView.as_view(), name='learnlog-import'),
    path('import-grade/', ImportGradeView.as_view(), name='learnlog-import-grade'),
]
