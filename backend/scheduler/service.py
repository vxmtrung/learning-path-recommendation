from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
import json

from students.views import get_all_student
from courses.views import get_all_course
from learnlog.views import get_learn_log
from courses.views import get_courses_by_major
from predict.views import predict_score

from recommendlogs.models import RecommendLog
from recommendlogs.serializers import RecommendLogSerializer
from learning_outcomes.models import Learning_Outcome
from student_needs.models import StudentNeed

from predict.model_predict import CF

from recommend.course_tree import create_course_tree
from recommend.recommend import recommend
from semesters.models import Semester
from semesters.serializers import SemesterSerializer
import pandas as pd
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer, util
import os
import pytz
from datetime import datetime

from decimal import Decimal, ROUND_HALF_UP
scheduler = BackgroundScheduler()
scheduler.start()

# def CallApi(taskId, url, method, body):
#   try:
#     if method == "POST":
#       response = requests.posts(url, json=body)
#     else:
#       response = requests.get(url)

#       print(f"Task {taskId} - API Response: {response.status_code}, {response.text}")
#   except Exception as e:
#     print(f"Task {taskId} - Failed: {e}")

# def CreateScheduleTask(taskId, runTime, url, method, body):
#   try:
#     job = scheduler.add_job(
#       CallApi,
#       trigger=DateTrigger(run_date=runTime),
#       args=[taskId, url, method, body],
#       id=str(taskId),
#       replace_existing=True
#     )
#     print(f"Create Schedule Task - Success: Id - {job.id}")

#     return job.id
#   except Exception as e:
#     print(f"Create Schedule Task - Failed: {e}")
  
def RemoveTask(taskId):
  try:
    scheduler.remove(taskId)
    print(f"Removed Schedule Task {taskId} - Success")
  except Exception as e:
    print(f"Remove Schedule Task - Failed: {e}")

def scheduleLearningPathUpdate(t, taskId):
  try:
    job = scheduler.add_job(
      learning_path_update_process,
       trigger=DateTrigger(run_date=t),
       args=[],
       id=str(taskId),
       replace_existing=True
    )

    print(f"Create Schedule Task - Success: Id - {job.id}")

    return job.id
  except Exception as e:
    print(f"Create Schedule Task - Failed: {e}")

def learning_path_update_process():
  # Step 1: Train model
  # Step 2: Train model with learning outcome
  # Step 3: Get active student needs
  # Step 4: Loop through the student needs and get new learning path
  # Step 5: Next semester
  try:
    train_model()
    train_model_with_learning_outcome()
    student_needs = get_active_student_need()
    for student_need in student_needs:
      generate_new_learning_path(student_need)
    switch_next_semester()
    print("Learning path update run")
    return {"status": "Learning path update process successful"}
  except Exception as e:
    return {"status": "Learning path update process failed", "error": e}

def train_model():
  try:
      # Get all student
      student_data = get_all_student()
      student_data = [student.student_code for student in student_data]
  
      # Get all course
      course_data = get_all_course()
      course_data = [course.course_code for course in course_data]
      
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
          
      rs = CF(data, k = 100, uuCF = 1, students=student_data, courses=course_data)
      rs.fit()
      with open('model.pkl', 'wb') as f:
          pickle.dump(rs, f)
      return {"status": "Train model successful"}
  except Exception as e:
      return {"status": "Train model failed", "error": e}
    
def train_model_with_learning_outcome():
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
          
      return {"status": "Train model with learning outcome successful"}
  except Exception as e:
      return {"status": "Train model with learning outcome failed", "error": e}

def get_active_student_need():
  try:
    return StudentNeed.objects.filter(active=True)
  except Exception as e:
    return {"status": "Get active student need failed", "error": e}
  
def generate_new_learning_path(student_need):
  try:
    # Get course list by major
    course_list = get_courses_by_major(student_need.major)
        
    # Get predict score
    scores = predict_score(student_need.student_id, course_list)
        
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
    learner_log = [log for log in learn_log if log.student_id == student_need.student_id]
        
    # Create Course Graph
    course_tree = create_course_tree(course_list)
        
    # Recommend Learing Path 
    learner = {
      "english_level": student_need.english_level,
      "learn_summer_semester": student_need.learn_summer_semester,
      "summer_semester": student_need.summer_semester,
      "group_free_elective": student_need.group_free_elective,
      "over_learn": student_need.over_learn,
      "main_semester": student_need.main_semester,
      "learn_to_improve": student_need.learn_to_improve,
    }
           
    try:
      learning_path_recommend = recommend(learner, learner_log, course_list, course_tree, int(student_need.next_semester))
    except Exception as e:
      return {"status": "Generate new learning path failed", "error": e}
        
        
    # Convert learning path to dictionary format
    learning_path_data = {"learning_path": [element.to_dict() for element in learning_path_recommend]}
        
    ### Add log
    try:
      # get path to logs folder
      current_dir = os.path.dirname(os.path.abspath(__file__))
      parent_dir = os.path.dirname(current_dir)
      logs_dir = os.path.join(parent_dir, 'logs')
      student_folder = os.path.join(logs_dir, student_need.student_id)
            
      # create logs folder if not exist
      os.makedirs(logs_dir, exist_ok=True)
      os.makedirs(student_folder, exist_ok=True)
            
      vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")
      current_datetime = datetime.now(vietnam_tz).strftime("%Y%m%d_%H%M%S")
        
      file_path = os.path.join(student_folder, f"{student_need.student_id}_{current_datetime }.txt")
      with open(file_path, 'w', encoding='utf-8') as f:  # Đảm bảo hỗ trợ Unicode
        json.dump(learning_path_data, f, indent=4, ensure_ascii=False)
            
      recommend_logs = []
      recommend_log = {
        "student": student_need.student_id,
        "log_file_name": f"{student_need.student_id}_{current_datetime }.txt",
        "is_active": True,
      }
      serializer = RecommendLogSerializer(data=recommend_log)
      if serializer.is_valid():
        recommend_logs.append(RecommendLog(**serializer.validated_data))
      else:
        return {"status": "Generate new learning path failed", "error": "Save log error"}
      RecommendLog.objects.bulk_create(recommend_logs)
    except Exception as e:
      return {"status": "Generate new learning path failed", "error": e}
  except Exception as e:
    return {"status": "Generate new learning path failed", "error": e}
  
def switch_next_semester():
  try:
    current_semester = Semester.objects.get(is_active=True)
  
    if current_semester.semester_name.endswith("1"):    
      next_semester_name = int(current_semester.semester_name) + 1
    elif current_semester.semester_name.endswith("2"):
      next_semester_name = int(current_semester.semester_name) + 1
    else:
      next_semester_name = int(current_semester.semester_name) + 8
      
    semester = {
      "semester_name": str(next_semester_name),
    }
    serializer = SemesterSerializer(data=semester)
    if not serializer.is_valid():
      return {"status": "Switch next semester failed", "error": serializer.errors}
    current_semester.is_active = False
    current_semester.save()
    serializer.save()
    return {"status": "Switch next semester successful"}
  except Exception as e:
    return {"error": "Can not create semester", "details": str(e)}
  
  