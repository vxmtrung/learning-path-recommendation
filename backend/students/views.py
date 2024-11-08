from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import csv

from students.models import Student
from students.serializers import StudentSerializer
# Create your views here.
class StudentImportView(APIView):
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

            student = []
            for row in csv_reader:
        
                student_data = {
                    "student_id": row[0],
                    "student_name": row[1],
                    "student_email": row[2],            
                    "english_level": row[3],
                    "faculty": row[4],
                    "GPA": row[5]
                }
                
                serializer = StudentSerializer(data=student_data)
                if serializer.is_valid():
                    student.append(Student(**serializer.validated_data))
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Bulk create majors in database
            Student.objects.bulk_create(student)
            return Response({"status": "Import successful"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)