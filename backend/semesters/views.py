from django.shortcuts import render

from rest_framework.views import APIView
from django.http import JsonResponse

from .models import Semester
from .serializers import SemesterSerializer
# Create your views here.
class SemesterView(APIView):
    def get(self, request):
        try:
            semester = Semester.objects.get(is_active=True)
            semester_data = {
                "semester_name": semester.semester_name,
            }
            return JsonResponse(semester_data, json_dumps_params={'indent': 4, 'ensure_ascii': False})
        except Exception as e:
            return JsonResponse({"error": "Can not get semester", "details": str(e)}, status=400)
      
    def post(self, request):
        try:
            input_data = request.data
            
            Semester.objects.filter(is_active=True).update(is_active=False)
            
            semester = {
                "semester_name": input_data['semester_name'],
            }
            serializer = SemesterSerializer(data=semester)
            if not serializer.is_valid():
                return JsonResponse({"error": serializer.errors}, status=400)
            serializer.save()
            return JsonResponse({"message": "Create semester successfully"}, safe=False, status=201)
        
        except Exception as e:
            return JsonResponse({"error": "Can not create semester", "details": str(e)}, status=400)