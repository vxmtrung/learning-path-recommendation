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

from learning_outcomes.models import Learning_Outcome
from learnlog.models import LearnLog

import pickle
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import matplotlib.pyplot as plt

# Create your views here.
class PredictView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Get all student and sort by student_code
            student_data = get_all_student()
            student_data = sorted([student.student_code for student in student_data])
               
            # Get all course
            course_data = get_all_course()
            course_data = sorted([course.course_code for course in course_data])
             
            # Get learn log
            learn_log = get_learn_log()
            learn_log = [log for log in learn_log if log.score and log.score <= 10 and log.score >= 0]
            
            student_course_matrix = pd.DataFrame(np.nan, index=student_data, columns=course_data)
            
            # Fill in the score from the learnlog
            for log in learn_log:
                student_course_matrix.at[log.student.student_code, log.course.course_code] = float(log.score)
               
            data = []
            for student in student_data:
                for course in course_data:
                    score = student_course_matrix.at[student, course]
                    if np.isnan(score):
                        data.append([int(student), course, None])
                    else:
                        data.append([int(student), course, float(score)])
            
            data = np.array(data)
        
            student_ids = {v: i for i, v in enumerate(np.unique(data[:, 0]))}

            course_ids = {v: i for i, v in enumerate(np.unique(data[:, 1]))}
            for i in range(len(data)):
                data[i, 0] = student_ids[data[i, 0]]
                data[i, 1] = course_ids[data[i, 1]]
                
            rs = CF(data, k = 1000, uuCF = 1, students=student_data, courses=course_data)
            rs.fit()
            with open('model.pkl', 'wb') as f:
                pickle.dump(rs, f)
            return Response({"status": "Train successful"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"status": "Train failed", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
  
class PredictBaseOnLearningOutcomeView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            model = SentenceTransformer("distiluse-base-multilingual-cased")
    
            all_courses = Learning_Outcome.objects.values_list("course__course_code", flat=True).distinct()
            course_embeddings = {}
            
            for course in all_courses:
                los = Learning_Outcome.objects.filter(course__course_code=course)
                if los:
                    embeddings = model.encode([lo.content_en for lo in los], batch_size=8, convert_to_numpy=True)
                    course_embeddings[course] = embeddings
                    
            course_similarities = {}
            for course_a, emb_a in course_embeddings.items():
                course_similarities[course_a] = {}
                for course_b, emb_b in course_embeddings.items():
                    if course_a != course_b:
                        similarities = util.cos_sim(emb_a, emb_b)
                        avg_similarity = similarities.numpy().mean()
                        course_similarities[course_a][course_b] = avg_similarity
            with open("course_similarity.pkl", "wb") as f:
                pickle.dump(course_similarities, f)
                
            return Response({"status": "Train successful"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"status": "Train failed", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)  
        
def predict_score(student_id, course_list):
    # Get all student
    student_data = get_all_student()
    student_data = sorted([student.student_code for student in student_data])

    # Get all course
    course_data = get_all_course()
    course_data = sorted([course.course_code for course in course_data])
    
    data = []
    for student in student_data:
        for course in course_data:
            data.append([int(student), course])
    
    data = np.array(data)
    student_ids = {v: i for i, v in enumerate(np.unique(data[:, 0]))}
    course_ids = {v: i for i, v in enumerate(np.unique(data[:, 1]))}
    
    with open("model.pkl", "rb") as f:
        loaded_model = pickle.load(f)
    return [{"course_id": course.course_code, "score": float(loaded_model.pred(student_ids[student_id], course_ids[course.course_code], 0, student_id, course.course_code))} for course in course_list]

class TestingAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Lấy learn log từ model LearnLog
            learn_log = LearnLog.objects.all()
            learn_log = sorted(learn_log, key=lambda x: x.semester)
            
      
            # Get all student
            student_data = get_all_student()
            student_data = sorted([student.student_code for student in student_data])

            # Get all course
            course_data = get_all_course()
            course_data = sorted([course.course_code for course in course_data])
  
            data = []
            for student in student_data:
                for course in course_data:
                    data.append([int(student), course])
                    
            data = np.array(data)
            student_ids = {v: i for i, v in enumerate(np.unique(data[:, 0]))}
            course_ids = {v: i for i, v in enumerate(np.unique(data[:, 1]))}
   
            with open("model.pkl", "rb") as f:
                loaded_model = pickle.load(f)
   
            year_data = {}
            for log in learn_log:
                predict_score = loaded_model.pred(
                    student_ids[log.student.student_code],
                    course_ids[log.course.course_code], 
                    0, log.student.student_code, log.course.course_code
                )
                
                # Xác định năm học từ mã học kỳ (VD: "201" -> "2020-2021")
                year = f"20{log.semester[:2]}-20{int(log.semester[:2]) + 1}"
                
                if year not in year_data:
                    year_data[year] = {"true": [], "predict": []}

                year_data[year]["true"].append(float(log.score))
                year_data[year]["predict"].append(float(predict_score))

            # Tính toán lỗi động
            results = {}
            for year, scores in year_data.items():
                if scores["true"] and scores["predict"]:
                    mae = mean_absolute_error(scores["true"], scores["predict"])
                    mse = mean_squared_error(scores["true"], scores["predict"])
                    rmse = np.sqrt(mse)
                    results[year] = {
                        "Mean Absolute Error": mae,
                        "Mean Squared Error": mse,
                        "Root Mean Squared Error": rmse,
                    }
                else:
                    results[year] = {
                        "Mean Absolute Error": None,
                        "Mean Squared Error": None,
                        "Root Mean Squared Error": None,
                    }

            return Response(results, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"status": "Test failed", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request, *args, **kwargs):
        try:
            # Lấy learn log từ model LearnLog và sort theo semester
            learn_log = LearnLog.objects.filter(student__student_code=request.data["student_id"])
            learn_log = sorted(learn_log, key=lambda x: x.semester)
      
            # Get all student
            student_data = get_all_student()
            student_data = sorted([student.student_code for student in student_data])

            # Get all course
            course_data = get_all_course()
            course_data = sorted([course.course_code for course in course_data])
  
            data = np.array([[int(student), course] for student in student_data for course in course_data])
            student_ids = {v: i for i, v in enumerate(np.unique(data[:, 0]))}
            course_ids = {v: i for i, v in enumerate(np.unique(data[:, 1]))}

            # Load model
            with open("model.pkl", "rb") as f:
                loaded_model = pickle.load(f)

            year_data = {}
             
            for log in learn_log:
                predict_score = loaded_model.pred(
                    student_ids[log.student.student_code],
                    course_ids[log.course.course_code], 
                    0, log.student.student_code, log.course.course_code
                )
                
                # Xác định năm học từ mã học kỳ (VD: "201" -> "2020-2021")
                year = f"20{log.semester[:2]}-20{int(log.semester[:2]) + 1}"
                
                if year not in year_data:
                    year_data[year] = {"true": [], "predict": []}

                year_data[year]["true"].append(float(log.score))
                year_data[year]["predict"].append(float(predict_score))

            # Tính toán lỗi động
            results = {}
            for year, scores in year_data.items():
                if scores["true"] and scores["predict"]:
                    mae = mean_absolute_error(scores["true"], scores["predict"])
                    mse = mean_squared_error(scores["true"], scores["predict"])
                    rmse = np.sqrt(mse)
                    results[year] = {
                        "Mean Absolute Error": mae,
                        "Mean Squared Error": mse,
                        "Root Mean Squared Error": rmse,
                    }
                else:
                    results[year] = {
                        "Mean Absolute Error": None,
                        "Mean Squared Error": None,
                        "Root Mean Squared Error": None,
                    }

            return Response(results, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"status": "Test failed", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        