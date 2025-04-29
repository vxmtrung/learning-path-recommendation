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
    # def get(self, request, *args, **kwargs):
    #     try:
    #         # Lấy learn log từ model LearnLog
    #         learn_log = LearnLog.objects.all()
    #         learn_log = sorted(learn_log, key=lambda x: x.semester)
            
      
    #         # Get all student
    #         student_data = get_all_student()
    #         student_data = sorted([student.student_code for student in student_data])

    #         # Get all course
    #         course_data = get_all_course()
    #         course_data = sorted([course.course_code for course in course_data])
  
    #         data = []
    #         for student in student_data:
    #             for course in course_data:
    #                 data.append([int(student), course])
                    
    #         data = np.array(data)
    #         student_ids = {v: i for i, v in enumerate(np.unique(data[:, 0]))}
    #         course_ids = {v: i for i, v in enumerate(np.unique(data[:, 1]))}
   
    #         with open("model.pkl", "rb") as f:
    #             loaded_model = pickle.load(f)
   
    #         year_data = {}
    #         for log in learn_log:
    #             predict_score = loaded_model.pred(
    #                 student_ids[log.student.student_code],
    #                 course_ids[log.course.course_code], 
    #                 0, log.student.student_code, log.course.course_code
    #             )
                
    #             # Xác định năm học từ mã học kỳ (VD: "201" -> "2020-2021")
    #             year = f"20{log.semester[:2]}-20{int(log.semester[:2]) + 1}"
                
    #             if year not in year_data:
    #                 year_data[year] = {"true": [], "predict": []}

    #             year_data[year]["true"].append(float(log.score))
    #             year_data[year]["predict"].append(float(predict_score))
            
    #         years = []
    #         mae_data = []
    #         rmse_data = []
    #         # Tính toán lỗi động
    #         results = {
    #             "number_of_students": len(student_data),
    #             "number_of_courses": len(course_data),
    #         }
    #         for year, scores in year_data.items():
    #             years.append(year)
    #             if scores["true"] and scores["predict"]:
    #                 mae = mean_absolute_error(scores["true"], scores["predict"])
    #                 mse = mean_squared_error(scores["true"], scores["predict"])
    #                 rmse = np.sqrt(mse)
    #                 mae_data.append(mae)
    #                 rmse_data.append(rmse)
    #                 results[year] = {
    #                     "Mean Absolute Error": mae,
    #                     "Mean Squared Error": mse,
    #                     "Root Mean Squared Error": rmse,
    #                 }
    #             else:
    #                 results[year] = {
    #                     "Mean Absolute Error": None,
    #                     "Mean Squared Error": None,
    #                     "Root Mean Squared Error": None,
    #                 }
            
    #         plt.figure(figsize=(10,6))

    #         plt.plot(years, mae_data, marker='o', label='Mean Absolute Error (MAE)')
    #         # plt.plot(years, mse, marker='s', label='Mean Squared Error (MSE)')
    #         plt.plot(years, rmse_data, marker='^', label='Root Mean Squared Error (RMSE)')

    #         plt.title('Các chỉ số lỗi qua các năm')
    #         plt.xlabel('Năm học')
    #         plt.ylabel('Giá trị lỗi')
    #         plt.legend()
    #         plt.grid(True)
    #         plt.show()
    #         return Response(results, status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         return Response({"status": "Test failed", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, *args, **kwargs):
        try:
            # Lấy learn log từ model LearnLog
            learn_log = LearnLog.objects.all()
            learn_log = sorted(learn_log, key=lambda x: x.semester)
            
            # Lấy tất cả sinh viên
            student_data = get_all_student()
            student_data = sorted([student.student_code for student in student_data])

            # Lấy tất cả môn học
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
            bmf_data = []
            for log in learn_log:
                bmf_data.append((log.student.student_code, log.course.course_code, log.score)) 
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

            
            model = BiasMatrixFactorization(n_factors=5, learning_rate=0.01, n_iter=1000, reg_lambda=0.1)
            model.fit(bmf_data)

            bmf_year_data = {}
            for log in learn_log:
                predict_score = model.predict(log.student.student_code, log.course.course_code)
                year = f"20{log.semester[:2]}-20{int(log.semester[:2]) + 1}"

                if year not in bmf_year_data:
                    bmf_year_data[year] = {"true": [], "predict": []}

                bmf_year_data[year]["true"].append(float(log.score))
                bmf_year_data[year]["predict"].append(float(predict_score))

            # Tính toán lỗi cho cả hai mô hình
            years = []
            mae_data = []
            rmse_data = []
            bmf_mae_data = []
            bmf_rmse_data = []

            results = {
                "number_of_students": len(student_data),
                "number_of_courses": len(course_data),
            }

            for year in year_data.keys():
                years.append(year)

                # if year in year_data and year in bmf_year_data:
                if year in year_data:
                    mae = mean_absolute_error(year_data[year]["true"], year_data[year]["predict"])
                    mse = mean_squared_error(year_data[year]["true"], year_data[year]["predict"])
                    rmse = np.sqrt(mse)

                    bmf_mae = mean_absolute_error(bmf_year_data[year]["true"], bmf_year_data[year]["predict"])
                    bmf_mse = mean_squared_error(bmf_year_data[year]["true"], bmf_year_data[year]["predict"])
                    bmf_rmse = np.sqrt(bmf_mse)

                    mae_data.append(mae)
                    rmse_data.append(rmse)
                    bmf_mae_data.append(bmf_mae)
                    bmf_rmse_data.append(bmf_rmse)

                    results[year] = {
                        "Mean Absolute Error": mae,
                        "Mean Squared Error": mse,
                        "Root Mean Squared Error": rmse,
                        "BMF Mean Absolute Error": bmf_mae,
                        "BMF Mean Squared Error": bmf_mse,
                        "BMF Root Mean Squared Error": bmf_rmse
                    }
                else:
                    results[year] = {
                        "Mean Absolute Error": None,
                        "Mean Squared Error": None,
                        "Root Mean Squared Error": None,
                        "BMF Mean Absolute Error": None,
                        "BMF Mean Squared Error": None,
                        "BMF Root Mean Squared Error": None
                    }

            # Vẽ đồ thị so sánh MAE và RMSE của cả hai mô hình
            plt.figure(figsize=(10, 6))

            plt.plot(years, mae_data, marker='o', linestyle='-', label='MAE (BMF Model)')
            plt.plot(years, bmf_mae_data, marker='s', linestyle='-', label='MAE (uuCF Model)')
            plt.plot(years, rmse_data, marker='^', linestyle='--', label='RMSE (BMF Model)')
            plt.plot(years, bmf_rmse_data, marker='D', linestyle='--', label='RMSE (uuCF Model)')

            plt.title('So sánh các chỉ số lỗi giữa mô hình hiện tại và BMF')
            plt.xlabel('Năm học')
            plt.ylabel('Giá trị lỗi')
            plt.legend()
            plt.grid(True)
            plt.show()

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
            results = {
                "number_of_courses": len(learn_log),
            }
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
        
        
class DiagramAPIView(APIView):
  def get(self, request):
    learnlogs = LearnLog.objects.all()
    student_course = {}
    for learnlog in learnlogs:
        student = learnlog.student
        if student not in student_course:
            student_course[student] = 0
        student_course[student] += 1
    
    num_subjects_per_student = list(student_course.values())
    # Tạo histogram
    plt.figure(figsize=(10, 6))
    bins = range(max(num_subjects_per_student) + 2) # Tạo bins phù hợp với số môn học
    plt.hist(num_subjects_per_student, bins=bins, edgecolor='black', align='left', rwidth=0.8)

    # Đặt các ticks trên trục x cho mỗi số môn học
    plt.xticks(range(max(num_subjects_per_student) + 1))

    # Đặt tiêu đề và nhãn
    plt.title('Biểu đồ số môn học mà sinh viên đã học')
    plt.xlabel('Số môn học đã học')
    plt.ylabel('Số sinh viên')

    # Hiển thị lưới (tùy chọn)
    plt.grid(axis='y', alpha=0.5)

    # Hiển thị biểu đồ
    plt.tight_layout()
    plt.show()
    
    return Response("Diagram generated", status=status.HTTP_200_OK)


