from learnlog.models import LearnLog
from pathlib import Path
from learnlog.serializers import LearnLogSerializer
import pandas as pd
from django.db.models.functions import Cast
from django.db.models import IntegerField
import os
import json

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
  folderPath = Path("logs/" + studentCode)
  print(folderPath.resolve())
  df_dict = {}

  for file in folderPath.glob("*.txt"):
      with file.open("r", encoding="utf-8") as f:
        data = json.load(f)

        records = []
        for ele in data["learning_path"]:
          semester = ele["semester"]
          course_codes = {course["course_code"] for course in ele["courses"]}
          records.append({"semester": semester, "pred_course": course_codes})
    
        df_true = pd.DataFrame(records)
        df_dict[file.stem] = df_true

  return df_dict

def evaluateRecommendationPathForEachStudent(student_code):
  df_pred_dict = getRecommendLogs(student_code)

  pathEval = []

  for name, df_pred in df_pred_dict.items():
    print(f"\nLearning Recommend từ file: {name}.txt")
    logs = getLearnLogByStudentCodeAndSemester(student_code, df_pred.iloc[0]["semester"])
    df_true = getYTrueDataFrame(logs)
    df_merge = df_true.merge(df_pred, on='semester', how='outer')

    df_merge['actual_course'] = df_merge['actual_course'].apply(lambda x: x if isinstance(x, set) else set())
    df_merge['pred_course'] = df_merge['pred_course'].apply(lambda x: x if isinstance(x, set) else set())
    
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

  return PathEvalForEachStudent(student_code, pathEval)

def evaluateRecommendationPathForAllStudents():
  res = []

  logs_path = Path("logs")
  ids = [f.name for f in logs_path.iterdir() if f.is_dir()]

  for id in ids:
     res.append(evaluateRecommendationPathForEachStudent(id)) 

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


