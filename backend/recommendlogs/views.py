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
        logs = RecommendLog.objects.filter(student_id=student_id, is_active=True)
        
        # Chuyển đổi các bản ghi thành dạng dictionary
        log_data = None
        for log in logs:
            log_name = log.log_file_name
            # Get log file by 7 first characters of log file name
            with open(f"logs/{log_name[:7]}/{log.log_file_name}", "r", encoding="utf-8") as log_file:
                log_data = json.load(log_file)
            log_file.close()
        
        # Trả về dữ liệu dưới dạng JSON
        return JsonResponse({'data': log_data}, json_dumps_params={'indent': 4, 'ensure_ascii': False})