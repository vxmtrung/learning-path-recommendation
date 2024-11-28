from django.db import models

# Create your models here.
class RecommendLog(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    learning_path = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.student_id