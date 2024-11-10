from django.contrib import messages
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

@login_required
def make_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user  # Link to the logged-in patient
            appointment.save()
            messages.success(request, "Votre rendez-vous a été pris avec succès.")
            return redirect('home')
        else:
            messages.error(request, "Erreur lors de la prise de rendez-vous. Veuillez réessayer.")
    else:
        form = AppointmentForm()
    
    return render(request, 'make_appointment.html', {'form': form})