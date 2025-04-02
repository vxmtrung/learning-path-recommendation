from django.urls import path, include
from .views import EvaluationsAPIView, AllEvaluationsAPIView, StudentEvaluationAPIView

urlpatterns = [
  path("all", AllEvaluationsAPIView.as_view(), name="overall-evaluations"),
  path("<student_id>/", StudentEvaluationAPIView.as_view(), name="student-evaluations")
]