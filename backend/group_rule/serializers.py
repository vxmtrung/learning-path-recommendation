from rest_framework import serializers
from .models import GroupRule

class GroupRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupRule
        fields = '__all__'
