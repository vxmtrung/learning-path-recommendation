from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Rule
from .serializers import RuleSerializer
# Create your views here.
class GetRuleView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            rules = Rule.objects.filter(is_active=True)
            serializer = RuleSerializer(rules, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AddRuleView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = RuleSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Add New Rule Successfull"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UpdateRuleView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            rule = Rule.objects.get(rule_code=request.query_params.get('rule_code'), is_active=True)
            serializer = RuleSerializer(rule, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "Update Rule Successful"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Rule.DoesNotExist:
            return Response({"error": "Rule not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class DeleteRuleView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            rule = Rule.objects.get(rule_code=request.query_params.get('rule_code'), is_active=True)
            rule.is_active = False
            rule.save()
            return Response({"status": "Rule deleted successfully"}, status=status.HTTP_200_OK)
        except Rule.DoesNotExist:
            return Response({"error": "Rule not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)