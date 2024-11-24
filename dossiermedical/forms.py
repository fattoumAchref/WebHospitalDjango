from django import forms
from .models import DossierMedical

class DossierMedicalForm(forms.ModelForm):
    class Meta:
        model = DossierMedical
        fields = ['patient', 'description','fichier']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
