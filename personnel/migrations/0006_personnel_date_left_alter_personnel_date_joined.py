# Generated by Django 4.2 on 2024-12-03 14:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0005_personnel_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='personnel',
            name='date_left',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 3, 14, 51, 1, 256835, tzinfo=datetime.timezone.utc)),
        ),
    ]
