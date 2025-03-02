from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import generics

from .models import GroupCourse
from .serializers import GroupCourseSerializer
import csv

# Create your views here.


class GroupCourseImportView(APIView):
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

            group_courses = []
            for row in csv_reader:
                group_course_data = {
                    "group_course_code": row[0],
                    "group_course_name": row[1],
                    "total_course": row[2],
                    "minimum_course": row[3]
                }
                
                serializer = GroupCourseSerializer(data=group_course_data)
                if serializer.is_valid():
                    group_courses.append(GroupCourse(**serializer.validated_data))
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Bulk create courses in database
            GroupCourse.objects.bulk_create(group_courses)
            
            return Response({"status": "Import successful"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GroupCourseGetView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            group_courses = GroupCourse.objects.all()
            serializer = GroupCourseSerializer(group_courses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GroupCourse.DoesNotExist:
            return Response({"error": "Group course not found."}, status=status.HTTP_404_NOT_FOUND)