class BiasMatrixFactorization:
    def __init__(self, n_factors=10, learning_rate=0.01, n_iter=1000, reg_lambda=0.1):
        self.n_factors = n_factors  # số lượng yếu tố
        self.learning_rate = learning_rate  # tỷ lệ học
        self.n_iter = n_iter  # số vòng lặp
        self.reg_lambda = reg_lambda  # tham số điều chuẩn

    def fit(self, data):
        # data là một danh sách các tuple (sinh viên, môn học, điểm số)
        # Mọi sinh viên và môn học sẽ được gán một chỉ mục (index)
        
        # Tạo chỉ mục cho sinh viên và môn học
        self.student_map = {s: idx for idx, s in enumerate(set([x[0] for x in data]))}
        self.course_map = {c: idx for idx, c in enumerate(set([x[1] for x in data]))}
        
        self.n_students = len(self.student_map)
        self.n_courses = len(self.course_map)
        
        # Ma trận điểm số thực tế
        self.R = np.zeros((self.n_students, self.n_courses))
        for student, course, score in data:
            self.R[self.student_map[student], self.course_map[course]] = score
        
        # Khởi tạo ma trận P (sinh viên) và Q (môn học) ngẫu nhiên
        self.P = np.random.rand(self.n_students, self.n_factors)
        self.Q = np.random.rand(self.n_courses, self.n_factors)

        # Ma trận bias của sinh viên và môn học
        self.b_student = np.zeros(self.n_students)
        self.b_course = np.zeros(self.n_courses)
        self.global_bias = np.mean(self.R[np.where(self.R != 0)])  # Giá trị trung bình toàn bộ

        # Học với gradient descent
        for i in range(self.n_iter):
            self.gradient_descent()
            # if (i + 1) % 100 == 0:
            #     print(f"Iteration {i + 1}: Error = {self.get_error()}")

    def gradient_descent(self):
        # Gradient descent trên ma trận P, Q và bias
        for i in range(self.n_students):
            for j in range(self.n_courses):
                if self.R[i, j] > 0:  # chỉ cập nhật khi có điểm số
                    # Tính toán lỗi (error)
                    error_ij = self.R[i, j] - self.predict_single(i, j)
                    
                    # Cập nhật bias
                    self.b_student[i] += self.learning_rate * (error_ij - self.reg_lambda * self.b_student[i])
                    self.b_course[j] += self.learning_rate * (error_ij - self.reg_lambda * self.b_course[j])
                    
                    # Cập nhật các yếu tố (factors) của sinh viên và môn học
                    for k in range(self.n_factors):
                        p_ik = self.P[i, k]
                        q_jk = self.Q[j, k]
                        
                        self.P[i, k] += self.learning_rate * (error_ij * q_jk - self.reg_lambda * p_ik)
                        self.Q[j, k] += self.learning_rate * (error_ij * p_ik - self.reg_lambda * q_jk)

    def predict_single(self, i, j):
        """Dự đoán điểm số cho một sinh viên và môn học cụ thể"""
        return self.global_bias + self.b_student[i] + self.b_course[j] + np.dot(self.P[i, :], self.Q[j, :].T)

    def get_error(self):
        """Tính toán lỗi (MSE - Mean Squared Error)"""
        error = 0
        count = 0
        for i in range(self.n_students):
            for j in range(self.n_courses):
                if self.R[i, j] > 0:  # chỉ tính với các giá trị thực tế
                    error += (self.R[i, j] - self.predict_single(i, j))**2
                    count += 1
        return np.sqrt(error / count)

    def predict(self, student, course):
        """Dự đoán điểm số cho một sinh viên và môn học"""
        return self.predict_single(self.student_map[student], self.course_map[course])