from django.db import models

# Create your models here.
class Major(models.Model):
    major_id = models.CharField(max_length=50, unique=True, primary_key=True)
    major_name = models.CharField(max_length=200)
    faculty = models.ForeignKey('faculties.Faculty', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.major_name} ({self.major_id})"