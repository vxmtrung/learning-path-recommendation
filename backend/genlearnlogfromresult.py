from pathlib import Path
import json
import pandas as pd
import random

sem1 = ['LA1003', 'MT1003', 'PH1003', 'CO1005', 'CO1023']
sem2 = ['LA1005', 'MT1005', 'MT1007', 'CO1027', 'PH1007']
sem3 = ['LA1007', 'SP1031', 'CO2007', 'CO2011', 'CO2003']
sem4 = ['LA1009', 'SP1033', 'CO2017', 'CO2039', 'MT2013', 'TCTD1']
sem5 = ['SP1035', 'CO3093', 'CO2013', 'CO3001', 'CH1003', 'DATH']
sem6 = ['SP1039', 'CO2001', 'CO3005', 'CO3335', 'DADN', 'TCTD2']
sem7 = ['SP1037', 'CO4029', 'TCTD3']
sem8 = ['SP1007', 'CO4337']

op = ['CO3065', 'CO3011', 'CO3013', 'CO3015', 'CO3017', 'CO3115', 'CO3089']


def getRecommendLogs(studentCode):
  folderPath = Path("logs/" + studentCode)
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
        if df_true.empty:
          all_pred_courses = set()
        else:
          df_true = df_true.drop(columns=['semester'])
          all_pred_courses = set(df_true.explode('pred_course')['pred_course'])
          df_true = pd.DataFrame({'pred_course': [all_pred_courses]})     

        df_dict[file.stem] = df_true

  return df_dict

def gen():
  res = []

  logs_path = Path("logs")
  ids = [f.name for f in logs_path.iterdir() if f.is_dir()]
  print(ids)
  for id in ids:
    if id[:3] == '211':
      courses = sem8 + random.sample(op, 2)
    elif id[:3] == '221':
      courses = sem6 + sem7 + sem8 + random.sample(op, 5)
    elif id[:3] == '231':
      courses = sem4 + sem5 + sem6 + sem7 + sem8 + random.sample(op, 5)
    elif id[:3] == '241':
      courses = sem2 + sem3 + sem4 + sem5 + sem6 + sem7 + sem8 + random.sample(op, 5)
    for course in courses: 
      with open("learn_log.txt", "a", encoding="utf-8") as file:
        file.write(f"{id},{course},{7},{1},{242}\n") 
  return 1


gen()