from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Facture(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='factures')
    description = models.TextField()  # Détails de la facture
    montant = models.DecimalField(max_digits=10, decimal_places=2)  # Montant total de la facture
    date_emission = models.DateField(auto_now_add=True)
    date_paiement = models.DateField(null=True, blank=True)  # Date de paiement, si déjà payé
    est_payee = models.BooleanField(default=False)  # Statut de paiement

    def __str__(self):
        return f"Facture #{self.id} - {self.patient.username}"
