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
                # alternative_group_id = None
                # if row[6]:
                #     alternative_group_id = GroupCourse.objects.get(group_course_code=row[6])
                group_course_data = {
                    "group_course_code": row[0],
                    "group_course_name": row[1],
                    "total_course": row[2],
                    "minimum_course": row[3],
                    "alternative": row[4],
                    "specifically": row[5],
                    "alternative_group": row[6],
                    "mandatory": row[7],
                }
                
                serializer = GroupCourseSerializer(data=group_course_data)
                if serializer.is_valid():
                    # Insert data into database
                    group = GroupCourse(**serializer.validated_data)
                    group.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({"status": "Import successful"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GroupCourseGetView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            group_courses = GroupCourse.objects.filter(is_active=True)
            serializer = GroupCourseSerializer(group_courses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GroupCourse.DoesNotExist:
            return Response({"error": "Group course not found."}, status=status.HTTP_404_NOT_FOUND)
        
class AddGroupCourseView(APIView):
    def post(self, request, *args, **kwargs):
        group_course_code = request.data.get('group_course_code')
        group_course_name = request.data.get('group_course_name')
        
        try:
            group_course = GroupCourse(group_course_code=group_course_code, group_course_name=group_course_name)
            group_course.save()
            return Response({"status": "Group course added successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UpdateGroupCourseView(APIView):
    def post(self, request, *args, **kwargs):
        group_course_id= request.query_params.get('group_course_id')
        group_course_name = request.data.get('group_course_name')
        
        try:
            group_course = GroupCourse.objects.get(group_course_id=group_course_id, is_active=True)
            group_course.group_course_name = group_course_name
            group_course.save()
            return Response({"status": "Update successful"}, status=status.HTTP_200_OK)
        except GroupCourse.DoesNotExist:
            return Response({"error": "Group course not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DeleteGroupCourseView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            group_course_id = request.query_params.get('group_course_id')
            group_course = GroupCourse.objects.get(group_course_id=group_course_id, is_active=True)
            group_course.is_active = False
            group_course.save()
            return Response({"status": "Group course deleted successfully"}, status=status.HTTP_200_OK)
        except GroupCourse.DoesNotExist:
            return Response({"error": "Group course not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)