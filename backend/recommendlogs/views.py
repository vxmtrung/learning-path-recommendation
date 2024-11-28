from django.shortcuts import render
from rest_framework.views import APIView

from .models import RecommendLog
from django.http import JsonResponse
import json
# Create your views here.
class RecommendLogsView(APIView):
     def post(self, request):
        input_data = request.data
        student_id = input_data['student_id']
        
        # Lấy các bản ghi từ RecommendLog cho student_id cụ thể
        logs = RecommendLog.objects.filter(student_id=student_id)
        
        # Chuyển đổi các bản ghi thành dạng dictionary
        log_data = []
        for log in logs:
            learning_path = json.loads(log.learning_path) if log.learning_path else None
            log_data.append({
                "id": log.id,
                "student_id": log.student_id,
                "learning_path": learning_path,
                "created_at": log.created_at
            })
        
        # Trả về dữ liệu dưới dạng JSON
        return JsonResponse({'recommendations': log_data}, json_dumps_params={'indent': 4, 'ensure_ascii': False})