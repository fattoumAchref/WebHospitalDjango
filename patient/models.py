from django.utils.timezone import now, make_aware
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
import numpy as np

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], default='Male')
    age = models.IntegerField(default=30)
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Rejected', 'Rejected')], default='Confirmed')
    date_joined = models.DateTimeField(default=now)
    date_left = models.DateTimeField(null=True, blank=True, default=None)
    emergency_case = models.BooleanField(default=False)
    face_image = models.ImageField(upload_to='faces/', null=True, blank=True)
    face_embeddings = models.JSONField(null=True, blank=True)  # Stocke directement les embeddings sous forme de liste

    def save(self, *args, **kwargs):
        # Convertir les dates en zone horaire si elles ne le sont pas déjà
        if self.date_left and not self.date_left.tzinfo:
            self.date_left = make_aware(self.date_left)
        if self.date_joined and not self.date_joined.tzinfo:
            self.date_joined = make_aware(self.date_joined)
        super().save(*args, **kwargs)

    def set_face_embeddings(self, embeddings):
    # Si embeddings est un ndarray, le convertir en liste
        if isinstance(embeddings, np.ndarray):
         embeddings = embeddings.tolist()  # Convertit ndarray en liste
         self.face_embeddings = embeddings  # Assigner la liste à face_embeddings



    def get_face_embeddings(self):
        return self.face_embeddings  # Django gère la désérialisation automatiquement
