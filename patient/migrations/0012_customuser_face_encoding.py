# Generated by Django 4.2 on 2024-12-14 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0011_remove_customuser_face_encoding_customuser_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='face_encoding',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]
