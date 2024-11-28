from django.db import models

# Create your models here.
class Syllabus(models.Model):
    name = models.TextField()
    course = models.ForeignKey(
        'courses.Course',
        to_field='course_code',
        on_delete=models.CASCADE
    )