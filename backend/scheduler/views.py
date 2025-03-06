from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ScheduledTask
from .serializers import ScheduledTaskSerializer
from .service import RemoveTask, learning_path_update_process, scheduleLearningPathUpdate
from datetime import datetime, timezone, timedelta

# Create your views here.
class ScheduledTaskViewSet(viewsets.ModelViewSet):
  queryset = ScheduledTask.objects.all()
  serializer_class = ScheduledTaskSerializer

  # def create(self, request, *args, **kwargs):
  #   serializer = self.get_serializer(data = request.data)
  #   if serializer.is_valid():
  #     task = serializer.save()
  #     jobId = CreateScheduleTask(task.id, task.run_time, task.url, task.method, task.body)

  #     return Response({"message": "Task Scheduled", "job_id": jobId}, status=status.HTTP_201_CREATED)
  
  #   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

  # def update(self, request, *args, **kwargs):
  #   task = self.get_object()
  #   serializer = self.get_serializer(task, data=request.data)
  #   if serializer.is_valid():
  #     task = serializer.save()
  #     RemoveTask(task.id)
  #     jobId = CreateScheduleTask(task.id, task.run_time, task.url, task.method, task.body)

  #     return Response({"message": "Task Rescheduled", "job_id": jobId}, status=status.HTTP_200_OK)
    
  #   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def destroy(self, request, *args, **kwargs):
    task = self.get_object()
    RemoveTask(task.id)
    task.delete()
    return Response({"message": "Task deleted"}, status=status.HTTP_204_NO_CONTENT)
  
  @action(detail=False, methods=["get"])
  def schedule(self, request):
    learning_path_update_process()
    return Response({"message": "Learning Paths Update Successfully!"})
  
  @action(detail=False, methods=["post"], url_path="set-time-update-learning-path")
  def setTimeUpdateLearningPath(self, request):
    year = request.data.get("year")
    month = request.data.get("month")
    day = request.data.get("day")
    hour = request.data.get("hour")
    minute = request.data.get("minute")
    t_7 = datetime(year, month, day, hour, minute, 0, tzinfo=timezone(timedelta(hours=7)))
    t_utc = t_7.astimezone(timezone.utc)

    print(f"t7 = {t_7.isoformat()}, t_utc = {t_utc.isoformat()}")

    task = ScheduledTask(run_time = t_7.isoformat())
    task.save()

    scheduleLearningPathUpdate(t_utc.isoformat(), task.id)

    return Response({"message": "Learning Paths Update Successfully!"})
  
