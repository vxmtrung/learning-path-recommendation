from django.db import models

# Create your models here.
class Student(models.Model):
    student_id = models.CharField(max_length=50, unique=True, primary_key=True)
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField()
    english_level = models.CharField(max_length=50)
    faculty = models.ForeignKey('faculties.Faculty', on_delete=models.CASCADE, blank=True, null=True)
    GPA = models.FloatField(default=0)

    def __str__(self):
        return self.name