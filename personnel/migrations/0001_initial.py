# Generated by Django 5.1.1 on 2024-09-29 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Personnel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('fonction', models.CharField(max_length=100)),
                ('telephone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('adresse', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
