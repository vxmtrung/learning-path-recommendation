from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecommendLogsView

urlpatterns = [
    path('get-log/', RecommendLogsView.as_view(), name='recommend-logs'),
]