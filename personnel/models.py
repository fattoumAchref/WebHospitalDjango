from django.db import models

class Personnel(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    FONCTION_CHOICES = [
        ('Generaliste', 'Médecin Généraliste'),
        ('Cardiologue', 'Médecin Cardiologue'),
        ('Dermatologue', 'Médecin Dermatologue'),
        ('Pediatre', 'Médecin Pédiatre'),
        ('Chirurgien', 'Médecin Chirurgien'),
        ('Radiologue', 'Médecin Radiologue'),
        ('Psychiatre', 'Médecin Psychiatre'),
        ('Gynecologue', 'Médecin Gynécologue'),
        ('Infirmier', 'Infirmier'),
        ('Secretaire', 'Secrétaire'),
        ('Technicien', 'Technicien'),
    ]

    nom = models.CharField(max_length=100)
    fonction = models.CharField(max_length=100, choices=FONCTION_CHOICES)  # Champ avec des choix
    telephone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    adresse = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.fonction}"
