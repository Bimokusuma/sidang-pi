# Generated by Django 3.2.3 on 2021-07-28 11:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_dailyquest_reward'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='date',
            field=models.DateTimeField(default=datetime.date.today),
        ),
    ]
