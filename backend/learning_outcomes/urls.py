from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LearningOutcomesView

urlpatterns = [
    path('import/', LearningOutcomesView.as_view(), name='learning-outcomes-import'),
]