# Generated by Django 3.2.3 on 2021-07-28 11:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_record_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 28, 11, 17, 4, 537970, tzinfo=utc)),
        ),
    ]