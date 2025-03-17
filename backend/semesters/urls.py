from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SemesterView

urlpatterns = [
    path('semesters/', SemesterView.as_view(), name='semesters'),
]