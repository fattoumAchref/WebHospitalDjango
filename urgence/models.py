from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class EmergencyCase(models.Model):
    # Coordinates for the emergency location
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    description = models.TextField(null=True, blank=True)  

    status = models.CharField(max_length=50, choices=[
        ('reported', 'Reported'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved')
    ], default='reported')
    
    priority = models.CharField(max_length=50, choices=[
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low')
    ], default='high')
    
    created_at = models.DateTimeField(auto_now_add=True)  # Time when the emergency case was created
    updated_at = models.DateTimeField(auto_now=True)  # Time when the case was last updated
    
    # Optional foreign key for linking to a user (if applicable)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Emergency at {self.created_at} (Lat: {self.latitude}, Lon: {self.longitude}) , Status: {self.status}"