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
                        avg_similarity = similarities.numpy().max(axis=1).mean()
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
      
            # Get all student
            student_data = get_all_student()
            student_data = sorted([student.student_code for student in student_data])

            # Get all course
            course_data = get_all_course()
            course_data = sorted([course.course_code for course in course_data])
  
            true_data_2020_2021 = []
            predict_data_2020_2021 = []
            true_data_2021_2022 = []
            predict_data_2021_2022 = []
            true_data_2022_2023 = []
            predict_data_2022_2023 = []
            true_data_2023_2024 = []
            predict_data_2023_2024 = []
            true_data_2024_2025 = []
            predict_data_2024_2025 = []
            
            data = []
            for student in student_data:
                for course in course_data:
                    data.append([int(student), course])
                    
            data = np.array(data)
            student_ids = {v: i for i, v in enumerate(np.unique(data[:, 0]))}
            course_ids = {v: i for i, v in enumerate(np.unique(data[:, 1]))}
   
            with open("model.pkl", "rb") as f:
                loaded_model = pickle.load(f)
   
            for log in learn_log:
                predict_score = loaded_model.pred(student_ids[log.student.student_code], course_ids[log.course.course_code], 0, log.student.student_code, log.course.course_code)
                if log.semester in ["201", "202"]:
                    true_data_2020_2021.append(float(log.score))
                    predict_data_2020_2021.append(float(predict_score))
                elif log.semester in ["211", "212"]:
                    true_data_2021_2022.append(float(log.score))
                    predict_data_2021_2022.append(float(predict_score))
                elif log.semester in ["221", "222"]:
                    true_data_2022_2023.append(float(log.score))
                    predict_data_2022_2023.append(float(predict_score))
                elif log.semester in ["231", "232"]:
                    true_data_2023_2024.append(float(log.score))
                    predict_data_2023_2024.append(float(predict_score))
                elif log.semester in ["241", "242"]:
                    true_data_2024_2025.append(float(log.score))
                    predict_data_2024_2025.append(float(predict_score))
            
            # 2020 - 2021
            mae_2020_2021 = mean_absolute_error(true_data_2020_2021, predict_data_2020_2021)
            mse_2020_2021 = mean_squared_error(true_data_2020_2021, predict_data_2020_2021)
            rmse_2020_2021 = np.sqrt(mse_2020_2021)
            r2_2020_2021 = r2_score(true_data_2020_2021, predict_data_2020_2021)
            
            # 2021 - 2022
            mae_2021_2022 = mean_absolute_error(true_data_2021_2022, predict_data_2021_2022)
            mse_2021_2022 = mean_squared_error(true_data_2021_2022, predict_data_2021_2022)
            rmse_2021_2022 = np.sqrt(mse_2021_2022)
            r2_2021_2022 = r2_score(true_data_2021_2022, predict_data_2021_2022)
            
            # 2022 - 2023
            mae_2022_2023 = mean_absolute_error(true_data_2022_2023, predict_data_2022_2023)
            mse_2022_2023 = mean_squared_error(true_data_2022_2023, predict_data_2022_2023)
            rmse_2022_2023 = np.sqrt(mse_2022_2023)
            r2_2022_2023 = r2_score(true_data_2022_2023, predict_data_2022_2023)
            
            # 2023 - 2024
            mae_2023_2024 = mean_absolute_error(true_data_2023_2024, predict_data_2023_2024)
            mse_2023_2024 = mean_squared_error(true_data_2023_2024, predict_data_2023_2024)
            rmse_2023_2024 = np.sqrt(mse_2023_2024)
            r2_2023_2024 = r2_score(true_data_2023_2024, predict_data_2023_2024)
            
            # 2024 - 2025
            mae_2024_2025 = mean_absolute_error(true_data_2024_2025, predict_data_2024_2025)
            mse_2024_2025 = mean_squared_error(true_data_2024_2025, predict_data_2024_2025)
            rmse_2024_2025 = np.sqrt(mse_2024_2025)
            r2_2024_2025 = r2_score(true_data_2024_2025, predict_data_2024_2025)
            years = ["2020-2021", "2021-2022", "2022-2023", "2023-2024", "2024-2025"]

            mae_values = [mae_2020_2021, mae_2021_2022, mae_2022_2023, mae_2023_2024, mae_2024_2025]
            mse_values = [mse_2020_2021, mse_2021_2022, mse_2022_2023, mse_2023_2024, mse_2024_2025]
            rmse_values = [rmse_2020_2021, rmse_2021_2022, rmse_2022_2023, rmse_2023_2024, rmse_2024_2025]

            # Vẽ biểu đồ đường
            plt.figure(figsize=(10, 6))

            plt.plot(years, mae_values, marker='o', linestyle='-', color='b', label="MAE")
            plt.plot(years, mse_values, marker='s', linestyle='--', color='r', label="MSE")
            plt.plot(years, rmse_values, marker='^', linestyle='-.', color='g', label="RMSE")

            # Thiết lập tiêu đề và nhãn
            plt.title("So sánh các chỉ số lỗi theo từng năm học", fontsize=14)
            plt.xlabel("Năm học", fontsize=12)
            plt.ylabel("Giá trị lỗi", fontsize=12)
            plt.legend()
            plt.grid(True)

            # Hiển thị biểu đồ
            plt.show()
            return Response({
                "status": "Test successful",
                "2020-2021": {
                    "Mean Absolute Error": mae_2020_2021,
                    "Mean Squared Error": mse_2020_2021,
                    "Root Mean Squared Error": rmse_2020_2021,
                },
                "2021-2022": {
                    "Mean Absolute Error": mae_2021_2022,
                    "Mean Squared Error": mse_2021_2022,
                    "Root Mean Squared Error": rmse_2021_2022,
                },
                "2022-2023": {
                    "Mean Absolute Error": mae_2022_2023,
                    "Mean Squared Error": mse_2022_2023,
                    "Root Mean Squared Error": rmse_2022_2023,
                },
                "2023-2024": {
                    "Mean Absolute Error": mae_2023_2024,
                    "Mean Squared Error": mse_2023_2024,
                    "Root Mean Squared Error": rmse_2023_2024,
                },
                "2024-2025": {
                    "Mean Absolute Error": mae_2024_2025,
                    "Mean Squared Error": mse_2024_2025,
                    "Root Mean Squared Error": rmse_2024_2025,
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"status": "Test failed", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        