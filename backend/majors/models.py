from django.db import models

# Create your models here.
class Major(models.Model):
    major_id = models.AutoField(primary_key=True)
    major_code = models.CharField(max_length=50, unique=True)
    major_name = models.CharField(max_length=200)
    faculty = models.ForeignKey(
        'faculties.Faculty',
        on_delete=models.CASCADE,
        to_field='faculty_code',
        related_name='majors'
    )
    
    def __str__(self):
        return f"{self.major_name} ({self.major_id})"