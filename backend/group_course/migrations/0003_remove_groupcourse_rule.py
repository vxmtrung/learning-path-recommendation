# Generated by Django 5.1.7 on 2025-03-18 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_course', '0002_groupcourse_rule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupcourse',
            name='rule',
        ),
    ]
