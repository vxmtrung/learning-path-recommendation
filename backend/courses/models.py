from django.db import models

# Create your models here.
class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    course_name = models.CharField(max_length=200) 
    majors = models.ManyToManyField(
        'majors.Major',
        related_name='courses',
        blank=True
    )
    prerequisites = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        to_field='course_code',
        related_name='dependent_courses'
    )
    semester = models.IntegerField() 
    count_learner = models.IntegerField()  
    average_score = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)  
    credit = models.IntegerField()   
    group_course = models.ForeignKey(
        'group_course.GroupCourse',
        on_delete=models.CASCADE,
        to_field='group_course_code',
        related_name='courses',
        null=True,
        blank=True
    )
    note = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.course_name} ({self.course_code})"