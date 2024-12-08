from django.utils.timezone import now
from django.db import models

class Personnel(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    FONCTION_CHOICES = [
        ('Médecin Generaliste', 'Médecin Généraliste'),
        ('Médecin Cardiologue', 'Médecin Cardiologue'),
        ('Médecin Dermatologue', 'Médecin Dermatologue'),
        ('Médecin Pediatre', 'Médecin Pédiatre'),
        ('Médecin Chirurgien', 'Médecin Chirurgien'),
        ('Médecin Radiologue', 'Médecin Radiologue'),
        ('Médecin Psychiatre', 'Médecin Psychiatre'),
        ('Médecin Gynecologue', 'Médecin Gynécologue'),
        ('Infirmier', 'Infirmier'),
        ('Secretaire', 'Secrétaire'),
        ('Technicien', 'Technicien'),
    ]
    fonction = models.CharField(max_length=100, choices=FONCTION_CHOICES)
    telephone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    adresse = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(upload_to='médecin/', null=True, blank=True, default='médecin/doctor.png')
    date_joined = models.DateTimeField(default=now)
    date_left = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.fonction}"
