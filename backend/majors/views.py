from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Major
from .serializers import MajorSerializer
from faculties.models import Faculty
import csv
# Create your views here.
class MajorImportView(APIView):
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

            majors = []
            for row in csv_reader:
                faculty = get_object_or_404(Faculty, faculty_code=row[2])
                major_data = {"major_code": row[0], "major_name": row[1], "faculty": faculty.faculty_code}
                serializer = MajorSerializer(data=major_data)
                if serializer.is_valid():
                    majors.append(Major(**serializer.validated_data))
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Bulk create majors in database
            Major.objects.bulk_create(majors)
            return Response({"status": "Import successful"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class MajorListView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            input_data = request.data
            majors = Major.objects.filter(faculty = input_data["faculty"])
            return Response(MajorSerializer(majors, many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)