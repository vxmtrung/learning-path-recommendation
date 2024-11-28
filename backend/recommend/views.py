import json
from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.views import get_courses_by_major
from learnlog.views import get_learn_log
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
        scores = predict_score(input_data['student_id'], course_list)
        
        score_dict = {item['course_id']: item['score'] for item in scores}
        for course in course_list:
            raw_score = score_dict.get(course.course_code, None)
            if raw_score is not None:
                course.predict_score = float(Decimal(raw_score).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
            else:
                course.predict_score = None
            
        # Get learn log
        learn_log = get_learn_log()
        learn_log = [log for log in learn_log if log.learned == True]
        
        
        # Get course group c in course list
        course_group_c = [course for course in course_list if course.is_group_c]
    
        # Get last 3 semester
        last_3_semester = self.get_last_3_semester(int(input_data['current_semester']))
        
        # Filter group c subjects studied in the last 3 semesters and had the highest prediction score
        course_group_c = self.resort_course_group_c(course_group_c, last_3_semester, learn_log)
        # for course in course_group_c:
        #     print(f"{course.course_name} ({course.course_code}) - Predict Score: {course.predict_score} - Note: {course.note}")
        
        ### Replace the group c subjects in the course list with the group c subjects that have been studied in the last 3 semesters
        course_list = self.replace_sublistcourse(course_list, course_group_c)
    
        # Get learner log from learn log
        learner_log = [log for log in learn_log if log.student_id == input_data['student_id']]
        
        # Create Course Graph
        course_tree = CourseTree.create_course_tree(course_list)
         
        # Recommend Learing Path 
        learner = {
            "english_level": input_data['english_level'],
            "learn_summer_semester": input_data['learn_summer_semester'],
            "credit_summer_semester": input_data['credit_summer_semester'],
            "course_free_elective": input_data['course_free_elective'],
            "over_learn": input_data['over_learn'],
            "over_learn_credit": input_data['over_learn_credit']
        }
        learning_path_recommend = Recommend.recommend(learner, learner_log, course_list, course_tree, int(input_data['current_semester']))
    
        self.print_learning_path(learning_path_recommend)
        # Convert learning path to dictionary format
        learning_path_data = {"learning_path": [element.to_dict() for element in learning_path_recommend]}
        
        # Add log
        recommend_logs = []
        recommend_log = {
            "student": input_data['student_id'],
            "learning_path": json.dumps(learning_path_data)
        }
        serializer = RecommendLogSerializer(data=recommend_log)
        if serializer.is_valid():
            recommend_logs.append(RecommendLog(**serializer.validated_data))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        RecommendLog.objects.bulk_create(recommend_logs)
        
        # Return JsonResponse with pretty JSON formatting
        return JsonResponse(learning_path_data, json_dumps_params={'indent': 4, 'ensure_ascii': False})


    def get_last_3_semester(self, current_semester):
        if current_semester % 10 == 1:
            return [current_semester - 20 + 1, current_semester - 10, current_semester - 10 + 1]
        if current_semester % 10 == 2:
            return [current_semester - 10 - 1, current_semester - 10, current_semester - 1]
        if current_semester % 10 == 3:
            return [current_semester - 10 - 1, current_semester - 2, current_semester - 1]

    def resort_course_group_c(self, course_group_c, last_3_semester, learn_log):
        course_group_c_resort = []
        course_group_c_not_in_last_3_semester = []
        for course in course_group_c:
            check = False
            for log in learn_log:
                if course.course_id == log.course.course_id and int(log.semester) in last_3_semester:
                    course_group_c_resort.append(course)
                    check = True
                    break
            if not check:
                course.note = "Mon hoc chua duoc mo trong 3 hoc ky chinh gan nhat"
                course_group_c_not_in_last_3_semester.append(course)
        course_group_c_resort.sort(key=lambda x: x.predict_score, reverse=True)
        course_group_c_not_in_last_3_semester.sort(key=lambda x: x.predict_score, reverse=True)
        return course_group_c_resort + course_group_c_not_in_last_3_semester

    def replace_sublistcourse(self, course_list, course_group_c):
        course_list = list(course_list)
        indices = [course_list.index(course) for course in course_group_c if course in course_list]
        if len(indices) == 0:
            print("Không có phần tử nào trong course_list giống với course_group_c.")
            return course_list
        elif len(indices) == 1:
            return course_list
        elif len(indices) == 2:
            if indices[0] + 1 == indices[1]:
                start = indices[0]
                end = indices[1]
                course_list[start:end + 1] = course_group_c
        else:
            start = indices[0]
            end = indices[-1]
            course_list[start:end + 1] = course_group_c
        return course_list
        
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
