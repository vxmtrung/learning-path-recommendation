from django.db import models

# Create your models here.
class ScheduledTask(models.Model):
  METHOD_CHOICES = [
    ("GET", "GET"),
    ("POST", "POST")
  ]

  url = models.URLField()
  method = models.CharField(max_length=10, choices=METHOD_CHOICES, default="POST")
  body = models.JSONField(blank=True, null=True)
  run_time = models.DateTimeField()

  def __str__(self):
    return f"{self.method} {self.url} at time {self.run_time}"