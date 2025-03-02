from rest_framework import serializers
from .models import StudentNeed

class StudentNeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentNeed
        fields = '__all__'
