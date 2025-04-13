from django.shortcuts import render
import csv
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Faculty
from .serializers import FacultySerializer
# Create your views here.
    
class FacultyImportView(APIView):
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

            faculties = []
            for row in csv_reader:
                faculty_data = {"faculty_code": row[0], "faculty_name": row[1]}
                serializer = FacultySerializer(data=faculty_data)
                if serializer.is_valid():
                    faculties.append(Faculty(**serializer.validated_data))
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Bulk create faculties in database
            Faculty.objects.bulk_create(faculties)
            return Response({"status": "Import successful"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetFacultyView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            faculties = Faculty.objects.filter(is_active=True)
            serializer = FacultySerializer(faculties, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddFacultyView(APIView):
    def post(self, request, *args, **kwargs):
        faculty_code = request.data.get('faculty_code')
        faculty_name = request.data.get('faculty_name')
        try:
            faculty = Faculty(faculty_code=faculty_code, faculty_name=faculty_name)
            faculty.save()
            return Response({"status": "Faculty added successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UpdateFacultyView(APIView):
    def post(self, request, *args, **kwargs):
        faculty_id = request.query_params.get('faculty_id')
        faculty_name = request.data.get('faculty_name')
        try:
            faculty = Faculty.objects.get(faculty_id=faculty_id, is_active=True)
            faculty.faculty_name = faculty_name
            faculty.save()
            return Response({"status": "Update successful"}, status=status.HTTP_200_OK)
        except Faculty.DoesNotExist:
            return Response({"error": "Faculty not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DeleteFacultyView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            faculty_id = request.query_params.get('faculty_id')
            faculty = Faculty.objects.get(faculty_id=faculty_id, is_active=True)
            faculty.is_active = False
            faculty.save()
            return Response({"status": "Faculty deleted successfully"}, status=status.HTTP_200_OK)
        except Faculty.DoesNotExist:
            return Response({"error": "Faculty not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    