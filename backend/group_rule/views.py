from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import GroupRule
from .serializers import GroupRuleSerializer
from rules.serializers import RuleSerializer
from rules.models import Rule
from group_course.models import GroupCourse
# Create your views here.
class GetRuleByGroupCourseView(APIView):
    def get(self, request):
        try:
            group_course_code = request.query_params.get('group_course_code')
            if not group_course_code:
                return Response({"error": "group_course_code is required"}, status=status.HTTP_400_BAD_REQUEST)
           
            return_data = []
            rules = GroupRule.objects.filter(group=group_course_code)
            for rule in rules:
                data = {
                    "rule_code": rule.rule.rule_code,
                    "rule_name": rule.rule.rule_name,
                    "rule_description": rule.rule.rule_description,
                    "is_active": True,
                    "parameter": rule.parameter,
                }
                return_data.append(data)
            return Response(return_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
        
class AddNewRuleToGroupCourseView(APIView):
    def post(self, request):
        try:
            group_course_code = request.data.get('group_course_code')
            rule_code = request.data.get('rule_code')
            parameter = request.data.get('parameter')
            if not group_course_code or not rule_code:
                return Response({"error": "group_course_code and rule_code are required"}, status=status.HTTP_400_BAD_REQUEST)

            group_course = GroupCourse.objects.filter(group_course_code=group_course_code, is_active=True)
            if not group_course:
                return Response({"error": "Group course not found"}, status=status.HTTP_404_NOT_FOUND)
            rule = Rule.objects.filter(rule_code=rule_code, is_active=True)
            if not rule:
                return Response({"error": "Rule not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = GroupRuleSerializer(data={
                    "group": group_course_code,
                    "rule": rule_code,
                    "parameter": parameter
                })
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Add New Group Course - Rule Successful"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UpdateRuleToGroupCourseView(APIView):
    def post(self, request):
        try:
            group_course_code = request.data.get('group_course_code')
            rule_code = request.data.get('rule_code')
            parameter = request.data.get('parameter')
            if not group_course_code or not rule_code:
                return Response({"error": "group_course_code and rule_code are required"}, status=status.HTTP_400_BAD_REQUEST)

            group_course = GroupCourse.objects.filter(group_course_code=group_course_code, is_active=True).first()
            if not group_course:
                return Response({"error": "Group course not found"}, status=status.HTTP_404_NOT_FOUND)
            rule = Rule.objects.filter(rule_code=rule_code, is_active=True).first()
            if not rule:
                return Response({"error": "Rule not found"}, status=status.HTTP_404_NOT_FOUND)
          
            group_rule = GroupRule.objects.filter(group=group_course, rule=rule).first()
            if not group_rule:
                return Response({"error": "GroupRule not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = GroupRuleSerializer(instance=group_rule, data={"parameter": parameter}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Update Group Course - Rule Successful"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DeleteRuleToGroupCourseView(APIView):
    def post(self, request):
        try:
            group_course_code = request.data.get('group_course_code')
            rule_code = request.data.get('rule_code')
            if not group_course_code or not rule_code:
                return Response({"error": "group_course_code and rule_code are required"}, status=status.HTTP_400_BAD_REQUEST)

            group_course = GroupCourse.objects.filter(group_course_code=group_course_code, is_active=True).first()
            if not group_course:
                return Response({"error": "Group course not found"}, status=status.HTTP_404_NOT_FOUND)
            rule = Rule.objects.filter(rule_code=rule_code, is_active=True).first()
            if not rule:
                return Response({"error": "Rule not found"}, status=status.HTTP_404_NOT_FOUND)
            
            group_rule = GroupRule.objects.filter(group=group_course, rule=rule).first()
            if not group_rule:
                return Response({"error": "Group Rule not found"}, status=status.HTTP_404_NOT_FOUND)
            
            group_rule.delete()
            return Response({"status": "Delete Group Course - Rule Successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
   