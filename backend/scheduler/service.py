from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
import requests
import json

scheduler = BackgroundScheduler()
scheduler.start()

def CallApi(taskId, url, method, body):
  try:
    if method == "POST":
      response = requests.posts(url, json=body)
    else:
      response = requests.get(url)

      print(f"Task {taskId} - API Response: {response.status_code}, {response.text}")
  except Exception as e:
    print(f"Task {taskId} - Failed: {e}")

def CreateScheduleTask(taskId, runTime, url, method, body):
  try:
    job = scheduler.add_job(
      CallApi,
      trigger=DateTrigger(run_date=runTime),
      args=[taskId, url, method, body],
      id=str(taskId),
      replace_existing=True
    )
    print(f"Create Schedule Task - Success: Id - {job.id}")

    return job.id
  except Exception as e:
    print(f"Create Schedule Task - Failed: {e}")
  
def RemoveTask(taskId):
  try:
    scheduler.remove(taskId)
    print(f"Removed Schedule Task {taskId} - Success")
  except Exception as e:
    print(f"Remove Schedule Task - Failed: {e}")