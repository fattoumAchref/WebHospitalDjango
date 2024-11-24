# Generated by Django 4.2 on 2024-11-24 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personnel',
            name='fonction',
            field=models.CharField(choices=[('Generaliste', 'Médecin Généraliste'), ('Cardiologue', 'Médecin Cardiologue'), ('Dermatologue', 'Médecin Dermatologue'), ('Pediatre', 'Médecin Pédiatre'), ('Chirurgien', 'Médecin Chirurgien'), ('Radiologue', 'Médecin Radiologue'), ('Psychiatre', 'Médecin Psychiatre'), ('Gynecologue', 'Médecin Gynécologue'), ('Infirmier', 'Infirmier'), ('Secretaire', 'Secrétaire'), ('Technicien', 'Technicien')], max_length=100),
        ),
    ]
