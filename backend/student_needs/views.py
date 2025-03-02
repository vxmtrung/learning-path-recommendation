from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import StudentNeed
from .serializers import StudentNeedSerializer
# Create your views here.
class GetStudentNeedView(APIView):
    # Define the get method
    def post(self, request, *args, **kwargs):
        # Get student from request
        student = request.data.get('student_id')
        
        # Get Last Student Needs by student
        student_needs = StudentNeed.objects.filter(student_id=student).order_by('-created_at').first()
        
        # Return the student needs
        return Response({
            "student_id": student_needs.student_id,
            "english_level": student_needs.english_level,   
            "major": student_needs.major,
            "learn_summer_semester": student_needs.learn_summer_semester,
            "summer_semester": student_needs.summer_semester,
            "group_free_elective": student_needs.group_free_elective,
            "over_learn": student_needs.over_learn,
            "main_semester": student_needs.main_semester,
            "next_semester": student_needs.next_semester,
            "learn_to_improve": student_needs.learn_to_improve
        })
        
class CreateStudentNeedView(APIView):
    # Define the post method
    def post(self, request, *args, **kwargs):
        try:
            # Get student needs from request
            student_needs = {
                "student_id": request.data.get('student_id'),
                "english_level": request.data.get('english_level'),
                "major": request.data.get('major'),
                "learn_summer_semester": request.data.get('learn_summer_semester'),
                "summer_semester": request.data.get('summer_semester'),
                "group_free_elective": request.data.get('group_free_elective'),
                "over_learn": request.data.get('over_learn'),
                "main_semester": request.data.get('main_semester'),
                "next_semester": request.data.get('next_semester'),
                "learn_to_improve": request.data.get('learn_to_improve')
            }
            
            # Create student needs
            serializer = StudentNeedSerializer(data=student_needs)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "Student needs created successful"}, status=201)
            else:
                return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)