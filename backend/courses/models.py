from django.db import models

# Create your models here.
class Course(models.Model):
    course_id = models.CharField(max_length=50, unique=True, primary_key=True)  
    course_name = models.CharField(max_length=200) 
    majors = models.ManyToManyField('majors.Major', related_name='courses', blank=True)
    prerequisites = models.ManyToManyField('self', symmetrical=False, related_name='courses', blank=True)
    semester = models.IntegerField() 
    count_learner = models.IntegerField()  
    average_score = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)  
    credit = models.IntegerField()   
    is_group_c = models.BooleanField(default=False)  
    is_group_d = models.BooleanField(default=False)  
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.course_name} ({self.course_id})"