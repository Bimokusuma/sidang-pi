# Generated by Django 3.2.3 on 2021-07-28 11:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_record_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 28, 18, 7, 21, 860483)),
        ),
    ]
