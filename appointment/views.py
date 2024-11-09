from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import AppointmentForm

# Check if user is an administrator
def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def add_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')  # Redirect to a page listing appointments
    else:
        form = AppointmentForm()
    return render(request, 'add_appointment.html', {'form': form})
