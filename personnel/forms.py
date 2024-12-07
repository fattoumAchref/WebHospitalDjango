from django import forms
from personnel.models import Personnel

class AddDoctorForm(forms.ModelForm):

    class Meta:
        model = Personnel
        fields = ['prenom', 'nom', 'fonction', 'telephone', 'email', 'photo' , 'adresse']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'fonction': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'photo': forms.EmailInput(attrs={'class': 'form-control'}),
            'adresse': forms.EmailInput(attrs={'class': 'form-control'}),
        }
