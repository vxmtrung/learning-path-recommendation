from django.db import models

# Create your models here.
class LearnLog(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True) 
    count_learn = models.IntegerField(default=0)
    credit = models.FloatField(default=0)
    semester = models.CharField(max_length=50)
    learned = models.BooleanField(default=False)
    
    def __str__(self):
        return self.student.student_name + ' - ' + self.course.course_name