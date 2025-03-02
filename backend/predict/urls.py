from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PredictView, PredictBaseOnLearningOutcomeView

urlpatterns = [
    path('train-predict-model/', PredictView.as_view(), name='predict'),
    path('train-predict-learning-outcome/', PredictBaseOnLearningOutcomeView.as_view(), name='predict-learning-outcome'),
]
