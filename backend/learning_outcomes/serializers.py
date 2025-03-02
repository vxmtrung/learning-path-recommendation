from rest_framework import serializers
from .models import Learning_Outcome

class LearningOutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Learning_Outcome
        fields = '__all__'
