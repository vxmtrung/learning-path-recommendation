from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MajorImportView

urlpatterns = [
    path('import/', MajorImportView.as_view(), name='major-import'),
]
