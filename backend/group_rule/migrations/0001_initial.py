# Generated by Django 5.1.7 on 2025-03-18 17:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rules', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupRule',
            fields=[
                ('group_rule_id', models.AutoField(primary_key=True, serialize=False)),
                ('parameter', models.JSONField()),
                ('rule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='rules.rule')),
            ],
        ),
    ]
