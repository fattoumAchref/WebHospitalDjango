from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2','face_image']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Nom d’utilisateur',
                'maxlength': 150,
                'pattern': '[a-zA-Z0-9@.+-_]+',
                'title': 'Utilisez uniquement des lettres, chiffres et @/./+/-/_'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Adresse e-mail',
                'type': 'email'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Numéro de téléphone',
                'pattern': '[0-9]+',
                'title': 'Utilisez uniquement des chiffres',
                'maxlength': 10
            }),
            'password1': forms.PasswordInput(attrs={
                'placeholder': 'Mot de passe',
                'minlength': 8,
                'title': 'Le mot de passe doit comporter au moins 8 caractères'
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': 'Confirmer le mot de passe',
                'minlength': 8
            }),
        }

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        

class PatientUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number']  
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Adresse email", required=True)

