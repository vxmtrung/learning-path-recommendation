from django.shortcuts import render
from io import TextIOWrapper
import csv
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from learnlog.models import LearnLog
from learnlog.serializers import LearnLogSerializer
from students.models import Student
from courses.models import Course
# Create your views here.
import pickle
class LearnlogImportView(APIView):
    def post(self, request, *args, **kwargs):
        # get file from request
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response({"error": "File not provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Check file format
        if not csv_file.name.endswith('.csv'):
            return Response({"error": "Invalid file format. Please upload a CSV file."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Đọc file CSV với TextIOWrapper để tránh lỗi encoding và dùng streaming
            csv_reader = csv.reader(TextIOWrapper(csv_file, encoding='utf-8'))
            next(csv_reader)  # Bỏ qua header

            learnlogs = []
            batch_size = 5000  # Tùy chỉnh batch size theo database của bạn

            for row in csv_reader:
                student = Student.objects.get(student_code=row[0])
                course = Course.objects.get(course_code=row[1])
                learnlog_data = {
                    "student": student,
                    "course": course,
                    "score": 10 if row[2] == 'MT' else row[2],            
                    "count_learn": row[3],
                    "semester": row[4]
                }

                learnlogs.append(LearnLog(**learnlog_data))

                # Khi danh sách đạt batch_size, insert vào DB
                if len(learnlogs) >= batch_size:
                    LearnLog.objects.bulk_create(learnlogs)
                    learnlogs.clear()

            # Insert phần còn lại nếu có
            if learnlogs:
                LearnLog.objects.bulk_create(learnlogs)

            return Response({"status": "Import successful"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
def get_learn_log():
    return LearnLog.objects.all()

class ImportGradeView(APIView):
    def post(self, request, *args, **kwargs):
        # get file from request
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response({"error": "File not provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Check file format
        if not csv_file.name.endswith('.csv'):
            return Response({"error": "Invalid file format. Please upload a CSV file."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Đọc file CSV với TextIOWrapper để tránh lỗi encoding và dùng streaming
            csv_reader = csv.reader(TextIOWrapper(csv_file, encoding='utf-8'))
            next(csv_reader)  # Bỏ qua header

            learnlogs = []
            batch_size = 5000  # Tùy chỉnh batch size theo database của bạn

            for row in csv_reader:
                student = Student.objects.get(student_code=row[0])
                course = Course.objects.get(course_code=row[1])
                learnlog_data = {
                    "student": student,
                    "course": course,
                    "score": 10 if row[2] == 'MT' else row[2],            
                    "count_learn": row[3],
                    "semester": row[4]
                }

                learnlogs.append(LearnLog(**learnlog_data))

                if float(learnlog_data["score"]) < 5:
                    print(f"Student {learnlog_data['student'].student_name} failed {learnlog_data['course'].course_name} with score {learnlog_data['score']}")
                    print(f"Student {learnlog_data['student'].student_name} need to learn this below courses:")
                    try:
                        with open("course_similarity.pkl", "rb") as f:
                            course_similarities = pickle.load(f)
                        similar_courses = sorted(course_similarities.get(learnlog_data['course'].course_code, {}).items(), key=lambda x: x[1], reverse=True)[:10]
                        count_course = 0
                       
                        for rcm_course_code, similarity in similar_courses:
                            rcm_course = Course.objects.get(course_code=rcm_course_code)
                            if rcm_course.semester <= course.semester:
                                print(f"{rcm_course.course_name} - {rcm_course_code} - {similarity}")
                                count_course += 1
                                if count_course == 5:
                                    break

                    except Exception as e:
                        print(str(e))
                        
                # Khi danh sách đạt batch_size, insert vào DB
                # if len(learnlogs) >= batch_size:
                #     LearnLog.objects.bulk_create(learnlogs)
                #     learnlogs.clear()

            # Insert phần còn lại nếu có
            # if learnlogs:
            #     LearnLog.objects.bulk_create(learnlogs)

            return Response({"status": "Import successful"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)