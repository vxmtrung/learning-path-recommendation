from rest_framework import serializers
from .models import RecommendLog

class RecommendLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendLog
        fields = '__all__'
