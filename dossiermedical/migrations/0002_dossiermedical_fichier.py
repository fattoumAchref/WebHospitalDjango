# Generated by Django 4.2 on 2024-11-24 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dossiermedical', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dossiermedical',
            name='fichier',
            field=models.FileField(blank=True, null=True, upload_to='dossiers_medicaux/'),
        ),
    ]