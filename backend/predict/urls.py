from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PredictView

urlpatterns = [
    path('train-predict-model/', PredictView.as_view(), name='predict'),
]
