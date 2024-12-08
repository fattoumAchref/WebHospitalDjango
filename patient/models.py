from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], default='Male')
    age = models.IntegerField(default=30) 
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Rejected', 'Rejected')],default='Confirmed')
    date_joined = models.DateTimeField(default=now)  
    date_left = models.DateTimeField(null=True, blank=True, default=None) 
    emergency_case = models.BooleanField(default=False)  