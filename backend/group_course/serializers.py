from rest_framework import serializers
from .models import GroupCourse

class GroupCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupCourse
        fields = '__all__'
