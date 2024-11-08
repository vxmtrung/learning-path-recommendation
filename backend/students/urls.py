from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentImportView

urlpatterns = [
    path('import/', StudentImportView.as_view(), name='student-import'),
]
