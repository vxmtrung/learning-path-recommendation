from django.db import models

# Create your models here.
class GroupRule(models.Model):
    group_rule_id = models.AutoField(primary_key=True)
    group = models.ForeignKey(
        'group_course.GroupCourse',
        on_delete=models.CASCADE,
        to_field='group_course_code',
        related_name='rules',
        null=True,
        blank=True,
    )
    rule = models.ForeignKey(
        'rules.Rule',
        on_delete=models.CASCADE,
        to_field='rule_code',
        related_name='groups'
    )
    parameter = models.JSONField()