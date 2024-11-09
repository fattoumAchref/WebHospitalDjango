from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from personnel.models import Personnel  # Import the Personnel model

User = get_user_model()

class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    personnel = models.ForeignKey(Personnel, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')  # Assign a doctor or personnel
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()

    def __str__(self):
        return f"Appointment for {self.patient.username} with {self.personnel.nom if self.personnel else 'No Personnel'} on {self.date} at {self.time}"
