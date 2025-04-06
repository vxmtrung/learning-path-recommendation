import json
import os
import pytz
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.views import get_courses_by_major
from learnlog.views import get_learn_log, get_learn_log_by_semester
from predict.views import predict_score

import recommend.course_tree as CourseTree
import recommend.recommend as Recommend

from decimal import Decimal, ROUND_HALF_UP

from recommendlogs.models import RecommendLog
from recommendlogs.serializers import RecommendLogSerializer

from rest_framework import status
# Create your views here.
class RecommendView(APIView):
    def post(self, request, *args, **kwargs):
        # Get data from request
        input_data = request.data
        
        # Get course list by major
        course_list = get_courses_by_major(input_data['major'])

        # Get predict score
        scores = predict_score(input_data['student_id'], course_list)
        
        # Add predict score to course list
        score_dict = {item['course_id']: item['score'] for item in scores}
        for course in course_list:
            raw_score = score_dict.get(course.course_code, None)
            if raw_score is not None:
                course.predict_score = float(Decimal(raw_score).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
            else:
                course.predict_score = None
            
        # Get learn log
        learn_log = get_learn_log()
        learn_log = [log for log in learn_log if log.score]
    
        # Get learner log from learn log
        learner_log = [log for log in learn_log if log.student_id == input_data['student_id']]
        
        english_level = 0
        seen_courses = set()

        for log in learner_log:
            if log.course.group_course.group_course_code == "group_english":
                course_code = log.course.course_code  # hoặc log.course.id
                if course_code not in seen_courses:
                    seen_courses.add(course_code)
                    english_level += 1
        
        # Create Course Graph
        course_tree = CourseTree.create_course_tree(course_list)
        
        # Recommend Learing Path 
        learner = {
            "english_level": english_level,
            "learn_summer_semester": input_data.get("learn_summer_semester", None),
            "summer_semester": input_data.get("summer_semester", []), 
            "group_free_elective": input_data.get("group_free_elective", None),
            "over_learn": input_data.get("over_learn", None),
            "main_semester": input_data.get("main_semester", []),
            "learn_to_improve": input_data.get("learn_to_improve", None),
            "major": input_data.get("major", None),
        }
        try:
            learning_path_recommend = Recommend.recommend(learner, learner_log, course_list, course_tree, int(input_data['next_semester']))
        except Exception as e:
            return JsonResponse({"error": "Recommend error", "details": str(e)}, status=400)
        
        self.print_learning_path(learning_path_recommend)
        # Convert learning path to dictionary format
        learning_path_data = {"learning_path": [element.to_dict() for element in learning_path_recommend]}
        
        ### Add log
        try:
            old_logs = RecommendLog.objects.filter(student_id=input_data['student_id'], is_active=True)
            for log in old_logs:
                log.is_active = False
                log.save()
                
            # get path to logs folder
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            logs_dir = os.path.join(parent_dir, 'logs')
            student_folder = os.path.join(logs_dir, input_data['student_id'])
            
            # create logs folder if not exist
            os.makedirs(logs_dir, exist_ok=True)
            os.makedirs(student_folder, exist_ok=True)
            
            vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")
            current_datetime = datetime.now(vietnam_tz).strftime("%Y%m%d_%H%M%S")
        

            file_path = os.path.join(student_folder, f"{input_data['student_id']}_{current_datetime }.txt")
            with open(file_path, 'w', encoding='utf-8') as f:  # Đảm bảo hỗ trợ Unicode
                json.dump(learning_path_data, f, indent=4, ensure_ascii=False)
            
            recommend_logs = []
            recommend_log = {
                "student": input_data['student_id'],
                "log_file_name": f"{input_data['student_id']}_{current_datetime }.txt",
                "is_active": True,
            }
            serializer = RecommendLogSerializer(data=recommend_log)
            if serializer.is_valid():
                recommend_logs.append(RecommendLog(**serializer.validated_data))
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            RecommendLog.objects.bulk_create(recommend_logs)
        except Exception as e:
            return JsonResponse({"error": "Save log error", "details": str(e)}, status=400)
        
        # Return JsonResponse with pretty JSON formatting
        return JsonResponse(learning_path_data, json_dumps_params={'indent': 4, 'ensure_ascii': False})
        
    def print_learning_path(self, learning_path_recommend):
        try:
            for semester in learning_path_recommend:
                print("----------" + str(semester.semester) + "-----------------")
                for course in semester.courses:
                    print(course.course_name)
                    # if course.note:
                    #     print(course.course_name + " - " + course.note)
                    # else:
                    #     print(course.course_name)
                print("Tong so tin chi trong hoc ky: " + str(semester.credit))
            print("")
        except:
            print(learning_path_recommend)


class RecommendEvaluationView(APIView):
    def post(self, request, *args, **kwargs):
        # Get data from request
        input_data = request.data
        
        # Get course list by major
        course_list = get_courses_by_major(input_data['major'])

        # Get predict score
        scores = predict_score(input_data['student_id'], course_list)
        
        # Add predict score to course list
        score_dict = {item['course_id']: item['score'] for item in scores}
        for course in course_list:
            raw_score = score_dict.get(course.course_code, None)
            if raw_score is not None:
                course.predict_score = float(Decimal(raw_score).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
            else:
                course.predict_score = None
            
        # Get learn log
        learn_log = get_learn_log_by_semester(int(input_data['next_semester']))
        learn_log = [log for log in learn_log if log.score]
    
        # Get learner log from learn log
        learner_log = [log for log in learn_log if log.student_id == input_data['student_id']]
        
        english_level = 0
        seen_courses = set()

        for log in learner_log:
            if log.course.group_course.group_course_code == "group_english":
                course_code = log.course.course_code  # hoặc log.course.id
                if course_code not in seen_courses:
                    seen_courses.add(course_code)
                    english_level += 1
        
        # Create Course Graph
        course_tree = CourseTree.create_course_tree(course_list)
        
        # Recommend Learing Path 
        learner = {
            "english_level": english_level,
            "learn_summer_semester": input_data.get("learn_summer_semester", None),
            "summer_semester": input_data.get("summer_semester", []), 
            "group_free_elective": input_data.get("group_free_elective", None),
            "over_learn": input_data.get("over_learn", None),
            "main_semester": input_data.get("main_semester", []),
            "learn_to_improve": input_data.get("learn_to_improve", None),
            "major": input_data.get("major", None),
        }
        try:
            learning_path_recommend = Recommend.recommend(learner, learner_log, course_list, course_tree, int(input_data['next_semester']))
        except Exception as e:
            return JsonResponse({"error": "Recommend error", "details": str(e)}, status=400)
        
        self.print_learning_path(learning_path_recommend)
        # Convert learning path to dictionary format
        learning_path_data = {"learning_path": [element.to_dict() for element in learning_path_recommend]}
        
        ### Add log
        try:
            old_logs = RecommendLog.objects.filter(student_id=input_data['student_id'], is_active=True)
            for log in old_logs:
                log.is_active = False
                log.save()
                
            # get path to logs folder
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            logs_dir = os.path.join(parent_dir, 'logs')
            student_folder = os.path.join(logs_dir, input_data['student_id'])
            
            # create logs folder if not exist
            os.makedirs(logs_dir, exist_ok=True)
            os.makedirs(student_folder, exist_ok=True)
            
            vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")
            current_datetime = datetime.now(vietnam_tz).strftime("%Y%m%d_%H%M%S")
        

            file_path = os.path.join(student_folder, f"{input_data['student_id']}_{current_datetime }.txt")
            with open(file_path, 'w', encoding='utf-8') as f:  # Đảm bảo hỗ trợ Unicode
                json.dump(learning_path_data, f, indent=4, ensure_ascii=False)
            
            recommend_logs = []
            recommend_log = {
                "student": input_data['student_id'],
                "log_file_name": f"{input_data['student_id']}_{current_datetime }.txt",
                "is_active": True,
            }
            serializer = RecommendLogSerializer(data=recommend_log)
            if serializer.is_valid():
                recommend_logs.append(RecommendLog(**serializer.validated_data))
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            RecommendLog.objects.bulk_create(recommend_logs)
        except Exception as e:
            return JsonResponse({"error": "Save log error", "details": str(e)}, status=400)
        
        # Return JsonResponse with pretty JSON formatting
        return JsonResponse(learning_path_data, json_dumps_params={'indent': 4, 'ensure_ascii': False})
        
    def print_learning_path(self, learning_path_recommend):
        try:
            for semester in learning_path_recommend:
                print("----------" + str(semester.semester) + "-----------------")
                for course in semester.courses:
                    print(course.course_name)
                    # if course.note:
                    #     print(course.course_name + " - " + course.note)
                    # else:
                    #     print(course.course_name)
                print("Tong so tin chi trong hoc ky: " + str(semester.credit))
            print("")
        except:
            print(learning_path_recommend)
