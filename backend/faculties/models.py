from django.db import models

# Create your models here.
class Faculty(models.Model):
    faculty_id = models.CharField(max_length=50, unique=True, primary_key=True)
    faculty_name = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.faculty_name} ({self.faculty_id})"