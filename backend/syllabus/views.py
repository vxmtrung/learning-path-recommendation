from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from syllabus.models import Syllabus
from syllabus.serializers import SyllabusSerializer
import csv
# Create your views here.
class SyllabusImportView(APIView):
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
            file_content = csv_file.read().decode('utf-8').splitlines()
        
            syllabus = []
            for row in file_content:
                chapter_data = row.split('|')
                if len(chapter_data) == 2:
                    syllabus_data = {
                        "name": chapter_data[0].strip(),
                        "course": chapter_data[1].strip(),
                    }

                    # Validate data using serializer
                    serializer = SyllabusSerializer(data=syllabus_data)
                    if serializer.is_valid():
                        syllabus.append(Syllabus(**serializer.validated_data))
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error": "Invalid data format in CSV file."}, status=status.HTTP_400_BAD_REQUEST)


            # Bulk create majors in database
            Syllabus.objects.bulk_create(syllabus)
            return Response({"status": "Import successful"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SyllabusListView(APIView):
    def post(self, request, *args, **kwargs):
        input_data = request.data
        syllabus = Syllabus.objects.filter(course = input_data["course_code"])
        return Response(SyllabusSerializer(syllabus, many=True).data, status=status.HTTP_200_OK)