from django.db import models

# Create your models here.
class Rule(models.Model):
    rule_code = models.CharField(primary_key=True)
    rule_name = models.CharField(max_length=200)
    rule_description = models.TextField()
    is_active = models.BooleanField(default=True)