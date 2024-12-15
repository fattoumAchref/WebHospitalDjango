from django import forms
from .models import Facture

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['patient', 'description', 'montant', 'est_payee', 'date_paiement']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'date_paiement': forms.DateInput(attrs={'type': 'date'}),
            'est_payee': forms.Select(choices=[('Oui', 'Oui'), ('Non', 'Non')])  # Ajout des choix 'Oui' et 'Non'
        }  
