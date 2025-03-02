from django.db import models

# Create your models here.
class GroupCourse(models.Model):
    group_course_id = models.AutoField(primary_key=True)
    group_course_code = models.CharField(max_length=50, unique=True)
    group_course_name = models.CharField(max_length=200)
    total_course = models.IntegerField()
    minimum_course = models.IntegerField()
    alternative = models.BooleanField(default=False)
    specifically = models.BooleanField(default=False)
    alternative_group = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        to_field='group_course_code',
        related_name='dependent_groups'
    )
    
    def __str__(self):
        return f"{self.group_course_name} ({self.group_course_code})"
    