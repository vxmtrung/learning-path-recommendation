from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseImportView

urlpatterns = [
    path('import/', CourseImportView.as_view(), name='course-import'),
]
