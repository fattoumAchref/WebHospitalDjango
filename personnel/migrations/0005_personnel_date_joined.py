# Generated by Django 4.2 on 2024-12-03 14:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0004_alter_personnel_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='personnel',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 3, 14, 47, 7, 276878, tzinfo=datetime.timezone.utc)),
        ),
    ]
