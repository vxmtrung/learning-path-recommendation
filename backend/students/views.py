from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import csv

from students.models import Student
from students.serializers import StudentSerializer
from faculties.models import Faculty
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
                faculty = get_object_or_404(Faculty, faculty_code=row[4])
                student_data = {
                    "student_code": row[0],
                    "student_name": row[1],
                    "student_email": row[2],            
                    "english_level": row[3],
                    "faculty": faculty.faculty_code,
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
        
def get_all_student():
    try:
        return Student.objects.all()
    except Student.DoesNotExist:
        return None

class StudentListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            students = Student.objects.filter(is_active=True)
            if not students:
                return Response({"error": "No students found."}, status=status.HTTP_404_NOT_FOUND)
            return Response(StudentSerializer(students, many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
    def post(self, request, *args, **kwargs):
        try:
            input_data = request.data
            student = Student.objects.filter(student_code = input_data["student_id"], is_active=True)
            return Response(StudentSerializer(student, many=True).data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
        
class AddStudentView(APIView):
    def post(self, request, *args, **kwargs):
        student_code = request.data.get('student_code')
        student_name = request.data.get('student_name')
        student_email = request.data.get('student_email')
        english_level = request.data.get('english_level')
        faculty_code = request.data.get('faculty_code')
        GPA = request.data.get('GPA')

        try:
            faculty = get_object_or_404(Faculty, faculty_code=faculty_code)
            if faculty is None:
                return Response({"error": "Faculty not found"}, status=status.HTTP_404_NOT_FOUND)
            student = Student(student_code=student_code, student_name=student_name, student_email=student_email,
                              english_level=english_level, faculty=faculty, GPA=GPA)
            student.save()
            return Response({"status": "Student added successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UpdateStudentView(APIView):
    def post(self, request, *args, **kwargs):
        student_code = request.query_params.get('student_code')
        student_name = request.data.get('student_name')
        faculty_code = request.data.get('faculty_code')

        try:
            student = get_object_or_404(Student, student_code=student_code)
            faculty = get_object_or_404(Faculty, faculty_code=faculty_code)
            if faculty is None:
                return Response({"error": "Faculty not found"}, status=status.HTTP_404_NOT_FOUND)
            student.student_name = student_name
            student.faculty = faculty
            student.save()

            return Response({"status": "Student updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DeleteStudentView(APIView):   
    def get(self, request, *args, **kwargs):
        try:
            student_code = request.query_params.get('student_code')
            student = get_object_or_404(Student, student_code=student_code)
            student.is_active = False
            student.save()
            return Response({"status": "Student deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)