from django.db import models

# Create your models here.
class Faculty(models.Model):
    faculty_id = models.AutoField(primary_key=True)
    faculty_code = models.CharField(max_length=50, unique=True)
    faculty_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.faculty_name} ({self.faculty_code})"