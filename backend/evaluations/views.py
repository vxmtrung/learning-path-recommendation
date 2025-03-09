from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import evaluateRecommendationPathForSystem
import pandas as pd

# Create your views here.
class EvaluationsAPIView(APIView):
  def get(self, request, *args, **kwargs):
    res = evaluateRecommendationPathForSystem()

    return Response(res, status=status.HTTP_200_OK)