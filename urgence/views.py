from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import EmergencyCase
import json

@csrf_exempt
def fetch_emergencies(request):
    emergencies = EmergencyCase.objects.all().order_by('-created_at')[:50]  # Limit to 50 most recent
    data = [
        {'latitude': emergency.latitude, 'longitude': emergency.longitude}
        for emergency in emergencies
    ]
    return JsonResponse({'emergencies': data}, safe=False)