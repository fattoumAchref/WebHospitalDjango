# Generated by Django 4.2 on 2024-12-13 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0007_alter_customuser_face_encoding'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='face_image',
            field=models.ImageField(blank=True, null=True, upload_to='faces/'),
        ),
    ]
