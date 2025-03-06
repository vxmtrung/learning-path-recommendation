from rest_framework import serializers
from .models import ScheduledTask
import pytz

class ScheduledTaskSerializer(serializers.ModelSerializer):

  run_time = serializers.SerializerMethodField()

  class Meta:
    model = ScheduledTask
    fields = "__all__"
    # fields = ["run_time"]

  def get_run_time(self, obj):
      tz = pytz.timezone("Asia/Bangkok")  # Chuyển sang múi giờ +7
      return obj.run_time.astimezone(tz).isoformat()