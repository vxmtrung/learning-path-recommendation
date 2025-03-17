from django.db import models

# Create your models here.
class StudentNeed(models.Model):
    student_need_id = models.AutoField(primary_key=True)
    student_id = models.CharField(max_length=50)
    english_level = models.CharField(max_length=50)
    major = models.JSONField()
    learn_summer_semester = models.CharField(max_length=50)
    summer_semester = models.JSONField()
    group_free_elective = models.CharField(max_length=50)
    over_learn = models.CharField(max_length=50)
    main_semester =  models.JSONField()
    next_semester = models.CharField(max_length=50)
    learn_to_improve = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
