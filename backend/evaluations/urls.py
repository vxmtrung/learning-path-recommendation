from django.urls import path, include
from .views import EvaluationsAPIView

urlpatterns = [
  path("evaluations/", EvaluationsAPIView.as_view(), name="overall-evaluations"),
  path("evaluations/<student_id>/", EvaluationsAPIView.as_view(), name="student-evaluations")
]