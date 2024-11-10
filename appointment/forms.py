from django import forms
from .models import Appointment
from personnel.models import Personnel  # Import Personnel model

class AppointmentForm(forms.ModelForm):
    personnel = forms.ModelChoiceField(
        queryset=Personnel.objects.all(),
        required=True,
        label="Choisir un personnel",
        widget=forms.Select(attrs={'class': 'form-control'})  # Optional styling
    )

    class Meta:
        model = Appointment
        fields = ['date', 'time', 'description', 'personnel']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'personnel': forms.Select(attrs={'class': 'form-control'}),
        }