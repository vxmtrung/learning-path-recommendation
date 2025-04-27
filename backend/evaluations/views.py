from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import evalAll, getPathEvaluationForStudent
import pandas as pd
import json
        
# Create your views here.
class AllEvaluationsAPIView(APIView):
    def get(self, request):
        res = evalAll()
        if isinstance(res, str):
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        return Response(json.loads(res.to_json(orient="records")), status=status.HTTP_200_OK)

class StudentEvaluationAPIView(APIView):
    def get(self, request, student_id):
        if not student_id: 
           return Response("Please provide student id", status=status.HTTP_400_BAD_REQUEST)

        res = getPathEvaluationForStudent(student_id)
        if isinstance(res, str):
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        return Response(json.loads(res.to_json(orient="records")), status=status.HTTP_200_OK)
    
class EvaluationsAPIView(APIView):
  def get(self, request, student_id=None):
    if student_id is None:
      res = evalAll()
      if isinstance(res, str):
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
      return Response(json.loads(res.to_json(orient="records")), status=status.HTTP_200_OK)
    else:
      res = getPathEvaluationForStudent(student_id)
      if isinstance(res, str):
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
      return Response(json.loads(res.to_json(orient="records")), status=status.HTTP_200_OK)
    