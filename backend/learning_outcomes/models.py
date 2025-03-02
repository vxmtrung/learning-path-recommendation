from django.db import models

# Create your models here.
class Learning_Outcome(models.Model):
    learning_outcome_id = models.AutoField(primary_key=True)
    learning_outcome_code = models.CharField(max_length=10)
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        to_field='course_code',
        related_name='learning_outcomes'
    )
    content_vn = models.TextField()
    content_en = models.TextField()

    