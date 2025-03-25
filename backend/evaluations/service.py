from learnlog.models import LearnLog
from pathlib import Path
from learnlog.serializers import LearnLogSerializer
import pandas as pd
from django.db.models.functions import Cast
from django.db.models import IntegerField
import os
import json
from datetime import datetime

class PathEvalForEachLog:
  def __init__(self, fileName, precision, recall, f1):
      self.fileName = fileName
      self.precision = precision
      self.recall = recall
      self.f1 = f1
  
  def __str__(self):
     return f"fileName: {self.fileName}, precision: {self.precision}, recall: {self.recall}, f1-score: {self.f1}"
  
  def to_dict(self):
     return {
        "file_name": self.fileName,
        "precision": self.precision,
        "recall": self.recall,
        "f1_score": self.f1
     }

class PathEvalForEachStudent:
  def __init__(self, student_code, pathEval):
      self.student_code = student_code
      self.pathEval = pathEval

  def to_dict(self):
      return {
          "student_code": self.student_code,
          "pathEval": [e.to_dict() for e in self.pathEval]
      }

def getYTrueDataFrame(logs):
    serializer = LearnLogSerializer(logs, many = True)
    df = pd.DataFrame(serializer.data)
    if df.empty:
       df_true = pd.DataFrame(columns=['semester', 'actual_course'])
    else:
      df_true = df.groupby('semester')['course'].apply(set).reset_index()
      df_true.columns = ['semester', 'actual_course']

    return df_true

def getLearnLogByStudentCodeAndSemester(studentCode, semester):
   logs = LearnLog.objects.annotate(
     semester_int=Cast('semester', IntegerField())
     ).filter(student__student_code=studentCode, semester_int__gte=semester)
   
   return logs

def getRecommendLogs(studentCode):
  latest_logs = getLatestLogForEachSemester(studentCode)
  folderPath = Path("logs/" + studentCode)
  df_dict = {}

  for _, info in latest_logs.items():
    file_path = folderPath / info["file_name"]
    if file_path.exists():
      with file_path.open("r", encoding="utf-8") as f:
          data = json.load(f)

          records = []
          for ele in data["learning_path"]:
            semester = ele["semester"]
            course_codes = {course["course_code"] for course in ele["courses"]}
            records.append({"semester": semester, "pred_course": course_codes})
      
          df_true = pd.DataFrame(records)
          df_dict[file_path.stem] = df_true

  return df_dict

def evaluateRecommendationPathForEachStudent(student_code):
  df_pred_dict = getRecommendLogs(student_code)

  pathEval = []

  for name, df_pred_raw in df_pred_dict.items():
    logs = getLearnLogByStudentCodeAndSemester(student_code, df_pred_raw.iloc[0]["semester"])
    df_true = getYTrueDataFrame(logs)

    df_true["semester"] = df_true["semester"].astype(int)
    df_pred_raw["semester"] = df_pred_raw["semester"].astype(int)

    cur_sem = df_true["semester"].max()
    df_pred = df_pred_raw[df_pred_raw["semester"] <= cur_sem]
    if df_true.empty and df_pred.empty:
      # pathEval.append(PathEvalForEachLog(name, 0, 0, 0))
      continue
    
    print(f"\nLearning Recommend từ file: {name}.txt")

    df_merge = df_true.merge(df_pred, on='semester', how='outer')

    df_merge['actual_course'] = df_merge['actual_course'].apply(lambda x: x if isinstance(x, set) else set())
    df_merge['pred_course'] = df_merge['pred_course'].apply(lambda x: x if isinstance(x, set) else set())
    
    print(df_merge)

    df_merge['correct'] = df_merge.apply(lambda x: len(x['actual_course'] & x['pred_course']), axis=1)

    df_merge['Precision'] = df_merge.apply(lambda x: x['correct'] / len(x['pred_course']) if len(x['pred_course']) > 0 else 0, axis=1)
    df_merge['Recall'] = df_merge.apply(lambda x: x['correct'] / len(x['actual_course']) if len(x['actual_course']) > 0 else 0, axis=1)
    df_merge['F1-score'] = df_merge.apply(
    lambda x: (2 * x['Precision'] * x['Recall']) / (x['Precision'] + x['Recall']) 
    if (x['Precision'] + x['Recall']) > 0 else 0, 
    axis=1)
    # Hiển thị kết quả
    print(df_merge[['semester', 'Precision', 'Recall', 'F1-score']])
    pathEval.append(PathEvalForEachLog(name, df_merge['Precision'].mean(), df_merge['Recall'].mean(), df_merge['F1-score'].mean()))

  if len(pathEval) == 0:
    pathEval.append(PathEvalForEachLog("NULL", 0, 0, 0))
     
  return PathEvalForEachStudent(student_code, pathEval)

