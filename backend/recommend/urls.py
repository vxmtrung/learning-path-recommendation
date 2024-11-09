from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecommendView

urlpatterns = [
    path('generate-learning-path/', RecommendView.as_view(), name='recommend'),
]
