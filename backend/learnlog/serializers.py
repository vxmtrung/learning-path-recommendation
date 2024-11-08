from rest_framework import serializers
from .models import LearnLog

class LearnLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnLog
        fields = '__all__'
