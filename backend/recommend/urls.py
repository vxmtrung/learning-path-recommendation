from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecommendView, RecommendEvaluationView

urlpatterns = [
    path('generate-learning-path/', RecommendView.as_view(), name='recommend'),
    path('generate-learning-path-evaluation/', RecommendEvaluationView.as_view(), name='recommend-evaluate'),
]
