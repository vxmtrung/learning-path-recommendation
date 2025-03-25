from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import evalAll, getPathEvaluationForStudent
import pandas as pd
import json

# Create your views here.
class EvaluationsAPIView(APIView):
  def get(self, request, student_id=None):
    if student_id is None:
      res = evalAll()
      return Response(json.loads(res.to_json(orient="records")), status=status.HTTP_200_OK)
    else:
      res = getPathEvaluationForStudent(student_id)
      if isinstance(res, str):
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
      return Response(json.loads(res.to_json(orient="records")), status=status.HTTP_200_OK)