def getPathEvaluationForStudent(student_code):
  df_pred_dict = getRecommendLogs(student_code)

  pathEval = []

  for name, df_pred_raw in df_pred_dict.items():
    logs = getLearnLogByStudentCodeAndSemester(student_code, df_pred_raw.iloc[0]["semester"])
    df_true = getYTrueDataFrame(logs)

    df_true["semester"] = df_true["semester"].astype(int)
    df_pred_raw["semester"] = df_pred_raw["semester"].astype(int)

    cur_sem = df_true["semester"].max()
    df_pred = df_pred_raw[df_pred_raw["semester"] <= cur_sem]
    if df_true.empty and df_pred.empty:
      # pathEval.append(PathEvalForEachLog(name, 0, 0, 0))
      continue
    
    # print(f"\nLearning Recommend từ file: {name}.txt")

    df_merge = df_true.merge(df_pred, on='semester', how='outer')

    df_merge['actual_course'] = df_merge['actual_course'].apply(lambda x: x if isinstance(x, set) else set())
    df_merge['pred_course'] = df_merge['pred_course'].apply(lambda x: x if isinstance(x, set) else set())
    
    # print(df_merge)

    df_merge['correct'] = df_merge.apply(lambda x: len(x['actual_course'] & x['pred_course']), axis=1)

    df_merge['Precision'] = df_merge.apply(lambda x: x['correct'] / len(x['pred_course']) if len(x['pred_course']) > 0 else 0, axis=1)
    df_merge['Recall'] = df_merge.apply(lambda x: x['correct'] / len(x['actual_course']) if len(x['actual_course']) > 0 else 0, axis=1)
    df_merge['F1-score'] = df_merge.apply(
    lambda x: (2 * x['Precision'] * x['Recall']) / (x['Precision'] + x['Recall']) 
    if (x['Precision'] + x['Recall']) > 0 else 0, 
    axis=1)
    # Hiển thị kết quả
    # print(df_merge[['semester', 'Precision', 'Recall', 'F1-score']])
    pathEval.append(df_merge[['semester', 'Precision', 'Recall', 'F1-score']])

  if len(pathEval) == 0:
    return "No data to evaluate for this student"

  res = pd.concat(pathEval).groupby("semester").mean().reset_index()
  return res

def evalAll():
  res = []
  logs_path = Path("logs")
  ids = [f.name for f in logs_path.iterdir() if f.is_dir()]


  for id in ids:
    tmp = getPathEvaluationForStudent(id)
    if isinstance(tmp, str):
       continue
    res.append(getPathEvaluationForStudent(id))

  res1 = pd.concat(res).groupby("semester").mean().reset_index()

  return res1


def evaluateRecommendationPathForAllStudents():
  res = []

  logs_path = Path("logs")
  ids = [f.name for f in logs_path.iterdir() if f.is_dir()]

  for id in ids:
     res.append(evaluateCourseChoicesForEachStudent(id)) 

  return res

def evaluateRecommendationPathForSystem():
  evalOfStudents = evaluateRecommendationPathForAllStudents()

  precision_sum = 0
  recall_sum = 0
  f1_sum = 0
  count = 0

  for evalStudent in evalOfStudents:
     for eval in evalStudent.pathEval:
        precision_sum += eval.precision
        recall_sum += eval.recall
        f1_sum += eval.f1
        count += 1
  
  return {
     "precision_mean": precision_sum / count,
     "recall_mean": recall_sum / count,
     "f1_score_mean": f1_sum / count
  }

def evaluateCourseChoicesForEachStudent(student_code):
  df_pred_dict = getRecommendLogs(student_code)

  pathEval = []

  for name, df_pred in df_pred_dict.items():
    logs = getLearnLogByStudentCodeAndSemester(student_code, df_pred.iloc[0]["semester"])
    df_true = getYTrueDataFrame(logs)

    df_true["semester"] = df_true["semester"].astype(int)
    df_pred["semester"] = df_pred["semester"].astype(int)
    
    cur_sem = df_true["semester"].max()
    df_pred_filtered = df_pred[df_pred["semester"] <= cur_sem]

    if df_true.empty:
       all_true_courses = set()
    else:
       df_true = df_true.drop(columns=['semester'])
       all_true_courses = set(df_true.explode('actual_course')['actual_course'])
    df_true = pd.DataFrame({'actual_course': [all_true_courses]})

    if df_pred_filtered.empty:
       all_pred_courses = set()
    else:
       df_pred_filtered = df_pred_filtered.drop(columns=['semester'])
       all_pred_courses = set(df_pred_filtered.explode('pred_course')['pred_course'])
    df_pred_filtered = pd.DataFrame({'pred_course': [all_pred_courses]})

    df_merge = pd.concat([df_pred_filtered, df_true], axis=1)
    df_merge['correct'] = df_merge.apply(lambda x: len(x['actual_course'] & x['pred_course']), axis=1)

    df_merge['Precision'] = df_merge.apply(lambda x: x['correct'] / len(x['pred_course']) if len(x['pred_course']) > 0 else 0, axis=1)
    df_merge['Recall'] = df_merge.apply(lambda x: x['correct'] / len(x['actual_course']) if len(x['actual_course']) > 0 else 0, axis=1)
    df_merge['F1-score'] = df_merge.apply(
    lambda x: (2 * x['Precision'] * x['Recall']) / (x['Precision'] + x['Recall']) 
    if (x['Precision'] + x['Recall']) > 0 else 0, 
    axis=1)
    print(df_merge[['Precision', 'Recall', 'F1-score']])
    pathEval.append(PathEvalForEachLog(name, df_merge['Precision'].mean(), df_merge['Recall'].mean(), df_merge['F1-score'].mean()))

  return PathEvalForEachStudent(student_code, pathEval)


def getLatestLogForEachSemester(student_code):
  folderPath = Path("logs/" + student_code)
  print(folderPath.resolve())

  latest_files = {}

  for file in folderPath.glob("*.txt"):
      with file.open("r", encoding="utf-8") as f:
        data = json.load(f)

      semester = data.get("learning_path")[0]["semester"]
      _, date_str, hour_str = file.name[:-4].split("_")
      file_date = datetime.strptime(date_str + hour_str, "%Y%m%d%H%M%S")

      if semester not in latest_files or file_date > latest_files[semester]["date"]:
        latest_files[semester] = {"date": file_date, "file_name": file.name}

  # for f, info in latest_files.items():
  #   print(f"Học kỳ {f}, file_name: {info['file_name']}, file_date: {info['date']}")
  
  return latest_files