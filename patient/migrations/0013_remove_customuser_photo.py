# Generated by Django 4.2 on 2024-12-14 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0012_customuser_face_encoding'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='photo',
        ),
    ]