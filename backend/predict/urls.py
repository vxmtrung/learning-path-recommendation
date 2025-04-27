from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PredictView, PredictBaseOnLearningOutcomeView, TestingAPIView, DiagramAPIView

urlpatterns = [
    path('train-predict-model/', PredictView.as_view(), name='predict'),
    path('train-predict-learning-outcome/', PredictBaseOnLearningOutcomeView.as_view(), name='predict-learning-outcome'),
    path('test-predict-model/', TestingAPIView.as_view(), name='test-predict'),
    path('diagram/', DiagramAPIView.as_view(), name='diagram'),
]
