from learnlog.models import LearnLog

import numpy as np
import pickle

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def test_model_predict():
    # Lấy learn log từ model LearnLog
    learn_log = LearnLog.objects.defer("learn_log_id", "count_learn", "semester").all()
    
    # Get all student từ file student_data.txt
    with open("student_data.txt", "r", encoding="utf-8") as file:
        student_data = file.readlines()
        student_data = [student.strip() for student in student_data]
        
    # Get all course từ file course_data.txt
    with open("course_data.txt", "r", encoding="utf-8") as file:
        course_data = file.readlines()
        course_data = [course.strip() for course in course_data]
            
    true_data = []
    predict_data = []
    
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
        true_data.append(float(log.score))
        predict_data.append(float(loaded_model.pred(student_ids[log.student.student_code], course_ids[log.course.course_code], 0, log.student.student_code, log.course.course_code)))
    
    mae = mean_absolute_error(true_data, predict_data)
    mse = mean_squared_error(true_data, predict_data)
    rmse = np.sqrt(mse)
    r2 = r2_score(true_data, predict_data)
   
    print("Mean Absolute Error: ", mae)
    print("Mean Squared Error: ", mse)
    print("Root Mean Squared Error: ", rmse)
    print("R2 Score: ", r2)

test_model_predict()