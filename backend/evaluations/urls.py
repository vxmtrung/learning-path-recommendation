from django.urls import path, include
from .views import EvaluationsAPIView

urlpatterns = [
  path("evaluations/", EvaluationsAPIView.as_view(), name="evaluation-list")
]