from django.db import models

# Create your models here.
class RecommendLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        'students.Student', 
        on_delete=models.CASCADE,
        to_field='student_code',
        related_name='recommendlogs'
    )
    log_file_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
