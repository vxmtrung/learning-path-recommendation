from django.db import models

# Create your models here.
class GroupCourse(models.Model):
    group_course_id = models.AutoField(primary_key=True)
    group_course_code = models.CharField(max_length=50, unique=True)
    group_course_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.group_course_name} ({self.group_course_code})"
    