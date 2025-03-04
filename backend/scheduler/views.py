from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import ScheduledTask
from .serializers import ScheduledTaskSerializer
from .service import CreateScheduleTask, RemoveTask

# Create your views here.
class ScheduledTaskViewSet(viewsets.ModelViewSet):
  queryset = ScheduledTask.objects.all()
  serializer_class = ScheduledTaskSerializer

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data = request.data)
    if serializer.is_valid():
      task = serializer.save()
      jobId = CreateScheduleTask(task.id, task.run_time, task.url, task.method, task.body)

      return Response({"message": "Task Scheduled", "job_id": jobId}, status=status.HTTP_201_CREATED)
  
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

  def update(self, request, *args, **kwargs):
    task = self.get_object()
    serializer = self.get_serializer(task, data=request.data)
    if serializer.is_valid():
      task = serializer.save()
      RemoveTask(task.id)
      jobId = CreateScheduleTask(task.id, task.run_time, task.url, task.method, task.body)

      return Response({"message": "Task Rescheduled", "job_id": jobId}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def destroy(self, request, *args, **kwargs):
    task = self.get_object()
    RemoveTask(task.id)
    task.delete()
    return Response({"message": "Task deleted"}, status=status.HTTP_204_NO_CONTENT)