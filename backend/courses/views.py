from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import generics

from majors.models import Major


from .models import Course
from .serializers import CourseSerializer
import csv
from group_course.models import GroupCourse

# Create your views here.


class CourseImportView(APIView):
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

            courses = []
            for row in csv_reader:
                print(row[0])
                print(row[8])
                major_ids = row[2].split('|') if row[2] else []
                group_course = get_object_or_404(GroupCourse, group_course_code=row[8]) if row[8] else None
                course_data = {
                    "course_code": row[0],
                    "course_name": row[1],
                    "prerequisites": row[3],
                    "semester": row[4],
                    "count_learner": row[5],
                    "average_score": 12 if row[6] == 'MT' else row[6],
                    "credit": row[7],
                    "group_course": group_course.group_course_code if group_course else None,
                    "note": None,
                    "description": None
                }
                
                serializer = CourseSerializer(data=course_data)
                if serializer.is_valid():
                    course = Course(**serializer.validated_data)
                    course.save()
                    course.majors.set(major_ids)
                    courses.append(course)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Bulk create courses in database
            # Course.objects.bulk_create(courses)
            return Response({"status": "Import successful"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
def get_courses_by_major(majors_list):
    try:
        majors = Major.objects.filter(major_id__in=majors_list)
        courses = Course.objects.filter(majors__in=majors).order_by('semester', 'group_course').distinct().prefetch_related('majors')
        return courses
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_all_course():
    try:
        return Course.objects.all()
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
