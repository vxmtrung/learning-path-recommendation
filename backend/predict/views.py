from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from students.views import get_all_student
from courses.views import get_all_course
from learnlog.views import get_learn_log

import pandas as pd
import numpy as np

from predict.model_predict import CF

import pickle
# Create your views here.
class PredictView(APIView):
    def get(self, request, *args, **kwargs):
        # Get all student
        student_data = get_all_student()
        student_data = [student.student_id for student in student_data]
      
        # Get all course
        course_data = get_all_course()
        course_data = [course.course_code for course in course_data]
        
        # Get learn log
        learn_log = get_learn_log()
        learn_log = [log for log in learn_log if log.learned == True]
        
        student_course_matrix = pd.DataFrame(np.nan, index=student_data, columns=course_data)
        
        # Fill in the score from the learnlog
        for log in learn_log:
            student_course_matrix.at[log.student_id, log.course_id] = float(log.score) if log.score else 10
            
        data = []
        for student in student_data:
            for course in course_data:
                score = student_course_matrix.at[student, course]
                if not np.isnan(score):
                    data.append([int(student), course, float(score)])
                else:
                    data.append([int(student), course, None])
        
        data = np.array(data)
     
        student_ids = {v: i for i, v in enumerate(np.unique(data[:, 0]))}

        course_ids = {v: i for i, v in enumerate(np.unique(data[:, 1]))}
        for i in range(len(data)):
            data[i, 0] = student_ids[data[i, 0]]
            data[i, 1] = course_ids[data[i, 1]]
            
        rs = CF(data, k = 100, uuCF = 1, students=student_data, courses=course_data)
        rs.fit()
        
        with open('model.pkl', 'wb') as f:
            pickle.dump(rs, f)
        return Response({"status": "Train successful"}, status=status.HTTP_201_CREATED)
        
def predict_score(student_id, course_list):
    # Get all student
    student_data = get_all_student()
    student_data = [student.student_id for student in student_data]
    
    # Get all course
    course_data = get_all_course()
    course_data = [course.course_code for course in course_data]
    
    # Get learn log
    learn_log = get_learn_log()
    learn_log = [log for log in learn_log if log.learned == True]
    
    student_course_matrix = pd.DataFrame(np.nan, index=student_data, columns=course_data)
    
    # Fill in the score from the learnlog
    for log in learn_log:
        student_course_matrix.at[log.student_id, log.course_id] = float(log.score) if log.score else 10
        
    data = []
    for student in student_data:
        for course in course_data:
            score = student_course_matrix.at[student, course]
            if not np.isnan(score):
                data.append([int(student), course, float(score)])
            else:
                data.append([int(student), course, None])
    
    data = np.array(data)
    student_ids = {v: i for i, v in enumerate(np.unique(data[:, 0]))}
    course_ids = {v: i for i, v in enumerate(np.unique(data[:, 1]))}
    
    with open("model.pkl", "rb") as f:
        loaded_model = pickle.load(f)
    return [{"course_id": course.course_code, "score": float(loaded_model.pred(student_ids[int(student_id)], course_ids[course.course_code], 0))} for course in course_list]