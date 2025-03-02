from django.shortcuts import render

import csv
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from learnlog.models import LearnLog
from learnlog.serializers import LearnLogSerializer
# Create your views here.

class LearnlogImportView(APIView):
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

            learnlogs = []
            for row in csv_reader:
                
                learnlog_data = {
                    "student": row[0],
                    "course": row[1],
                    "score": None if row[2] == 'MT' else row[2],            
                    "count_learn": row[3],
                    "semester": row[4]
                }
                
                serializer = LearnLogSerializer(data=learnlog_data)
                if serializer.is_valid():
                    learnlogs.append(LearnLog(**serializer.validated_data))
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Bulk create majors in database
            LearnLog.objects.bulk_create(learnlogs)
            return Response({"status": "Import successful"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
def get_learn_log():
    return LearnLog.objects.all()