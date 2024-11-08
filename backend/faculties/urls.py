from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FacultyImportView

urlpatterns = [
    path('import/', FacultyImportView.as_view(), name='faculty-import'),
]
