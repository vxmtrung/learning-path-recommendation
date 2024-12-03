from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentImportView, StudentListView

urlpatterns = [
    path('import/', StudentImportView.as_view(), name='student-import'),
    path('get-info-by-id/', StudentListView.as_view(), name='student-info'),
]
