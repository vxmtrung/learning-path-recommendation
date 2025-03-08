from django.shortcuts import render

import csv

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from learning_outcomes.models import Learning_Outcome
from learning_outcomes.serializers import LearningOutcomeSerializer
# Create your views here.
class LearningOutcomesView(APIView):
    def post(self, request, *args, **kwargs):
        # get file from request
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response({"error": "File not provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Check file format
        if not csv_file.name.endswith('.csv'):
            return Response({"error": "Invalid file format. Please upload a CSV file."}, status=status.HTTP_400_BAD_REQUEST)

        # Read CSV file
        try:
            csv_reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
            next(csv_reader) 
            
            learning_outcomes = []
            for row in csv_reader:
                
                learning_outcome_data = {
                    "learning_outcome_code": row[0],
                    "content_vn": row[1],
                    "content_en": row[2],
                    "course": row[3],
                }
                
                serializer = LearningOutcomeSerializer(data=learning_outcome_data)
                if serializer.is_valid():
                    learning_outcomes.append(Learning_Outcome(**serializer.validated_data))
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Bulk create majors in database
            Learning_Outcome.objects.bulk_create(learning_outcomes)
            return Response({"status": "Import successful"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)