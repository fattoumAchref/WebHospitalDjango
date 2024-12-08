from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import make_aware
from datetime import datetime

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], default='Male')
    age = models.IntegerField(default=30) 
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Rejected', 'Rejected')],default='Confirmed')
    date_joined = models.DateTimeField(default=now)  
    date_left = models.DateTimeField(null=True, blank=True, default=None) 
    emergency_case = models.BooleanField(default=False)  
    def save(self, *args, **kwargs):
        if self.date_left and not self.date_left.tzinfo:
            self.date_left = make_aware(self.date_left)
        if self.date_joined and not self.date_joined.tzinfo:
            self.date_joined = make_aware(self.date_joined)
        super().save(*args, **kwargs)