from django.db import models

# Create your models here.
class LearnLog(models.Model):
    learn_log_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        'students.Student',
        to_field='student_code',
        on_delete=models.CASCADE,
        related_name='learnlog'
    )
    course = models.ForeignKey(
        'courses.Course',
        to_field='course_code',
        on_delete=models.CASCADE,
        related_name='learnlog'
    )
    score = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True) 
    count_learn = models.IntegerField(default=0)
    semester = models.CharField(max_length=50)
    
    def __str__(self):
        return self.student.student_name + ' - ' + self.course.course_name