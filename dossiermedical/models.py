from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class DossierMedical(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dossiers_medicaux')
    description = models.TextField()  # Exemple pour des notes médicales
    date_creation = models.DateTimeField(auto_now_add=True)
    dernier_mise_a_jour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dossier médical de {self.patient.username}"
