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
    
class GetCourseView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            course = Course.objects.filter(is_active=True)
            serializer = CourseSerializer(course, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddCourseView(APIView):
    def post(self, request, *args, **kwargs):
        course_code = request.data.get('course_code')
        course_name = request.data.get('course_name')
        semester = request.data.get('semester')
        count_learner = request.data.get('count_learner')
        average_score = request.data.get('average_score')
        credit = request.data.get('credit')
        note = request.data.get('note')
        description = request.data.get('description')
        major_ids = request.data.get('majors').split('|')
        try:
            course = Course(course_code=course_code, course_name=course_name, semester=semester, count_learner=count_learner, average_score=average_score, credit=credit, note=note, description=description)
            course.save()
            majors = Major.objects.filter(major_id__in=major_ids)
            course.majors.set(majors)
            return Response({"status": "Course added successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UpdateCourseView(APIView):
    def post(self, request, *args, **kwargs):
        course_code = request.query_params.get('course_code')
        course_name = request.data.get('course_name')
        semester = request.data.get('semester')
        credit = request.data.get('credit')
        description = request.data.get('description')
        prerequisites = request.data.get('prerequisites')
        major_ids = request.data.get('majors').split('|')
        try:
            course = Course.objects.get(course_code=course_code, is_active=True)
            if not course:
                return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
            
            course.course_code = course_code
            course.course_name = course_name
            course.semester = semester
            course.credit = credit
            course.description = description
            course.prerequisites = prerequisites
            majors = Major.objects.filter(major_id__in=major_ids)
            course.majors.set(majors)
            course.save()
            return Response({"status": "Course updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DeleteCourseView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            course_code = request.query_params.get('course_code')
            course = Course.objects.get(course_code=course_code, is_active=True)
            if not course:
                return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
            
            course.is_active = False
            course.save()
            return Response({"status": "Course deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetCoureByGroupCourseView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            group_course_code = request.query_params.get('group_course_code')
            group_course = GroupCourse.objects.get(group_course_code=group_course_code, is_active=True)
            courses = Course.objects.filter(group_course=group_course, is_active=True)
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AddCourseToGroupCourseView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            group_course_code = request.data.get('group_course_code')
            course_code = request.data.get('course_code')
            
            group_course = GroupCourse.objects.get(group_course_code=group_course_code, is_active=True)
            course = Course.objects.get(course_code=course_code, is_active=True)
            
            course.group_course = group_course
            course.save()
            
            return Response({"status": "Courses added to group course successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RemoveCourseFromGroupCourseView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            group_course_code = request.data.get('group_course_code')
            course_code = request.data.get('course_code')
            
            # group_course = GroupCourse.objects.get(group_course_code=group_course_code, is_active=True)
            course = Course.objects.get(course_code=course_code, is_active=True)
    
            course.group_course = None
            course.save()
            
            return Response({"status": "Courses removed from group course successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)