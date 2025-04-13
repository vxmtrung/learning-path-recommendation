from django.db import models

# Create your models here.
class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    student_code = models.CharField(max_length=50, unique=True)
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField()
    english_level = models.CharField(max_length=50)
    faculty = models.ForeignKey(
        'faculties.Faculty',
        on_delete=models.CASCADE,
        to_field='faculty_code',
        related_name='students'
    )
    GPA = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.student_name